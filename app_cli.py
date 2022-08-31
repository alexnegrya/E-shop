from cli.main import *
from cli.paginators import Paginator
import boot
from boot import *
from datetime import datetime
import json
from models.tools import validate_model_attrs
from getpass import getpass
from psycopg2.errors import UniqueViolation


# Setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)
_paginator = Paginator()


def _get_data_choice(msg: str, prev_menu_name: str): return get_user_choice('Re-enter data', f'Back to {prev_menu_name} menu', title=msg)


def _is_user_choose_continue(exception: Exception, model_name: str, prev_menu_name: str):
    wait('c')
    if not isinstance(exception, UniqueViolation): msg = f'{str(exception)[0].upper() + str(exception)[1:]}'
    else:
        field = ''
        for char in str(exception)[str(exception).find('(') + 1:]:
            if char != ')': field += char
            else: break
        msg = f'{model_name} with this {field} already exists'
    return _get_data_choice(f'{msg}...', prev_menu_name) == 1


def _get_and_test_models_attrs(model, prev_menu_name: str, *attrs: tuple[str],
        confirm_password=True, debug=False, old_model=None, preattr_str=None, show_hint=True):
    """
    Accepts model (will be used for test objects creation) and list of attrs names.
    Get all data using inputs, test it into global `entered_data` dict if no exception occured.
    `bool` what means user choice to re-enter data or not.
    """
    global entered_data
    model_name = model.__class__.__name__
    preattr_str = ' ' if preattr_str == None else f' {preattr_str} '
    if old_model != None and show_hint: print('Hint: press enter to keep the old value, it works only if old value exists.\n')

    for attr in attrs:
        attr_data = attr.split('|')
        if len(attr_data) == 2: attr, attr_name = attr_data[0], attr_data[1]
        else: attr_name = attr
        attr_name = ' '.join(attr_name.strip().split('_'))

        entered_data[model] = entered_data.get(model, {})
        if attr not in entered_data[model]:
            if old_model != None:
                old_attr = getattr(old_model, attr, None)
                if old_attr == None: old_attr = 'was not specified'
                print(f'Old{preattr_str}{attr_name}: {old_attr if attr != "password" else format_password(old_attr)}')
            q = f'Enter {"your" if old_model == None else "new"}{preattr_str}{attr_name}'

            value = input(q + ': ') if attr != 'password' else getpass(q + ': ')
            if old_model != None and value == '' and old_attr != None: value = old_attr
            if confirm_password and attr == 'password' and locals().get('old_attr', None) == None:
                try:
                    validate_model_attrs(model, **{attr: value})
                except Exception as e:
                    if not debug: return _is_user_choose_continue(e, model_name, prev_menu_name)
                    else: raise e
                confirm = getpass(q + ' again: ')
                if value != confirm:
                    if _get_data_choice('Passwords not match...', 'start') == 1: return True
                    return False
            try:
                validate_model_attrs(model, **{attr: value})
                entered_data[model][attr] = value
            except Exception as e:
                if not debug: return _is_user_choose_continue(e, model_name, prev_menu_name)
                else: raise e


def _add_sections_to_title(old_title: str, *sections: tuple[str]) -> str: return old_title + ' -> ' + ' -> '.join(sections)


def _login():
    global active_client
    email_entered = False
    while True:
        entered_data.clear()
        wait('c')

        try:
            if not email_entered:
                status = _get_and_test_models_attrs(Client, 'start', 'email')
                if type(status) == bool:
                    if status: continue
                    else: break
                try:
                    client = cm.find(email=entered_data[Client]['email'])[0]
                    email_entered = True
                except IndexError:
                    if _get_data_choice(
                        'User with this email was not found, please register\
 first...', 'start') == 1: continue
                    else: break
            
            status = _get_and_test_models_attrs(Client, 'start', 'password',
                confirm_password=False)
            if type(status) == bool:
                if status: continue
                else: break
            if entered_data[Client]['password'] == client.password:
                active_client = client
                break
            else:
                if _get_data_choice('Wrong password...',
                    'start') == 1: continue
                else: break
        except Exception as e:
            if _is_user_choose_continue(e, 'Client', 'start'): continue
            active_client = None
            break


