from ui.index import *
from boot import *

# Creating user function
def addUser():
    global next_id
    global next_addressId
    global user_names
    global active_user
    while True:
        try:
            print('E-shop\n')
            # set first name and last name
            name = input('Enter your first name: ')
            if name in user_names:
                print('\nThis first name already was taken by other user!')
                wait('a')
                continue
            surname = input('Enter your last name: ')
            # set password
            back = False
            while True:
                wait('c')
                back = False
                print('E-shop\n')
                password = input('Enter your password: ')
                for letter in password:
                    if letter == ' ':
                        print('\nPassword should not contain spaces!')
                        wait('t')
                        back = True
                        break
                if password == '':
                    print('Password should not be empty!')
                    wait('t')
                    back = True
                elif len(password) < 6:
                    print('Minimum password lenght is 6 symbols!')
                    wait('t')
                    back = True
                if back:
                    continue
                wait('c')
                print('E-shop\n')
                confirm = input('Enter your password again: ')
                if password == confirm:
                    break
                else:
                    print('\nPasswords don\'t match!')
                    wait('t')
            # creating user if data is correct
            user_names.append(name)
            user = Customer(name, surname, next_addressId)
            user.id = next_id
            user.password = password
            user.order = None
            next_id += 1
            crf.save(user)
            active_user = user
            break
        except:
            print('\nWrong first or last name!')
            wait('a')


# Add first user
addUser()

# Starting app cycle
while exit == False:
    wait('c')
    # print main menu
    option = printOptions(mainOptions, 'E-shop')
    # action by user choice
    if option == 1: # Account
        while True:
            wait('c')
            print('Your account:')
            print(active_user)
            o = printOptions(userOptions, clear=False)
            if o == 1: # change first name
                while True:
                    name = input('\nEnter first name: ')
                    if name in user_names:
                        print('\nThis first name already was taken by other user!')
                        wait('a')
                        continue
                    else:
                        try:
                            active_user.firstName = name
                            user_names.append(name)
                        except:
                            print('\nWrong first name!')
                            wait('a')
                            continue
                        break
            elif o == 2: # change last name
                while True:
                    surname = input('\nEnter last name: ')
                    try:
                        active_user.lastName = surname
                    except:
                        print('\nWrong last name!')
                        wait('a')
                        continue
                    break
            elif o == 3: # change password
                while True:
                    active_pw = input('\nEnter current password: ')
                    if active_pw != active_user.password:
                        print('\nWrong current password!')
                        wait('a')
                        continue
                    new_pw = input('Enter new password: ')
                    if new_pw != active_user.password:
                        active_user.password = new_pw
                        break
                    else:
                        print('\nNew password is the same of current password!')
                        wait('a')
                        continue
            elif o == 4: # change user
                print('\nEnter \"log\" to log in to an existing user account.\
                \nEnter \"reg\" to register new user account.\n')
                enter = input('>>> ')
                prompt = True
                if enter == 'log':
                    while True:
                        wait('c')
                        print('Account')
                        if prompt:
                            print('Prompt: Enter \"back\" to return to the account menu\n')
                            prompt = False
                        name = input('Enter user name: ')
                        users = crf.findByFirstName(name, False)
                        if len(users) != 0:
                            print('\nFound users:', users)
                            print('Is here user you want to switch to?\n')
                            answer = input('(yes/no) >>> ')
                            if answer == 'yes':
                                back = False
                                while True:
                                    wait('c')
                                    print('\nFound users:', users)
                                    try:
                                        userId = int(input('Enter user id: '))
                                        if active_user.id == userId:
                                            print('\nYou are already in this account!')
                                            wait('t')
                                            back = True
                                            break
                                        user = crf.findById(userId, False)
                                        if user == None:
                                            print(
                                                '\nInvalid user id, enter user id from the list of found users!')
                                            wait('t')
                                            continue
                                        break
                                    except:
                                        print('\nWrong user id!')
                                        wait('t')
                                        continue
                                if back:
                                    continue
                                password = input('\nEnter user password: ')
                                if password == user.password:
                                    active_user = user
                                    print('\nYou have successfully changed user!')
                                    input('Press [Enter] to return to the account menu... ')
                                    break
                                else:
                                    print('\nWrong user password!')
                                    wait('t')
                            elif answer == 'no':
                                continue
                        else:
                            print(f'\nUsers by search query \"{name}\" not found')
                            wait('t')
                elif enter == 'reg':
                    wait('c')
                    addUser()
                else:
                    print('\nUnknown option!')
                    wait('t')
                    continue
            elif o == 0: # exit
                break
    elif option == 2: # Catalog
        # create shop products if not created
        if len(prf.all()) == 0:
            data = tds.getTestProducts()
            for obj in data:
                p = Product(obj['title'], Money(int(obj['price']), 1), 1)
                p.id = obj['id']
                prf.save(p)
        # print products
        add = printProducts(prf.all())
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
    elif option == 3: # Order
        if active_user.order == None:
            wait('c')
            print('Cart is empty')
            wait('t')
        else:
            wait('c')
            print(active_user.order)
            wait('t')
    elif option == 0: # Exit
        wait('c')
        print('Thank you for using this app!')
        break
