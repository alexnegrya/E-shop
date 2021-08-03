class Rating:
    __ids = []

    def __init__(self, stars, review, productId, customerId):
        self.id = self.__get_id()
        self.stars = stars
        self.review = review
        self.productId = productId
        self.customerId = customerId

    def __get_id(self):
        from random import randint
        ID = ''
        for v in range(randint(4, 6)):
            ID = ID + str(randint(0, 9))
        return int(ID)

    def __check_id(self, id_):
        if id_ not in self.__ids:
            if id_ < 1 or id_ > 1000000:
                raise ValueError(
                    'id must be greater then 0 and lesser then 1000000')
            elif type(id_) != int:
                raise TypeError('id must be an integer')
            else:
                return True
        else:
            return False

    def __str__(self):
        title = f"--- Rating ---"
        id = f"Id: {self.id}"
        stars = f'Stars: {self.stars}'
        review = f'Review: {self.review}'
        productId = f'Product id: {self.productId}'
        customerId = f'Customer id: {self.customerId}'
        out = f'\n\n{title}\n{id}\n{stars}\n{review}\n{productId}\n{customerId}\n\n'
        return out

    def __repr__(self):
        return str(self)

    def __setattr__(self, name, value):
        if name == 'id':
            if self.__check_id(value):
                object.__setattr__(self, name, value)
            else:
                while True:
                    if value == self.id:
                        if self.__check_id(value):
                            self.id = self.__get_id()
                    else:
                        break
                object.__setattr__(self, name, value)
        elif name == '__ids':
            raise AttributeError('changing this attribute is not allowed')
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

    def __getattr__(self, name):
        if name == 'id':
            object.__getattribute__(self, str(name))
        elif name == '__ids':
            return tuple(self.__ids)

    def __eq__(self, other):
        if type(other) == Rating:
            if self.id == other.id:
                return True
            else:
                return False


class RatingRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._ratings = []

    def __str__(self):
        if len(self._ratings) != 0:
            out = ''
            for rating in self._ratings:
                out = out + str(rating)
        else:
            out = '\nThere are no ratings here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getRating(self, stars, review, productId, customerId):
        obj = Rating(stars, review, productId, customerId)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._ratings.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._ratings)

    def save(self, rating):
        # Type verify
        if type(rating) != Rating:
            raise TypeError('the entity should only be Rating type')
        # Id verify
        if len(self._ratings) != 0:
            for r in self._ratings:
                if rating == r:
                    raise AttributeError(
                        'a Rating object with this id already exists')
        self._ratings.append(rating)

    def save_many(self, ratings_list):
        # checking ratings_list type
        if type(ratings_list) != list:
            raise TypeError('ratings you want save should be in the list')
        # checking object quantity
        if len(ratings_list) in [0, 1]:
            l = len(ratings_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(ratings_list)):
            if type(ratings_list[i]) != Rating:
                raise TypeError(
                    f'object with index {i} is not a Rating type')
        # checking objects id's
        for rating in ratings_list:
            for r in self._ratings:
                if rating == r:
                    raise AttributeError(
                        'a Rating object with this id already exists')
        self._ratings.extend(ratings_list)

    def overwrite(self, ratings_list):
        # checking ratings_list type
        if type(ratings_list) != list:
            raise TypeError(
                'ratings you want overwrite should be in the list')
        # checking objects type
        for i in range(len(ratings_list)):
            if type(ratings_list[i]) != Rating:
                raise TypeError(
                    f'object with index {i} is not a Rating type')
        # checking objects id's
        for rating in ratings_list:
            for r in self._ratings:
                if rating == r:
                    raise AttributeError(
                        'a Rating object with this id already exists')
        self._ratings = ratings_list

    def findById(self, id_, showMode=True):
        # check id
        if type(id_) != int:
            raise TypeError('id must be int type')
        # search
        for rating in self._ratings:
            if rating.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Rating found by id [{id_}]:' + str(rating) + f"\n{'-'*10}\n"
                else:
                    return rating
        if showMode:
            return f"\n{'-'*10}\n" + f'Rating found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return rating

    def deleteById(self, id_):
        for rating in self._ratings:
            if id_ == rating.id:
                self._ratings.remove(rating)
    
    def findByStars(self, stars, showMode=True):
        # check type
        if type(stars) != int:
            raise TypeError('stars must be int type')
        # search
        found = []
        for rating in self._ratings:
            if rating.stars == stars:
                found.append(rating)
        found.reverse()
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Ratings found by stars {stars}:' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Ratings found by stars {stars}:' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found
    
    def findByStarsRange(self, starsMin, starsMax, showMode=True):
        # check type
        for stars in [starsMin, starsMax]:
            if type(stars) != int:
                raise TypeError('stars ranges must be int type')
        # search
        found = []
        for rating in self._ratings:
            if rating.stars >= starsMin\
                    and rating.stars <= starsMax:
                found.append(rating)
        found.reverse()
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\nFound ratings in stars range [{starsMin}-{starsMax}]: \n{found}\n{'-'*10}"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\nFound ratings in stars range [{starsMin}-{starsMax}]: \nNothing was found\n{'-'*10}"
            else:
                return found
    
    def findByReview(self, review, showMode=True):
        if type(review) != str:
            raise TypeError('review must be str type')
        # With a incomplete match with the review
        found = []
        for rating in self._ratings:
            if review in rating.review:
                found.append(rating)
        if len(found) != 0:
            if showMode:
                out = ''
                for c in found:
                    out = out + str(c)
                return f"\n{'-'*10}\n" + f'Ratings found by review keyword \"{review}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the review
        for rating in self._ratings:
            if rating.review == review:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Found Rating with review \"{review}\":' + str(rating) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Found Rating with review \"{review}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found

    def findByProductId(self, productId, showMode=True):
        # check type
        if type(productId) != int:
            raise TypeError('productId must be int type')
        # search
        found = []
        for rating in self._ratings:
            if rating.productId == productId:
                found.append(rating)
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Ratings found by product id {productId}:' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Ratings found by product id {productId}:' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found

    def findByCustomerId(self, customerId, showMode=True):
        # check type
        if type(customerId) != int:
            raise TypeError('customerId must be int type')
        # search
        found = []
        for rating in self._ratings:
            if rating.customerId == customerId:
                found.append(rating)
        # output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Ratings found by customer id {customerId}:' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Ratings found by customer id {customerId}:' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found
