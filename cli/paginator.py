from os import system
from math import ceil


def paginate(l: tuple | list, title=None):
    help = 'Enter \"<\" or \">\" to go to the previous or next page\
 and \"p\" to go the specified page.\
 \nEnter \"buy\" to add product to cart or \"back\" to return to the main menu.'
    hint = True
    per_page = 5
    current_page = 1
    page_total = ceil(len(l) / per_page)

    while True:
        system('clear')
        start_i = (current_page - 1) * per_page
        end_i = start_i + per_page

        # Print title and content
        if title == None: print('List:\n')
        elif type(title) == str: print(f'{title}:\n')
        else: raise TypeError('title must be str type')
        [print(l[i]) for i in l[start_i:end_i]]
        print()

        # Print pages
        for page in range(1, page_total + 1):
            print(f'[{page}]', end=' ') if page == current_page else print(page, end=' ')
        print()

        # Interaction
        if hint == True:
            print('Enter \"help\" to more information')
            hint = False
        enter = input('\n>>> ')
        print()

        if enter == 'p':
            print('Enter the number of the page you want to go')
            try: choice = int(input('\n>>> '))
            except ValueError: continue
            current_page = 1 if choice < 1 else page_total if choice > page_total else choice
        elif enter == '<':
            if current_page < 1: current_page = 1
            else: current_page -= 1
        elif enter == '>':
            if current_page > page_total: current_page = page_total
            else: current_page += 1
        elif enter == 'help':
            system('clear')
            print(help)
            input('\nPress [Enter] to continue... ')
        elif enter in ('back', 'buy'): return enter == 'buy'
