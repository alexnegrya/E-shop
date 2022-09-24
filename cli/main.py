from os import system
from textwrap import indent
from uuid import uuid4
from datetime import datetime, timedelta
import re


# Global config
active_client = None
exit = False
entered_data = {}
EXIT_MSG = 'Thank you for using this app!'
NOT_READY_MSG = 'This functional coming soon, please wait'
PAYMENT_METHODS = ('In cash', 'By card', 'With PayPal')


# Options (described which models and for which operations will be used in each option)
main_options = (
    'Account', # Client CRUD, Address CRUD, Contact CRUD
    'Catalog', # Category R, Product page - Product R, StockItem R, Rating CRU, Money CRU, Order CU, OrderItem CU
    'Cart', # Order RUD, OrderItem RUD, Service R, Shop R, Payment CRUD and other models related to this models
    'Exit'
)
sub_options = {
    'account': (
        'Change data', # Change Client and his Address and Contact objects attrs
        'Change user', # Change active Client
        'Delete user', # Delete active Client
        'Back to main menu'
    ),
    'catalog': (
        'All products', # Sorting by updated and created DESC
        'Categories', # 1 ... n - categories names, 0 - exit to catalog menu
        'Back to main menu'
    ),
    'cart': (
        'Complete my order',
        'Change products count',
        'Clear cart',
        'Back to main menu'
    )
}


# Auxiliary functions

def wait(mode: str, msg='Press [Enter] to continue'):
    MODES = ('c', 't', 'a', 'f')
    if type(mode) != str: raise TypeError('mode must be a string')
    if mode not in MODES: raise ValueError(
        f'unknown mode, supported modes: {", ".join(MODES)}')

    if mode in ('c', 'f'): system('clear')
    elif mode in ('t', 'a', 'f'): input(f'\n{msg}... ')
    if mode == 'a': system('clear')


def format_password(password: str):
    return password[0] + '*' * len(password[1:-1]) + password[-1]


# Behaviour

def format_numeric_option(option: str, options_length: int) -> int: return int(
    option[0] if len(list(filter(lambda n: n > 9, range(options_length)))) == 0
        else option)

def get_user_choice(*options: tuple[str], title=None, frames=True, clear=True,
  add_line=True) -> int:
    if type(title) != str and title != None:
        raise TypeError('title must be str type')
    if any([type(o) != str for o in options]):
        raise TypeError('all options must be strings')

    exit_option = options[-1]
    options = {n: o for n, o in enumerate(options[:-1], 1)}
    options.update({0: exit_option})

    while True:
        if clear: wait('c')
        try:
            if title != None: print(title, '\n' if add_line else '')
            if frames: print('#'*30)
            [print(f'{key}. {options[key]}') for key in options]
            if frames: print('#'*30)

            option = input('>>> ')
            if option.isnumeric(): option = format_numeric_option(option,
                len(options) - 1)
            else:
                wait('c')
                continue
            if option in options.keys(): return option
            else:
                wait('c')
                continue
        except ValueError: continue

def get_data_choice(msg: str, prev_menu_name: str): return get_user_choice(
    'Re-enter data', f'Back to {prev_menu_name} menu', title=msg)


def is_user_choice_confirmed() -> bool:
    while True:
        wait('c')
        c = input('You are sure? (y/n) >>> ').lower()
        if c != '': c = c[0]
        else: continue
        if c in ('y', 'n'): return c == 'y'

def get_formatted_category(category, cats_manager,
  include_parent_name=True) -> str:
    """
    Recursive format category and it parent categories names in one string.
    """
    if category.parent_category_id == None: return category.name
    else:
        formatted_cat = category.name
        if include_parent_name:
            formatted_pc = get_formatted_category(cats_manager.find(
                id=category.parent_category_id), cats_manager)
            formatted_cat = f'{formatted_pc} -> ' + formatted_cat
        return formatted_cat

