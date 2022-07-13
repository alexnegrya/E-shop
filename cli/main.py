from os import system


# Config
user_id = 1
address_id = 1
active_user = None
exit = False
entered_data = {}


# Options (described which models and for which operations will be used in each option)
main_options  = {
    1: 'Account', # Customer CRUD, Address CRUD
    2: 'Catalog', # Category R, Product page - Product R, Rating R and CU if Product was already bought, Money R, Currency R, Order CU, OrderItem CU
    3: 'Cart', # Order RUD, OrderItem RUD, Shop R, Payment CRUD
    0: 'Exit'
}
sub_options = {
    'account': {
        1: 'Change data', # Change Customer and his Address attrs
        2: 'Change user', # Change active Customer
        0: 'Back to main menu'
    },
    'catalog': {
        1: 'All products', # Sorting by updated and created DESC
        2: 'Categories', # 1 ... n - categories names, 0 - exit to catalog menu
    0: 'Back to main menu'
    }
}


# Behaviour
def get_user_choice(options: dict[int, str], title=None, frames=True, clear=True):
    if type(title) != str and title != None: raise TypeError('title must be str type')
    if type(options) != dict: raise TypeError('options must be dict type')

    while True:
        if clear:
            system('clear')
        try:
            if title != None: print(title, '\n')
            if frames: print('#'*30)
            [print(f'{key}. {options[key]}') for key in options]
            if frames: print('#'*30)

            option = input('>>> ')
            return int(option[0] if len(list(
                filter(lambda n: n > 9, options.keys()))) == 0 else option)
        except ValueError:
            continue


def print_products(products):
    # print many products
    if len(products) >= 6:
        from .paginator import paginate
        add_to_order = paginate(products, 'Cart')
        return add_to_order
    # print a few products
    else:
        hint = True
        help = '\nEnter \"buy\" to add product to cart or \"back\" to return to the main menu.'
        while True:
            system('clear')
            for product in products:
                print(product)
            if hint:
                print(help)
                hint = False
            option = input('\n>>> ')
            if option == 'buy':
                return True
            elif option == 'back':
                return False


# Additional functions

def wait(mode):
    modes = ['c', 't', 'a']
    # check type
    if type(mode) != str:
        raise TypeError('mode must be str type')
    # check mode
    if mode not in modes:
        raise ValueError('unknown mode')
    # proccesing
    if mode == 'c':
        system('clear')
    elif mode == 't':
        input('\nPress [Enter] to continue... ')
    else:
        input('\nPress [Enter] to continue... ')
        system('clear')
