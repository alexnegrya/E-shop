from turtle import back
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


def _is_user_choose_continue(exception: Exception, model_name: str,
  prev_menu_name: str):
    wait('c')
    if not isinstance(exception, UniqueViolation):
        msg = f'{str(exception)[0].upper() + str(exception)[1:]}'
    else:
        field = ''
        for char in str(exception)[str(exception).find('(') + 1:]:
            if char != ')': field += char
            else: break
        msg = f'{model_name} with this {field} already exists'
    return get_data_choice(f'{msg}...', prev_menu_name) == 1


def _get_and_test_models_attrs(model, prev_menu_name: str, *attrs: tuple[str],
        confirm_password=True, debug=False, old_model=None, preattr_str=None,
        show_hint=True, attrs_to_int=None):
    """
    Accepts model (will be used for test objects creation) and list of attrs names.
    Get all data using inputs, test it into global `entered_data` dict if no exception occured.
    `bool` what means user choice to re-enter data or not.
    """
    global entered_data
    model_name = model.__class__.__name__
    if attrs_to_int != None:
        an = 'attrs_to_int arg'
        if type(attrs_to_int) != tuple: raise TypeError(
            f'{an} arg must be a tuple')
        elif any([type(attr) != str for attr in attrs_to_int]):
            raise TypeError(f'{an} must contains only str values')
        elif any([attr not in attrs for attr in attrs_to_int]):
            raise ValueError(
                f'all values in {an} must be present in attrs arg')
    preattr_str = ' ' if preattr_str == None else f' {preattr_str} '
    if old_model != None and show_hint: print('Hint: press enter to keep the'
        ' old value, it works only if old value exists.\n')

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
                    return get_data_choice('Passwords not match...',
                        prev_menu_name) == 1
            if attrs_to_int != None and attr in attrs_to_int:
                try: value = int(value)
                except ValueError: return get_data_choice(
                    f'{attr_name[0].upper() + attr_name[1:]} must be a ' +
                    'number...', 'start') == 1
            try:
                validate_model_attrs(model, **{attr: value})
                entered_data[model][attr] = value
            except Exception as e:
                if not debug: return _is_user_choose_continue(e, model_name, prev_menu_name)
                else: raise e