def get_formatted_rating(rating, clients_manager) -> str:
    owner = clients_manager.find(id=rating.client_id)
    full_name = f'{owner.first_name} {owner.last_name}'
    stars = f'{"★" * rating.stars}{"☆" * (10 - rating.stars)}'
    return f'  {full_name}   {stars}\n{indent(rating.review, prefix="    ")}'


def _get_rating_type(rating_stars: int) -> str:
    if rating_stars > 7: return 'positive'
    elif rating_stars > 4: return 'average'
    else: return 'negative'


def _get_formatted_ratings_title(ratings_type: str, ratings_symbol: str
  ) -> str: return ' '.join([ratings_symbol * 3,
    ratings_type[0].upper() + ratings_type[1:], ratings_symbol * 3])


def show_product_page(active_client, product, stock_items_manager,
  ratings_manager, clients_manager) -> str:
    """
    Returns option (not it index) selected by user.
    """
    quantity = stock_items_manager.find(product_id=product.id)[0].quantity
    product_info = ' | '.join((product.name, f'{product.price} MDL',
        f'{quantity} in stock' if quantity > 0 else 'Out of stock'))
    
    ratings = ratings_manager.find(product_id=product.id)
    ratings_dict = {'positive': [], 'average': [], 'negative': []}
    aclient_rating = None
    for rating in ratings:
        frating = get_formatted_rating(rating, clients_manager)
        if rating.client_id == active_client.id: aclient_rating = rating
        else:
            if all([len(ratings_dict[t]) == 3 for t in ratings_dict.keys()]):
                break
            rating_type = _get_rating_type(rating.stars)
            if len(ratings_dict[rating_type]) < 3:
                ratings_dict[rating_type].append(frating)
    RATINGS_SYMBOLS = {'positive': '+', 'average': '=', 'negative': '-'}
    formatted_ratings = [
        _get_formatted_ratings_title(name, RATINGS_SYMBOLS[name]) + '\n' + \
'\n'.join(ratings_dict[name]) for name in ratings_dict.keys() if len(
        ratings_dict[name]) > 0]
    fratings = '-=+ Ratings +=-\n\n'
    fratings += '\n\n'.join(formatted_ratings) if len(formatted_ratings) > 0 \
        else 'Neither one rating has been written yet...'

    options = ['Add to cart', 'View all ratings', 'Leave a rating',
        'Back to this category products']
    if aclient_rating != None:
        options[2] = 'Change my rating'
        options.insert(3, 'Delete my rating')
        formatted_rating = get_formatted_rating(aclient_rating,
            clients_manager)
        fratings += f'\n\nYour rating:\n{formatted_rating}'
    o = get_user_choice(*options, title=f'{product_info}\n\n{fratings}')
    if o == 0: return options[-1]
    else: return options[o - 1]


def get_formatted_order_items(cats_manager, prods_manager, *order_items,
  with_total_cost=False) -> tuple:
    formatted_ois = []
    if with_total_cost: total_cost = 0
    for order_item in order_items:
        product = prods_manager.find(id=order_item.product_id)
        if with_total_cost: total_cost += product.price * order_item.quantity
        category = cats_manager.find(id=product.category_id)
        formatted_ois.append(' | '.join((product.name, f'{product.price} MDL',
            get_formatted_category(category, cats_manager))) +
            f' --- x{order_item.quantity} - ' +
            f'{product.price * order_item.quantity} MDL')
    if with_total_cost: return tuple([tuple(formatted_ois), total_cost])
    else: return tuple(formatted_ois)


def get_cart_string(formatted_ois: tuple) -> str:
    return 'Your cart:' + '\n' + '\n'.join(formatted_ois)

def get_order_payment(order, payments_manager, new_total_cost=None):
    payment = payments_manager.find(id=order.payment_id)
    if new_total_cost != None:
        payment.price = new_total_cost
        payments_manager.save(payment)
    return payment

