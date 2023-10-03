# PyMongo
from pymongo import MongoClient

# security
from security.config import settings


class MongoDB:

    def __init__(self):
        username = settings.mongodb_user
        password = settings.mongodb_password
        host = settings.mongodb_host
        test = settings.is_test_db
        
        atlas_url = f'mongodb+srv://{username}:{password}{host}'
        
        if test:
            self.__db_client = MongoClient(atlas_url).test
        else:
            self.__db_client = MongoClient(atlas_url).production
        
        self.users_db = self.__db_client.users
        self.shops_db = self.__db_client.shops
        self.products_db = self.__db_client.products
        self.carts_db = self.__db_client.carts
        self.tickets_db = self.__db_client.tickets