def _add_sections_to_title(title: str, *sections: tuple[str],
  separator=' -> ', only_add=False, only_remove=False) -> str:
    """
    Add or remove every section to/from title depending on it presence in
    title. Returns changed title.
    """
    all_sections = title.split(separator)
    if (only_add, only_remove) == (False, False):
        for section in sections:
            all_sections.remove(section) if section in all_sections \
                else all_sections.append(section)
    elif only_add and only_remove: raise ValueError(
        'only one of only_add and only_remove args can be True')
    elif only_add: [all_sections.append(s) for s in sections]
    elif only_remove: []
    return separator.join(all_sections)


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
                    if get_data_choice(
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
                if get_data_choice('Wrong password...',
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
            raise SystemExit(EXIT_MSG)


_show_home_screen()


# Main app cycle
while not exit:
    wait('c')
    title = 'E-shop'
    choice = get_user_choice(*main_options, title=title)

    if choice == 1: # Account
        title = _add_sections_to_title(title, 'Account')
        to_main_menu = False
        while not to_main_menu:
            wait('c')

            try: address = am.find(id=active_client.address_id)
            except TypeError: address = None

            attrs_dict = {
                'Email': active_client.email,
                'First name': active_client.first_name,
                'Last name': active_client.last_name,
                'Password': format_password(active_client.password),
            }
            attrs_dict.update({'Country': address.country,
                'City': address.city,
                'Street': address.street,
                'Street number': address.number} \
                if address != None else {'Address': 'Not specified'})
            contacts = conm.find(client_id=active_client.id)
            attrs_dict.update({con.type: con.value for con in contacts} if \
                len(contacts) > 0 else {'Contacts': 'Not specified'})
            o = get_user_choice(*sub_options['account'], title=title + '\n' + \
                json.dumps(attrs_dict, indent=0, ensure_ascii=False) \
                .replace('"', '').strip(r'{}'), add_line=False)

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
                    options += ['Add address'] if address == None else [
                        'Country', 'City', 'Street', 'Street number',
                        'Delete address']
                    start_contacts_option = len(options) + 1
                    if len(contacts) > 0: options += [
                        con.type for con in contacts]
                    options += ['Add contact', 'Back to account menu']

                    section_title = _add_sections_to_title(title,
                        'Change data')
                    c = get_user_choice(*options, title=section_title)
                    wait('c')
                    try:
                        section_title = _add_sections_to_title(section_title,
                            options[c - 1])
                    except KeyError:
                        continue

                    while True:
                        wait('c')
                        print(section_title, '\n')

                        if c == 1: # change all data (user + address)
                            list_for_update = []
                            cstatus = _get_and_test_models_attrs(Client,
                                'change data', 'email', 'first_name',
                                'last_name', 'password',
                                old_model=active_client)
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
            elif o == 2:
                _show_home_screen(title)
                to_main_menu = True
            elif o == 3 and is_user_choice_confirmed():
                cm.delete(active_client)
                active_client = None
                _show_home_screen()
            elif o == 0: break

    elif choice == 2: # Catalog
        title = _add_sections_to_title(title, 'Catalog')
        show_all_categories = True
        while show_all_categories:
            category = _paginator.paginate_all_categories(title, catm)
            if category != None:
                show_this_cat_prods = True
                while show_this_cat_prods:
                    product = _paginator.paginate_products(title, category,
                        catm, pm, *pm.find(category_id=category.id))
                    if product != None:
                        show_prod_page = True
                        while show_prod_page:
                            o = show_product_page(active_client, product,
                                sim, rm, cm)

                            if o == 'Add to cart':
                                in_stock = sim.find(product_id=product.id)[
                                    0].quantity
                                if in_stock == 0:
                                    wait('f', 'This product is out of stock, '
                                        'please more products appear (press '
                                        '[Enter] to back to product page)')
                                    continue
                                while True:
                                    wait('c')
                                    try:
                                        quantity = int(input(
                                            'How much do you want to add? '))
                                    except ValueError:
                                        wait('t', 'Please enter a number')
                                        continue

                                    # Get or create order, order item (or update it)
                                    orders = om.find(client_id=active_client.id)
                                    try:
                                        if len(orders) == 0:
                                            payment = paym.save(Payment(price=0,
                                                method=None))[0]
                                            order = om.save(Order(
                                                payment_id=payment.id,
                                                client_id=active_client.id))[0]
                                            order_item = OrderItem(
                                                quantity=quantity,
                                                product_id=product.id,
                                                order_id=order.id)
                                        else:
                                            order = om.find(
                                                client_id=active_client.id)[0]
                                            order_items = oim.find(
                                                product_id=product.id,
                                                order_id=order.id)
                                            if len(order_items) == 0:
                                                order_item = OrderItem(
                                                    quantity=quantity,
                                                    product_id=product.id,
                                                    order_id=order.id)
                                            else:
                                                order_item = order_items[0]
                                                order_item.quantity += quantity
                                    except ValueError as e:
                                        if 'quantity' in str(e):
                                            if _is_user_choose_continue(
                                              e, 'OrderItem', 'product page'):
                                                continue
                                            else: break
                                        else: raise e
                                    if quantity > in_stock:
                                        if get_data_choice(
                                            'There is no such quantity in stock'
                                            ', please add less or wait until '
                                            'more products appear...',
                                            'product page') == 1: continue
                                        else: break
                                    else:
                                        oim.save(order_item)
                                        input('\nAdded to cart successfully,' + \
                                            ' current product count in your ' + \
                                            'cart: ' + str(order_item.quantity) + \
                                            ' ')
                                        break

                            elif o == 'View all ratings':
                                all_ratings = rm.sort(*rm.find(
                                    product_id=product.id))
                                formatted_ratings = []
                                for i in range(len(all_ratings)):
                                    rating = get_formatted_rating(
                                        all_ratings[i], cm)
                                    if i != len(all_ratings) - 1:
                                        rating += '\n'
                                    formatted_ratings.append(rating)
                                _paginator.paginate(*formatted_ratings,
                                    numerate=False)

                            elif o == 'Leave a rating':
                                while True:
                                    wait('c')
                                    status = _get_and_test_models_attrs(Rating,
                                        'product page', 'stars', 'review',
                                        attrs_to_int=('stars',))
                                    if type(status) == bool:
                                        if status: continue
                                        else: break
                                    rm.save(Rating(
                                        stars=entered_data[Rating]['stars'],
                                        review=entered_data[Rating]['review'],
                                        product_id=product.id,
                                        client_id=active_client.id))
                                    break
                                input('\nRating left successfully, '
                                    'press [Enter] to continue... ')

                            elif o == 'Change my rating':
                                rating = rm.find(product_id=product.id,
                                    client_id=active_client.id)[0]
                                while True:
                                    wait('c')
                                    status = _get_and_test_models_attrs(Rating,
                                        'product page', 'stars', 'review',
                                        old_model=rating,
                                        attrs_to_int=('stars',))
                                    if type(status) == bool:
                                        if status: continue
                                        else: break
                                    rating.stars = entered_data[Rating][
                                        'stars']
                                    rating.review = entered_data[Rating][
                                        'review']
                                    rm.save(rating)
                                    break
                            
                            elif o == 'Delete my rating' and \
                              is_user_choice_confirmed(): rm.delete(rm.find(
                                product_id=product.id,
                                client_id=active_client.id)[0])

                            elif o == 'Back to this category products':
                                show_prod_page = False
                    else: show_this_cat_prods = False
            else: show_all_categories = False

    elif choice == 3: # Cart
        back_to_main_menu = False
        while not back_to_main_menu:
            try:
                order = om.find(client_id=active_client.id)[0]
            except IndexError:
                wait('c')
                wait('t', 'There`s nothing here yet, please use the "Catalog" '
                'option to add products, press [Enter] to return to the main '
                'menu')
                break
            title = _add_sections_to_title(title, 'Cart')
            order_items = oim.find(order_id=order.id)
            back_to_cart_menu = False
            while not back_to_cart_menu:
                formatted_ois, total_cost = get_formatted_order_items(catm, pm,
                    *order_items, with_total_cost=True)
                formatted_order = format_order(order, formatted_ois, total_cost,
                    paym)
                o = get_user_choice(*sub_options['cart'], title=title +
                    '\n\n' + formatted_order)
                
                if o == 1: # Complete order
                    back_to_cart_menu = complete_order(om, am, paym, sim,
                        order, order_items, formatted_ois, shm.all(), sem.all())
                    back_to_main_menu = back_to_cart_menu
                
                elif o == 2: # Change products count
                    option = _paginator.paginate(*formatted_ois, title=title + 
                        '\n\nPlease select product.')
                    if option == None: continue
                    order_item = order_items[option - 1]  
                    while True:
                        wait('c')
                        print('If you want to remove product from cart,',
                            'you can enter 0.')
                        entered_data.clear()
                        status = _get_and_test_models_attrs(OrderItem, 'cart',
                            'quantity', old_model=order_item,
                            attrs_to_int=('quantity',))
                        if type(status) == bool:
                            if status: continue
                            else: break
                        break
                    quantity = entered_data[OrderItem]['quantity']
                    if quantity == 0:
                        oim.delete(order_item)
                        order_items.pop(option - 1)
                    else:
                        order_item.quantity = quantity
                        oim.save(order_item)
                        order_items[option - 1] = order_item

                elif o == 3: # Clear cart
                    om.delete(order)
                    back_to_cart_menu = True
                
                elif o == 0: # Back to main menu
                    back_to_cart_menu, back_to_main_menu = True, True

    elif choice == 0: # Exit
        wait('c')
        raise SystemExit(EXIT_MSG)
