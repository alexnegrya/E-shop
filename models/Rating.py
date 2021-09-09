class Rating:
    def __init__(self, id_, stars, review, productId, customerId):
        self.id = id_
        self.inDB = False
        self.stars = stars
        self.review = review
        self.productId = productId
        self.customerId = customerId

    def __str__(self):
        title = f"--- Rating ---"
        id = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        stars = f'Stars: {self.stars}'
        review = f'Review: {self.review}'
        productId = f'Product id: {self.productId}'
        customerId = f'Customer id: {self.customerId}'
        return f'\n\n{title}\n{id}\n{inDB}\n{stars}\n{review}\n{productId}\n{customerId}\n\n'

    def __repr__(self):
        return f'<<{self.id, self.inDB, self.stars, self.review, self.productId, self.customerId}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) == int:
                    object.__setattr__(self, name, value)
                else:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value in (True, False):
                object.__setattr__(self, name, value)
            else:
                raise TypeError(
                    'value for inDB attribute must be True or False only')
        elif name == 'stars':
            # check type
            if type(value) != int:
                raise TypeError('stars must be int type')
            # check if value in correct range
            if value < 1 or value > 10:
                raise ValueError('stars must be in int range 1-10')
            object.__setattr__(self, name, value)
        elif name == 'review':
            # check type
            if type(value) != str:
                raise TypeError('review must be str type')
            # spliting review by letters
            splited = []
            for i in range(len(value)):
                splited.append(value[i])
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
                    raise AttributeError(
                        'the review contains only the same letters')
            # Checking review lenght
            if len(value) > 500:
                raise ValueError('review must contain 500 characters max')
            object.__setattr__(self, name, '\"' + value + '\"')
        elif name == 'productId':
            if type(value) != int:
                raise TypeError('productId must be int type')
            else:
                object.__setattr__(self, name, value)
        elif name == 'customerId':
            if type(value) != int:
                raise TypeError('customerId must be int type')
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == Rating:
            if self.id == other.id:
                return True
            else:
                return False


class RatingRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        data = self.pgds.query('SELECT * FROM ratings')
        if len(data) != 0:
            ratings = []
            for row in data:
                r = self.getRating(row[0], row[1], row[2], row[3], row[4])
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
    def getRating(self, id_, stars, review, productId, customerId):
        return Rating(id_, stars, review, productId, customerId)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM ratings')
        if len(res) > 0:
            ratings = []
            for row in res:
                r = self.getRating(row[0], row[1], row[2], row[3], row[4])
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
                VALUES ({rating.stars}, \'{rating.review}\', {rating.productId}, {rating.customerId})\
                RETURNING id')[0][0]
            rating.inDB = True
        elif rating.inDB:
            self.pgds.query(f'UPDATE ratings\
                SET stars = {rating.stars}, review = \'{rating.review}\', \
                product_id = {rating.productId}, client_id = {rating.customerId}\
                WHERE id = {rating.id}')

    def save_many(self, *ratings):
        # Checking object quantity
        l = len(ratings)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(ratings)):
            if type(ratings[i]) != Rating:
                raise TypeError(f'object number {i+1} is not a Rating type')
        # Save objects data
        for rating in ratings:
            if rating.inDB == False:
                rating.id = self.pgds.query(f'INSERT INTO ratings(stars, review, product_id, client_id)\
                    VALUES ({rating.stars}, \'{rating.review}\', {rating.productId}, {rating.customerId})\
                    RETURNING id')[0][0]
                rating.inDB = True
            elif rating.inDB:
                self.pgds.query(f'UPDATE ratings\
                    SET stars = {rating.stars}, review = \'{rating.review}\', \
                    product_id = {rating.productId}, client_id = {rating.customerId}\
                    WHERE id = {rating.id}')

    def findById(self, id_):
        # Checking id
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Search and return
        data = self.pgds.query(f'SELECT * FROM ratings WHERE id = {id_}')
        if len(data) > 0:
            r = Rating(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4])
            r.inDB = True
            return r
    
    def deleteById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must ne int type')
        # Delete data
        self.pgds.query(f'DELETE FROM ratings WHERE id = {id_}')
