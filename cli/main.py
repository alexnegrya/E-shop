from os import system
from .paginator import paginate


# Config
active_client = None
exit = False
entered_data = {}
exit_msg = 'Thank you for using this app!'


# Options (described which models and for which operations will be used in each option)
main_options = (
    'Account', # Client CRUD, Address CRUD, Contact CRUD
    'Catalog', # Category R, Product page - Product R, StockItem R, Rating CRU, Money CRU, Currency R, Order CU, OrderItem CU
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


def print_products(products: list):
    # print many products
    if len(products) >= 6: return paginate(products, 'Cart')
    # print a few products
    else:
        hint = True
        help = '\nEnter \"buy\" to add product to cart or \"back\" to return to the main menu.'
        while True:
            system('clear')
            [print(product) for product in products]
            if hint:
                print(help)
                hint = False
            option = input('\n>>> ')
            if option == 'buy': return True
            elif option == 'back': return False


# Additional functions

def wait(mode: str):
    MODES = ('c', 't', 'a')
    if type(mode) != str: raise TypeError('mode must be a string')
    if mode not in MODES: raise ValueError('unknown mode')

    if mode == 'c': system('clear')
    elif mode in ('t', 'a'): input('\nPress [Enter] to continue... ')
    if mode == 'a': system('clear')


def format_password(password: str): return password[0] + '*' * len(password[1:-1]) + password[-1]