def _create_user():
    global active_client
    global entered_data
    entered_data.clear()

    while True:
        wait('c')

        status = _get_and_test_models_attrs(Client, 'start', 'email',
            'first_name', 'last_name', 'password')
        if type(status) == bool:
            if status: continue
            break
        
        # Creating user, set it as active and exit
        try:
            while True:
                wait('c')
                address_option = input('Want you enter your address? (y/n): ').lower()
                if any([address_option.startswith(option) for option in ('y', 'n')]):
                    with_address = True if address_option[0] == 'y' else False
                    break
            wait('c')
            
            if with_address:
                while True:
                    status = _get_and_test_models_attrs(Address, 'start', 'country', 'city', 'street', 'number|street number')
                    wait('c')
                    if type(status) == bool:
                        if status: continue
                        break
                    adata = entered_data[Address]
                    address_id = am.save(Address(country=adata['country'], city=adata['city'], street=adata['street'], number=adata['number']))[0].id
                    break
            cdata = entered_data[Client]
            client = Client(email=cdata['email'],
                first_name=cdata['first_name'], last_name=cdata['last_name'],
                password=cdata['password'], address_id=address_id if with_address else None)
            active_client = cm.save(client)[0]
        except Exception as e:
            if _is_user_choose_continue(e, 'Client', 'start'): continue
            active_client = None
            break
        break


def _show_home_screen(custom_title=None):
    global active_client

    while True:
        if custom_title == None:
            hour = datetime.now().hour
            if hour > 0 and hour < 12:
                day_time = 'morning'
            elif hour > 12 and hour < 18:
                day_time = 'afternoon'
            else:
                day_time = 'evening'
            title = f'Good {day_time}!'
        else: title = f'{custom_title}'

        active_client = None
        choice = get_user_choice('Login', 'Register', 'Exit', title=title)
        if choice == 1:
            _login()
            if active_client != None: break
        elif choice == 2:
            _create_user()
            if active_client != None: break
        elif choice == 0:
            wait('c')
            raise SystemExit(exit_msg)


_show_home_screen()