def format_order(order, formatted_ois: tuple, total_cost: int,
  payments_manager) -> str:
    formatted_order = get_cart_string(formatted_ois)
    payment = get_order_payment(order, payments_manager, total_cost)
    return formatted_order + f'\nTotal cost: {payment.price} MDL'


def get_days_names() -> tuple[str]: return tuple(
    [datetime(2000, 1, day).strftime('%A') for day in range(3, 8)] +
    [datetime(2000, 1, day).strftime('%A') for day in range(1, 3)])

def get_order_completion_msg() -> str: return 'Your order is successfully ' + \
    'completed! You will receive an email with its status within an hour.' + \
    f' Please save your order UUID, it will be useful later: {uuid4()}.'

def _is_user_choose_continue(msg: str, prev_menu: str) -> bool:
    msg = msg[0].upper() + msg[1:] + '...'
    choice = get_data_choice(msg, prev_menu)
    return not choice == 0

def raise_validation_error(msg: str, prev_menu: str): raise ValueError('continue' \
    if _is_user_choose_continue(msg, prev_menu) else 'break')

def get_validated_card_data(data_type: str, prev_menu: str):
    standart_err_msg = f'wrong {data_type}'
    data = input(f'Enter {data_type} >>> ')
    if data_type == 'card holder name':
        spl = data.split(' ')
        err_substr = f'{data_type} and surname must'
        if len(spl) != 2: raise_validation_error(
            f'{err_substr} be separated by space', prev_menu)
        elif any([not s[0].isupper() for s in spl]): raise_validation_error(
            f'{err_substr} start with a capital letter', prev_menu)
    elif data_type == 'card number':
        if any([not re.match(p, data) for p in (
          r"[456]\d{3}(-?\d{4}){3}$", r"((\d)-?(?!(-?\2){3})){16}")]):
            raise_validation_error(standart_err_msg, prev_menu)
    elif data_type == 'expiry date':
        try:
            spl = [int(s) for s in data.split('/')]
            if len(spl) != 2: spl = [int(s) for s in data.split('-')]
        except ValueError: raise_validation_error(standart_err_msg, prev_menu)
        if spl[1] < 1 or spl[1] > 99: raise_validation_error(
            'wrong year', prev_menu)
        try: datetime(2000 + spl[1], spl[0], 1)
        except ValueError as e: raise_validation_error(str(e), prev_menu)
        now = datetime.now()
        def raise_error(date_value: str): return raise_validation_error(
            f'card expired, current {date_value} greater than {date_value} ' +
            f'in {data_type}', prev_menu)
        if spl[1] > now.year: raise_error('year')
        elif spl[0] > now.month: raise_error('month')
    elif data_type == 'security code':
        if not data.isnumeric() or len(data) not in (3, 4):
            raise_validation_error(standart_err_msg, prev_menu)
    return data

def is_user_choose_payment_method(title: str, prev_menu: str) -> bool:
    while True:
        wait('c')
        choice = get_user_choice(*list(PAYMENT_METHODS) +
            [f'Back to {prev_menu} menu'], title=title +
            '\n\nPlease select one of the available payment methods.')
        is_selected = True
        if choice == 0: return False # Go back
        elif choice == 1: return True # In cash
        elif choice == 2: # By card
            data_types = ['card holder name', 'card number', 'expiry date',
                'security code']
            while is_selected:
                wait('c')
                data = []
                try:
                    for data_type in data_types.copy():
                        data.append(get_validated_card_data(
                            data_type, prev_menu))
                        data_types.remove(data_type)
                except ValueError as e:
                    if str(e) == 'continue': continue
                    elif str(e) == 'break': is_selected = False
                break
        elif choice == 3: # With PayPal
            while is_selected:
                wait('c')
                email = input('Please enter your PayPal email >>> ')
                if not re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
                  email):
                    if _is_user_choose_continue('wrong PayPal email',
                        prev_menu): continue
                    else: is_selected = False
                break
        return is_selected

