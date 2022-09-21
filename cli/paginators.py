from os import system
from math import ceil
from .main import get_formatted_category


class Paginator:
    """
    All needed CLI pagination methods located here.
    """

    def __setattr__(self, name: str, value):
        if name in ('_cats', '_cats_indexes'):
            if type(value) != list: raise TypeError(
                f'{name} attr must be a list')
            if name == '_cats':
                if any([type(obj) != tuple for obj in value]): raise ValueError(
                    f'{name} attr must contains only tuples with categories')
            elif name == '_cats_indexes':
                if len(value) != 2: raise ValueError(
                    f'{name} attr must contains two values')
                elif value[0] != None and type(value[0]) != int:
                    raise TypeError(
                        f'first value of {name} attr must be None or int only')
                elif type(value[1]) != int: raise TypeError(
                    f'last value of {name} attr must be int only')
        object.__setattr__(self, name, value)

    def paginate(self, *objs, title=None, numerate=True) -> int | None:
        HELP = f'''Enter "<" or ">" to go to the previous or next page, "p"
to go the specified page{" ," if numerate else " or"} "back" to return to the 
previous menu{" or enter number of item which one you want to choose" if numerate else ""}\
.'''
        l = len(objs)
        if l == 0: raise ValueError('at least one object must be passed')
        hint = True
        per_page = 5
        current_page = 1
        page_total = ceil(l / per_page)

        while True:
            system('clear')
            start_i = (current_page - 1) * per_page
            end_i = start_i + per_page

            # Print title and content
            if title != None:
                if type(title) == str: print(f'{title}\n')
                else: raise TypeError('title must be str type')
            if numerate: [print(f'{n}.', obj) \
                for n, obj in enumerate(objs[start_i:end_i], 1)]
            else: [print(obj) for obj in objs[start_i:end_i]]

            # Print pages
            print()
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
                if current_page <= 1: current_page = 1
                else: current_page -= 1
            elif s == '>':
                if current_page >= page_total: current_page = page_total
                else: current_page += 1
            elif s == 'help':
                system('clear')
                print(HELP)
                input('\nPress [Enter] to continue... ')
            elif s == 'back': break
            elif numerate and s.isnumeric(): 
                n = int(s)
                if n == 0: continue
                else: return n if n <= l else l

    def __get_list_exclude_other(self, main_list: list,
      other_list: list) -> list:
        l = main_list.copy()
        [l.remove(obj) for obj in other_list]
        return l

    def __get_title_with_changed_sections(self, title: str,
      *sections: tuple[str], separator=' -> ',
      only_add=False, only_remove=False) -> str:
        """
        Add or remove every section to/from title depending on it presence in
        title. Returns changed title.
        """
        all_sections = title.split(separator)
        if (only_add, only_remove) == (False, False):
            for section in sections:
                all_sections.remove(section) if section in all_sections \
                    else all_sections.append(section)
        elif only_add and only_remove: raise ValueError(
            'only one of only_add and only_remove args can be True')
        elif only_add: [all_sections.append(s) for s in sections]
        elif only_remove: []
        return separator.join(all_sections)

    def __get_cats_data(self, cats: list, cats_manager) -> dict:
        cats_data = {'cats': {}}
        cats_data['children'] = {c.id: tuple(cats_manager.find(
            parent_category_id=c.id)) for c in cats}
        cats_data['cats']['with_children'] = tuple([c for c in cats if len(
            cats_data['children'][c.id]) > 0])
        cats_data['cats']['other'] = tuple(self.__get_list_exclude_other(
            list(cats), list(cats_data['cats']['with_children'])))
        cats_data['cats']['all'] = cats_data['cats']['with_children'] + \
            cats_data['cats']['other']
        return cats_data

    def __get_cat_choice(self, cats_data: dict, cats_manager, title: str, 
      show_cats_parents_names=True):
        formatted_cats = []
        for cat in cats_data['cats']['all']:
            formatted_cat = get_formatted_category(cat, cats_manager,
                show_cats_parents_names)
            if cat in cats_data['cats']['with_children']: formatted_cat += ' >'
            formatted_cats.append(formatted_cat)
        return self.paginate(*formatted_cats, title=title)

    def paginate_all_categories(self, title: str, cats_manager):
        """
        For user navigation between categories: with no parent first and after
        their children. User can select only category with no children.
        Returns category selected by user.
        """

        # For cats with no parent
        if getattr(self, '_cats', None) == None \
          and getattr(self, '_cats_indexes', None) == None:
            cats = cats_manager.find(parent_category_id=None)
            self._cats = [tuple(cats)]
            self._cats_indexes = [None, 0]
            cats_data = self.__get_cats_data(cats, cats_manager)
            choice = self.__get_cat_choice(cats_data, cats_manager, title)

        else: # For children
            cats = self._cats[self._cats_indexes[1]]
            prev_cats = self._cats[self._cats_indexes[0]]
            subtitle = title + ' -> ' + get_formatted_category(
                cats_manager.find(id=cats[0].parent_category_id), cats_manager)
            cats_data = self.__get_cats_data(cats, cats_manager)
            choice = self.__get_cat_choice(cats_data, cats_manager,
                subtitle, False)
            if choice == None: # For children parent
                if not any([c.parent_category_id == None \
                  for c in prev_cats]): # All with parents
                    self._cats.pop(-1)
                    self._cats_indexes = list(map(
                        lambda n: n - 1, self._cats_indexes))
                else: # For cats with no parents
                    del self._cats, self._cats_indexes
                return self.paginate_all_categories(title, cats_manager)
        
        if type(choice) == int: # If user selected category
            l = len(cats_data['cats']['with_children'])
            if l > 0 and choice <= l: # Paginate category children
                self._cats.append(cats_data['children'][
                    cats_data['cats']['with_children'][choice - 1].id])
                i2 = self._cats_indexes[1]
                self._cats_indexes = [i2, i2 + 1]
                return self.paginate_all_categories(title, cats_manager)
            else: # Return category with no children
                del self._cats, self._cats_indexes
                return cats_data['cats']['all'][choice - 1]
        else: del self._cats, self._cats_indexes
        
    def paginate_products(self, title: str, prods_manager, *products,
      cats_manager=None):
        """
        Add products categories names to their title if `cats_manager` argument
        received. Returns product selected by user or `None` if user wants come
        back to the previous menu.
        """
        products = prods_manager.sort(*products)
        prods = []
        for product in products:
            prod = f'{product.name} |\
 {product.price} MDL'
            if cats_manager != None: prod += get_formatted_category(
                cats_manager.find(id=product.category_id), cats_manager)
            prods.append(prod)
        choice = self.paginate(*prods, title=title)
        if type(choice) == int: return products[choice - 1]
