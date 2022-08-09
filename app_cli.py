from cli.main import *
import boot
from boot import *
from datetime import datetime
import sys
import json


# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


def _test_data(model, **attrs):
    SUPPORTED_MODELS = (Client, Address)
    if model in SUPPORTED_MODELS:
        data_for_test = model.test_data.copy()
        data_for_test.update({k.strip('_'): v for k, v in attrs.items() if v != None})
        if model == Client:
            Client(
                data_for_test['id'],
                data_for_test['email'],
                data_for_test['first_name'],
                data_for_test['last_name'],
                data_for_test['password'],
                data_for_test['address_id']
            )
        elif model == Address:
            Address(
                data_for_test['id'],
                data_for_test['country'],
                data_for_test['city'],
                data_for_test['street'],
                data_for_test['number']
            )
    else:
        raise ValueError(f'unsupported model: "{model.__class__.__name__}"')


def _get_data_choice():
    return get_user_choice({1: 'Re-enter data', 0: 'Back to start menu'}, clear=False)


def _is_user_choose_continue(exception):
    wait('c')
    print(f'{str(exception)[0].upper() + str(exception)[1:]}, please enter valid data...\n')
    if _get_data_choice() == 1: return True
    return False


def _get_and_test_models_attrs(model, *attrs: tuple[str], confirm_password=True, debug=False):
    """
    Accepts model (will be used for test objects creation) and list of attrs names.
    Get all data using inputs, test it into global `entered_data` dict if no exception occured.
    `bool` what means user choice to re-enter data or not.
    """
    global entered_data
    for attr in attrs:
        attr_data = attr.split('|')
        if len(attr_data) == 2:
            attr, attr_name = attr_data[0], attr_data[1]
        else:
            attr_name = attr
        entered_data[model] = entered_data.get(model, {})
        if attr not in entered_data[model]:
            q = f'Enter your {" ".join(attr_name.split("_")).strip()}'
            value = input(q + ': ')
            if confirm_password and attr == 'password':
                wait('c')
                confirm = input(q + ' again: ')
                if value != confirm:
                    wait('c')
                    print('Passwords not match')
                    choice = _get_data_choice()
                    if choice == 1: return True
                    return False
            try:
                _test_data(model, **{attr: value})
                entered_data[model][attr] = value
            except Exception as e:
                if not debug: return _is_user_choose_continue(e)
                else: raise e


def _add_sections_to_title(old_title: str, *sections: tuple[str]) -> str:
    return old_title + ' -> ' + ' -> '.join(sections)


def _login():
    global active_user
    entered_data.clear()

    while True:
        wait('c')

        status = _get_and_test_models_attrs(Client, 'email', 'password', confirm_password=False, debug=True)
        if type(status) == bool:
            if status: continue
            break

        try:
            active_user = crf.find_by_data(
                email=entered_data[Client]['email'],
                password=entered_data[Client]['password']
            )[0]
            break
        except IndexError:
            wait('c')
            print('User with this email and password was not found...')
            print('Please, make sure that you have registered and entered correct data.\n')
            if _get_data_choice() == 1: continue
            break
        except Exception as e:
            if _is_user_choose_continue(e): continue
            break


def _create_user():
    global user_id
    global address_id
    global active_user
    global entered_data
    entered_data.clear()

    while True:
        wait('c')

        status = _get_and_test_models_attrs(Client, 'email', 'first_name', 'last_name', 'password')
        if type(status) == bool:
            if status: continue
            break
        
        # Creating user, set it as active and exit
        try:
            while True:
                address_option = input('Want you enter your address? (y/n): ').lower()
                if any([address_option.startswith(option) for option in ('y', 'n')]):
                    with_address = True if address_option[0] == 'y' else False
                    break
            
            if with_address:
                status = _get_and_test_models_attrs(Address, 'country', 'city', 'street', 'number|street number')
                if type(status) == bool:
                    if status: continue
                    break
                adata = entered_data[Address]
                arf.save(arf.get_address(address_id, adata['country'], adata['city'], adata['street'], adata['number']))
            cdata = entered_data[Client]
            active_user = crf.get_client(user_id, cdata['email'], cdata['first_name'], cdata['last_name'], cdata['password'], address_id if with_address else None)
            crf.save(active_user)
            active_user.inDB = True
        except Exception as e:
            if _is_user_choose_continue(e): continue
            break
            
        if with_address: address_id += 1
        user_id += 1
        break


def _show_home_screen(custom_title=None):
    while True:
        wait('c')
        if custom_title == None:
            hour = datetime.now().hour
            if hour > 0 and hour < 12:
                day_time = 'morning'
            elif hour > 12 and hour < 18:
                day_time = 'afternoon'
            else:
                day_time = 'evening'
            print(f'Good {day_time}!\n')
        else: print(f'{custom_title}\n')

        choice = get_user_choice({1: 'Login', 2: 'Register', 0: 'Exit'}, clear=False)
        if choice == 1:
            _login()
            if active_user != None: break
        elif choice == 2:
            _create_user()
            if active_user != None: break
        elif choice == 0:
            sys.exit(0)