def format_services(*services, check_marks_dict=None) -> list:
    formatted_services = []
    for service in services:
        formatted_service = f'{service.name} | {service.price} MDL'
        if check_marks_dict != None:
            check_mark = f'{"☑" if check_marks_dict[service.id] else "☐"}'
            formatted_service = f'{check_mark} {formatted_service}'
        formatted_services.append(formatted_service)
    return formatted_services

def format_shops(addresses_manager, *shops) -> list:
    formatted_shops = []
    days = get_days_names()
    for shop in shops:
        address = addresses_manager.find(id=shop.address_id)
        formatted_shop = f'♦ {address.country}; {address.city}; {address.street} ' \
            + address.number
        working_time = []
        for i in range(len(shop.working_hours)):
            wt = shop.working_hours[i]
            t1, t2 = wt[0], wt[1]
            h1, m1 = t1.split(':')
            h2, m2 = t2.split(':')
            if all([time == '00:00' for time in wt]):
                schedule = 'Non-working day'
            elif wt == ['00:00', '23:59']:
                schedule = 'Works all day'
            else:
                summary = datetime(2000, 1, 1, int(h2) - int(h1), int(m1)) + \
                    timedelta(minutes=int(m2))
                schedule = "-".join(shop.working_hours[i]) + \
                    f' (works {summary.hour} hour(s) and ' + \
                    f'{summary.minute} minute(s))'
            working_time.append(f'{days[i]}: {schedule}')
        formatted_shops.append(formatted_shop + '\n' + '\n'.join(working_time))
    return formatted_shops

def complete_order(orders_manager, addresses_manager, payments_manager,
  si_manager, order, order_items: list, formatted_ois: tuple, shops: list,
  services: list) -> bool:
    payment = get_order_payment(order, payments_manager)
    title = f'{get_cart_string(formatted_ois)}\nTotal cost:' + \
        f' {payment.price} MDL'
    continue_cycle = False

    while True:
        wait('c')
        prev_menu = 'cart'
        if not is_user_choose_payment_method(title, prev_menu): return False
        choice = get_user_choice('Self-delivery', 'Delivery',
            f'Back to {prev_menu} menu',
            title=title + '\n\nPlease select delivery method.')
        if choice == 0: return False
        else: wait('c')

        if choice == 1: print(get_order_completion_msg(), # Self-delivery
            'Now you can view our shops addresses and working hours:\n\n' +
            "\n\n".join(format_shops(addresses_manager, *shops)))

        elif choice == 2: # Delivery
            check_marks_dict = {id_: False for id_ in [
                s.id for s in services]}
            while True:
                continue_cycle = False
                services_str = 'Services:\n' + '\n'.join(format_services(
                    *services, check_marks_dict=check_marks_dict))
                back_option = 'Back to payment method selection menu'
                choice = get_user_choice('Add/Remove service', 'Complete order',
                    back_option, title=services_str)
                if choice == 0: continue_cycle = True # Delivery selection
                elif choice == 2:
                    wait('c')
                    print(get_order_completion_msg()) # Complete
                elif choice == 1: # Add/Remove service
                    c = get_user_choice(*format_services(*services) + 
                        [back_option], title='Select service:')
                    if c == 0: break
                    is_selected = check_marks_dict[services[c - 1].id]
                    check_marks_dict[services[c - 1].id] = not is_selected
                    continue
                break
            for service in services:
                if check_marks_dict[service.id]: payment.price += service.price
            payments_manager.save(payment)

        if continue_cycle: continue
        else: break

    # ----> There may be integrated real payment <----

    for order_item in order_items:
        stock_item = si_manager.find(product_id=order_item.product_id)[0]
        stock_item.quantity -= order_item.quantity
        si_manager.save(stock_item)
    orders_manager.delete(order)
    wait('a', 'Press [Enter] to return to the main menu')
    return True
