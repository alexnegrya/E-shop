from os import system

# Config
next_id = 1
next_addressId = 1
user_names = []
active_user = None
exit = False

# Options
mainOptions  = {
    1: 'Account',
    2: 'Catalog',
    3: 'Cart',
    0: 'Exit'
}
userOptions = {
    1: 'Change first name',
    2: 'Change last name',
    3: 'Change password',
    4: 'Change user',
    0: 'Back to main menu'
}

# Behaviour
def printOptions(options, title=None, frames=True, clear=True):
    # check type
    if type(title) != str and title != None:
        raise TypeError('title must be str type')
    if type(options) != dict:
        raise TypeError('options must be dict type')
    # input and return
    while True:
        if clear:
            system('clear')
        try:
            if title != None:
                print(title)
            if frames:
                print('#'*30)
            for key in options:
                print(f'{key}. {options[key]}')
            if frames:
                print('#'*30)
            option = int(input('>>> '))
            break
        except ValueError:
            return 100
        except:
            continue
    return option


def printProducts(products):
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