_show_home_screen()


# Main app cycle
while exit == False:
    wait('c')
    title = 'E-shop'
    choice = get_user_choice(main_options, title)

    # action by user choice
    if choice == 1: # Account
        while True:
            wait('c')
            title = _add_sections_to_title(title, 'Account')
            print(title)
            try:
                address = arf.find_by_id(active_user.address_id)
            except TypeError:
                address = None
            attrs_dict = {
                'Email': active_user.email,
                'First name': active_user.first_name,
                'Last name': active_user.last_name,
                'Password': active_user.password[0] + '*' * len(active_user.password[1:-1]) + active_user.password[-1],
            }
            attrs_dict.update({'Country': address.country, 'City': address.city, 'Street': address.street, 'Street number': address.number} \
                if address != None else {'Address': 'Not specified'})
            print(json.dumps(attrs_dict, indent=0).replace('"', '').strip(r'{}'))
            o = get_user_choice(sub_options['account'], clear=False)

            if o == 1: # change user data
                while True:
                    entered_data.clear()
                    options = {
                        1: 'All data',
                        2: 'Email',
                        3: 'First name',
                        4: 'Last name',
                        5: 'Password',
                    }
                    user_with_address = active_user.address_id != None
                    options.update({6: 'Add address'} if not user_with_address else {6: 'Country', 7: 'City', 8: 'Street', 9: 'Street number'})
                    options.update({0: 'Back to account menu'})

                    section_title = _add_sections_to_title(title, 'Change data')
                    c = get_user_choice(options, section_title)
                    wait('c')
                    try:
                        section_title = _add_sections_to_title(section_title, options[c])
                    except KeyError:
                        continue
                    print(section_title, '\n')

                    if c == 1: # change all data (user + address)
                        list_for_update = []
                        cstatus = _get_and_test_models_attrs(Client, 'email', 'first name', 'last name', 'password')
                        if type(cstatus) == bool:
                            if cstatus: continue
                            break
                        list_for_update.append((active_user, Client))
                        if user_with_address:
                            astatus = _get_and_test_models_attrs(Address, 'country', 'city', 'street', 'number|street number')
                            if type(astatus) == bool:
                                if astatus: continue
                                break
                            list_for_update.append(arf.find_by_id(active_user.address_id))
                        [[setattr(obj, attr, value) for attr, value in entered_data[model].items()] for obj, model in list_for_update]
                        [model_rf.save(obj) for model_rf, obj in ((crf, active_user), (arf, list_for_update[1][1]))] \
                            if user_with_address else crf.save(active_user)

                    elif c in range(2, 6): # change one attr (user attrs only)
                        attr = options[c].lower().replace(' ', '_')
                        status = _get_and_test_models_attrs(Client, attr)
                        if type(status) == bool:
                            if status: continue
                            break
                        setattr(active_user, attr, entered_data[Client][attr])
                        crf.save(active_user)

                    elif c > 5: # add or update address
                        if options[6] == 'Add address':
                            status = _get_and_test_models_attrs(Address, 'country', 'city', 'street', 'number|street number')
                            if type(status) == bool:
                                if status: continue
                                break
                            data = entered_data[Address]
                            arf.save(arf.get_address(address_id, data['country'], data['city'], data['street'], data['number']))
                            active_user.address_id = address_id
                            crf.save(active_user)
                        else:
                            attr = options[c].split(' ')[-1].lower()
                            status = _get_and_test_models_attrs(Address, attr if attr != 'number' else 'number|street number')
                            if type(status) == bool:
                                if status: continue
                                break
                            address = arf.find_by_id(active_user.address_id)
                            print(entered_data)
                            setattr(address, attr, entered_data[Address][attr])
                            arf.save(address)

                    break

            elif o == 2: _show_home_screen(title)
            elif o == 0: break

    elif choice == 2: # Catalog
        # create shop products if not created
        if len(prf.all()) == 0:
            data = tds.getTestProducts()
            for obj in data:
                p = Product(obj['title'], Money(int(obj['price']), 1), 1)
                p.id = obj['id']
                prf.save(p)
        # print products
        add = print_products(prf.all())
        # buy product
        if add:
            # get product id by user input and check it
            try:
                productId = int(input('\nEnter product id: '))
                if productId < (len(prf.all()) - len(prf.all()) + 1)\
                    or productId > len(prf.all()):
                    print('\nProduct with this id not exist!')
                    wait('t')
                    continue
            except:
                print('\nWrong product id!')
                wait('t')
                continue
            # find product and order of active user
            product = prf.findById(productId, False)
            if active_user.order == None:
                active_user.order = Order([product], Money(product.price.amount, 1), 1, 1)
            else:
                active_user.order.itemList.append(product)
                active_user.order.totalCost.amount += product.price.amount
    elif choice == 3: # Order
        if active_user.order == None:
            wait('c')
            print('Cart is empty')
            wait('t')
        else:
            wait('c')
            print(active_user.order)
            wait('t')
    elif choice == 0: # Exit
        wait('c')
        print('Thank you for using this app!')
        break
