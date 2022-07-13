from db.templates import *


class Rating(Model):
    def __init__(self, id_, stars, review, product_id, customer_id):
        self.id = id_
        self.inDB = False
        self.stars = stars
        self.review = review
        self.product_id = product_id
        self.customer_id = customer_id

    def __str__(self):
        title = f"--- Rating ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        stars = f'Stars: {self.stars}'
        review = f'Review: {self.review}'
        product_id = f'Product id: {self.product_id}'
        customer_id = f'Customer id: {self.customer_id}'
        return f'\n\n{title}\n{id}\n{inDB}\n{stars}\n{review}\n{product_id}\n{customer_id}\n\n'

    def __repr__(self):
        return f'<<{self.id, self.inDB, self.stars, self.review, self.product_id, self.customer_id}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int: raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False):
                raise TypeError('inDB attribute must have bool value')
        elif name == 'stars':
            if type(value) != int: raise TypeError('stars must be int type')
            if value not in range(1, 11): raise ValueError('stars must be in int range 1-10')
        elif name == 'review':
            if type(value) != str: raise TypeError('review must be str type')
            # spliting review by letters
            splited = list(value)
            # checking review for letters repition
            repeated_numbers = {}
            for i in range(len(splited)):
                if splited[i] not in repeated_numbers:
                    repeated_numbers[splited[i]] = 1
                else:
                    repeated_numbers[splited[i]] += 1
            # checking review for the same letters only
            for i in range(len(repeated_numbers)):
                if repeated_numbers[splited[i]] == len(value):
                    raise AttributeError('the review contains only the same letters')
            # Checking review lenght
            if len(value) > 500:
                raise ValueError('review must contain 500 characters max')
            value = f'"{value}"'
        elif name == 'product_id':
            if type(value) != int:
                raise TypeError('product_id must be int type')
        elif name == 'customer_id':
            if type(value) != int:
                raise TypeError('customer_id must be int type')
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == Rating else False


class RatingRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT * FROM ratings')
        if len(data) != 0:
            ratings = []
            for row in data:
                r = self.get_rating(row[0], row[1], row[2], row[3], row[4])
                r.inDB = True
                ratings.append(r)
            out = ''
            for rating in ratings:
                out = out + str(rating)
        else:
            out = '\nNo ratings here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM ratings'))

    # ##### Factory methods #####
    def get_rating(self, id_, stars, review, product_id, customer_id):
        return Rating(id_, stars, review, product_id, customer_id)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM ratings')
        if len(res) > 0:
            ratings = []
            for row in res:
                r = self.get_rating(row[0], row[1], row[2], row[3], row[4])
                r.inDB = True
                ratings.append(r)
            return ratings
        else:
            return []

    def save(self, rating):
        # Type verify
        if type(rating) != Rating:
            raise TypeError('the entity should only be Rating type')
        # Save object data
        if rating.inDB == False:
            rating.id = self.pgds.query(f'INSERT INTO ratings(stars, review, product_id, client_id)\
                VALUES ({rating.stars}, \'{rating.review}\', {rating.product_id}, {rating.customer_id})\
                RETURNING id')[0][0]
            rating.inDB = True
        elif rating.inDB:
            self.pgds.query(f'UPDATE ratings\
                SET stars = {rating.stars}, review = \'{rating.review}\', \
                product_id = {rating.product_id}, client_id = {rating.customer_id}\
                WHERE id = {rating.id}')

    def save_many(self, *ratings):
        # Checking object quantity
        l = len(ratings)
        if l in [0, 1]: raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(l):
            if type(ratings[i]) != Rating:
                raise TypeError(f'object number {i + 1} is not a Rating type')
        # Save objects data
        [self.save(rating) for rating in ratings]

    def find_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int type')
        data = self.pgds.query(f'SELECT * FROM ratings WHERE id = {id_}')
        if len(data) > 0:
            r = Rating(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4])
            r.inDB = True
            return r
    
    def delete_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must ne int type')
        self.pgds.query(f'DELETE FROM ratings WHERE id = {id_}')
