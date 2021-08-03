def paginate(l, title=None):
    from os import system
    from math import ceil

    # help
    h = 'Enter \"<\" or \">\" to go to the previous or next page\
 and \"p\" to go the specified page.\
 \nEnter \"buy\" to add product to cart or \"back\" to return to the main menu.'

    # hint
    hint = True

    # paginator data
    per_page = 5
    current_page = 1
    page_total = ceil(len(l) / per_page)
    page_min = (len(l)) - (len(l)) + 1

    while True:
        system('clear')

        start_i = (current_page - 1) * per_page
        end_i = start_i + per_page

        # print list
        if title == None:
            print('List:\n')
        else:
            if type(title) == str:
                print(f'{title}:\n')
            else:
                raise TypeError('title must be str type')
        for i in range(len(l)):
            if i in range(start_i, end_i):
                print(l[i])
        print()

        # print pages
        for page in range(1, page_total + 1):
            if page == current_page:
                print(f'[{page}]', end=' ')
            else:
                print(page, end=' ')
        print()

        # interaction
        if hint == True:
            print('Enter \"help\" to more information')
            hint = False
        enter = input('\n>>> ')
        print()

        if enter == 'p':
            print('Enter the number of the page you want to go')
            choose = int(input('\n>>> '))
            if choose < page_min:
                current_page = page_min
            elif choose > page_total:
                current_page = page_total
            else:
                current_page = choose
        elif enter == '<':
            current_page -= 1
            if current_page < page_min:
                current_page = 1
        elif enter == '>':
            current_page += 1
            if current_page > page_total:
                current_page = page_total
        elif enter == 'help':
            system('clear')
            print(h)
            input('\nPress [Enter] to continue... ')
        elif enter == 'back':
            return False
        elif enter == 'buy':
            return True
