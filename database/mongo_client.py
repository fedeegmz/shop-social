# Python
import os
# from bson import ObjectId

# # typing
# from typing import Union

# # FastAPI
# from fastapi import HTTPException, status
# from fastapi.encoders import jsonable_encoder

# pymongo
from pymongo import MongoClient

# # models
# from models.user import User


class MongoDB:
    """
    The MongoDB class is a Python class that provides methods for interacting with a MongoDB database.
    This class contains methods for retrieving, updating, and creating users and grocery lists.
    There are also methods for checking the existence of a user and 
    getting specific grocery lists by order number.

    The documentation for this class has been provided by ChatGPT, 
    a natural language model based on OpenAI's GPT-3.5.
    The documentation includes details on input and output parameters, 
    as well as possible exceptions that may be thrown during the execution of the methods.
    """

    def __init__(self) -> None:
        """
        Initializes a MongoDB instance.
        """
        username = os.getenv("SHOP_SOCIAL_DB_USER")
        password = os.getenv("SHOP_SOCIAL_DB_PASSW")
        test = os.getenv("IS_TEST_DB", None)

        atlas_url = f'mongodb+srv://{username}:{password}@main.v5svgs3.mongodb.net/?retryWrites=true&w=majority'
        
        if test:
            self.__db_client = MongoClient(atlas_url).test
        else:
            self.__db_client = MongoClient(atlas_url).production
        
        self.users_db = self.__db_client.users
        self.shops_db = self.__db_client.shops
        self.products_db = self.__db_client.products
        self.carts_db = self.__db_client.carts
