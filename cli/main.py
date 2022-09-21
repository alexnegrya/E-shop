from os import system
from textwrap import indent


# Global config
active_client = None
exit = False
entered_data = {}
exit_msg = 'Thank you for using this app!'
not_ready_msg = 'This functional coming soon, please wait'


# Options (described which models and for which operations will be used in each option)
main_options = (
    'Account', # Client CRUD, Address CRUD, Contact CRUD
    'Catalog', # Category R, Product page - Product R, StockItem R, Rating CRU, Money CRU, Order CU, OrderItem CU
    'Cart (coming soon)', # Order RUD, OrderItem RUD, Service R, Shop R, Payment CRUD and other models related to this models
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
    )
}


# Behaviour

def get_user_choice(*options: tuple[str], title=None, frames=True, clear=True, add_line=True) -> int:
    if type(title) != str and title != None: raise TypeError('title must be str type')
    if any([type(o) != str for o in options]): raise TypeError('all options must be strings')

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
            if option.isnumeric(): option = int(option[0] if len(list(filter(lambda n: n > 9, options.keys()))) == 0 else option)
            else:
                wait('c')
                continue
            if option in options.keys(): return option
            else:
                wait('c')
                continue
        except ValueError: continue


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

    options = ['Add to cart', 'View all ratings',
        'Leave a rating', 'Back to this category products']
    if aclient_rating != None:
        options[2] = 'Change my rating'
        formatted_rating = get_formatted_rating(aclient_rating,
            clients_manager)
        fratings += f'\n\nYour rating:\n{formatted_rating}'
    o = get_user_choice(*options, title=f'{product_info}\n\n{fratings}')
    if o == 0: return options[-1]
    else: return options[o - 1]


def show_order(order, oi_manager, prods_manager, cats_manager,
  payments_manager) -> None:
    formatted_order = 'Your cart:\n'
    order_items = oi_manager.find(order_id=order.id)
    formatted_ois = []
    total_cost = 0
    for order_item in order_items:
        product = prods_manager.find(id=order_item.product_id)
        total_cost += product.price * order_item.quantity
        category = cats_manager.find(id=product.category_id)
        formatted_ois.append(' | '.join((product.name, f'{product.price} MDL',
            get_formatted_category(category, cats_manager))) +
            f' --- x{order_item.quantity}')
    formatted_order += '\n'.join(formatted_ois)
    payment = payments_manager.find(id=order.payment_id)
    payment.price = total_cost
    print(formatted_order + '\n\n' + '\n'.join((
        f'Total cost: {payment.price} MDL', 'Payment method: ' + 
        f'{payment.method if payment.method != None else "Not specified"}')))


# Additional functions

def wait(mode: str, msg='Press [Enter] to continue'):
    MODES = ('c', 't', 'a')
    if type(mode) != str: raise TypeError('mode must be a string')
    if mode not in MODES: raise ValueError('unknown mode')

    if mode == 'c': system('clear')
    elif mode in ('t', 'a'): input(f'\n{msg}... ')
    if mode == 'a': system('clear')


def format_password(password: str):
    return password[0] + '*' * len(password[1:-1]) + password[-1]