# Main app cycle
while not exit:
    wait('c')
    title = 'E-shop'
    choice = get_user_choice(*main_options, title=title)

    if choice == 1: # Account
        title = _add_sections_to_title(title, 'Account')
        while True:
            wait('c')

            try: address = am.find(id=active_client.address_id)
            except TypeError: address = None

            attrs_dict = {
                'Email': active_client.email,
                'First name': active_client.first_name,
                'Last name': active_client.last_name,
                'Password': format_password(active_client.password),
            }
            attrs_dict.update({'Country': address.country, 'City': address.city, 'Street': address.street, 'Street number': address.number} \
                if address != None else {'Address': 'Not specified'})
            contacts = conm.find(client_id=active_client.id)
            attrs_dict.update({con.type: con.value for con in contacts} if len(contacts) > 0 else {'Contacts': 'Not specified'})
            o = get_user_choice(*sub_options['account'], title=title + '\n' + json.dumps(attrs_dict, indent=0).replace('"', '').strip(r'{}'), add_line=False)

            if o == 1: # change user data
                while True:
                    try: address = am.find(id=active_client.address_id)
                    except TypeError: address = None
                    contacts = conm.find(client_id=active_client.id)

                    entered_data.clear()
                    options = [
                        'All data',
                        'Email',
                        'First name',
                        'Last name',
                        'Password'
                    ]
                    options += ['Add address'] if address == None else ['Country', 'City', 'Street', 'Street number', 'Delete address']
                    start_contacts_option = len(options) + 1
                    if len(contacts) > 0: options += [con.type for con in contacts]
                    options += ['Add contact', 'Back to account menu']

                    section_title = _add_sections_to_title(title, 'Change data')
                    c = get_user_choice(*options, title=section_title)
                    wait('c')
                    try:
                        section_title = _add_sections_to_title(section_title, options[c - 1])
                    except KeyError:
                        continue

                    while True:
                        wait('c')
                        print(section_title, '\n')

                        if c == 1: # change all data (user + address)
                            list_for_update = []
                            cstatus = _get_and_test_models_attrs(Client, 'change data', 'email', 'first_name', 'last_name', 'password', old_model=active_client)
                            if type(cstatus) == bool:
                                if cstatus: continue
                                break
                            list_for_update.append((active_client, Client))

                            if address != None:
                                astatus = _get_and_test_models_attrs(Address, 'change data', 'country', 'city', 'street', 'number|street number', old_model=address, show_hint=False)
                                if type(astatus) == bool:
                                    if astatus: continue
                                    break
                                [setattr(address, attr, value) for attr, value in entered_data[Address].items()]
                                am.save(address)
                            
                            [setattr(active_client, attr, value) for attr, value in entered_data[Client].items()]
                            cm.save(active_client)

                        elif c in range(2, 6): # change one attr (user attrs only)
                            attr = options[c - 1].lower().replace(' ', '_')
                            status = _get_and_test_models_attrs(Client, 'change data', attr, old_model=active_client)
                            if type(status) == bool:
                                if status: continue
                                break
                            setattr(active_client, attr, entered_data[Client][attr])
                            cm.save(active_client)

                        elif c > 5 and c < start_contacts_option: # create, update or delete address
                            if options[5] == 'Add address': # create
                                status = _get_and_test_models_attrs(Address, 'change data', 'country', 'city', 'street', 'number|street number')
                                if type(status) == bool:
                                    if status: continue
                                    else: break
                                data = entered_data[Address]
                                active_client.address_id = am.save(Address(country=data['country'], city=data['city'], street=data['street'], number=data['number']))[0].id
                                cm.save(active_client)
                            elif c == 10 and is_user_choice_confirmed(): # delete
                                am.delete(active_client.address_id)
                                active_client.address_id = None
                            else: # update
                                attr = options[c - 1].split(' ')[-1].lower()
                                status = _get_and_test_models_attrs(Address, 'change data', attr if attr != 'number' else 'number|street number', old_model=address)
                                if type(status) == bool:
                                    if status: continue
                                    else: break
                                setattr(address, attr, entered_data[Address][attr])
                                am.save(address)
                        
                        elif c >= start_contacts_option: # add contact or update existing
                            add_contact_option = len(options) - 1
                            if c == add_contact_option: # add contact
                                status = _get_and_test_models_attrs(Contact, 'change data', 'type', 'value', preattr_str='contact')
                                if type(status) == bool:
                                    if status: continue
                                    else: break
                                conm.save(Contact(
                                    type=entered_data[Contact]['type'],
                                    value=entered_data[Contact]['value'],
                                    client_id=active_client.id)
                                )
                            elif c < add_contact_option: # change one of contacts
                                contact = conm.find(type=options[c - 1], client_id=active_client.id)[0]
                                cc = get_user_choice('Change', 'Delete', 'Back to change data menu',
                                    title=f'{contact.type}: {contact.value}\nWhat do you want to do with this contact?')
                                if cc == 1:
                                    status = _get_and_test_models_attrs(Contact, 'change data', 'type', 'value', old_model=contact, preattr_str='contact')
                                    if type(status) == bool:
                                        if status: continue
                                        else: break
                                    contact.type = entered_data[Contact]['type']
                                    contact.value = entered_data[Contact]['value']
                                    conm.save(contact)
                                elif cc == 2:
                                    if is_user_choice_confirmed(): conm.delete(contact)
                        break
                    break
            elif o == 2: _show_home_screen(title)
            elif o == 3 and is_user_choice_confirmed():
                cm.delete(active_client)
                active_client = None
                _show_home_screen()
            elif o == 0: break

    elif choice == 2: # Catalog
        wait('a', not_ready_msg)
        continue

        if len(pm.all()) == 0:
            data = tds.getTestProducts()
            for obj in data:
                p = Product(obj['title'], Money(int(obj['price']), 1), 1)
                p.id = obj['id']
                pm.save(p)
        # print products
        add = print_products(pm.all())
        # buy product
        if add:
            # get product id by user input and check it
            try:
                productId = int(input('\nEnter product id: '))
                if productId < (len(pm.all()) - len(pm.all()) + 1)\
                    or productId > len(pm.all()):
                    print('\nProduct with this id not exist!')
                    wait('t')
                    continue
            except:
                print('\nWrong product id!')
                wait('t')
                continue
            # find product and order of active user
            product = pm.findById(productId, False)
            if active_client.order == None:
                active_client.order = Order([product], Money(product.price.amount, 1), 1, 1)
            else:
                active_client.order.itemList.append(product)
                active_client.order.totalCost.amount += product.price.amount
    elif choice == 3: # Cart
        wait('a', not_ready_msg)
        continue

        if active_client.order == None:
            wait('c')
            print('Cart is empty')
            wait('t')
        else:
            wait('c')
            print(active_client.order)
            wait('t')
    elif choice == 0: # Exit
        wait('c')
        raise SystemExit(exit_msg)
