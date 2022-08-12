from os import system
from math import ceil


class Paginator:
    """
    All needed CLI pagination methods located here.
    """

    def paginate(self, *objs: tuple, title=None, numerate=True) -> int | None:
        HELP = f'''Enter "<" or ">" to go to the previous or next page, "p"
 to go the specified page{" ," if numerate else " or"} "back" to return to the 
 previous menu{" or enter number of item which one you want to choose\
" if numerate else ""}.'''
        hint = True
        per_page = 5
        current_page = 1
        page_total = ceil(len(objs) / per_page)

        while True:
            system('clear')
            start_i = (current_page - 1) * per_page
            end_i = start_i + per_page

            # Print title and content
            if title != None and type(title) == str: print(f'{title}:\n')
            else: raise TypeError('title must be str type')
            if numerate: [print(f'{n}.', obj, '\n') \
                for n, obj in enumerate(objs[start_i:end_i], 1)]
            else: [print(obj, '\n') for obj in objs[start_i:end_i]]

            # Print pages
            for page in range(1, page_total + 1):
                print(f'[{page}]', end=' ') \
                    if page == current_page else print(page, end=' ')
            print()

            # Interaction
            if hint:
                print('Enter \"help\" for controls info')
                hint = False
            s = input('\n>>> ')
            print()

            if s == 'p':
                print('Enter the number of the page you want to go')
                try: choice = int(input('\n>>> '))
                except ValueError: continue
                current_page = 1 if choice < 1 else \
                    page_total if choice > page_total else choice
            elif s == '<':
                if current_page < 1: current_page = 1
                else: current_page -= 1
            elif s == '>':
                if current_page >= page_total: current_page = page_total
                else: current_page += 1
            elif s == 'help':
                system('clear')
                print(HELP)
                input('\nPress [Enter] to continue... ')
            elif s == 'back': break
            elif numerate and s.isnumeric(): return int(s)

    def paginate_products(self, money_manager, cats_manager,
      show_cats_names: bool, *products): pass
