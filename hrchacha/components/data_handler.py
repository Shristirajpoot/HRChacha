import os
import sys

import streamlit as st
from dotenv import load_dotenv
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from hrchacha.constants import DB_NAME, COLLECTION_NAME
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging

load_dotenv()


class Database:
    def __init__(self):

        try:
            # Get URI from .env file.
            uri = st.secrets["MONGO_URI"]

            if not uri:
                raise ValueError("MONGO_URI not set in environment variables.")

            self.client = MongoClient(uri, server_api=ServerApi('1'))

            self.db = self.client[DB_NAME]
            self.collection: Collection = self.db[COLLECTION_NAME]


            self.client.admin.command("ping")
            logging.info("Connected to MongoDB")

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))

    def insert_user(self, user_data: dict) -> bool:
        """Insert a new candidate record. Returns True if successful."""
        try:
            email = user_data.get("email")

            #Check if user already exists and update it.
            existing = self.collection.find_one({"email":email })
            if existing:
                return self.update_user(email, user_data)


            self.collection.insert_one(user_data)
            logging.info("User data inserted")

            return True
        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            return False

    def update_user(self, email: str, updated_data: dict) -> bool:
        """Update an existing user's record."""
        try:
            result = self.collection.update_one(
                {"email": email},
                {"$set": updated_data}
            )
            if result.modified_count:
                logging.info("User data updated")
                return True
            else:
                logging.info("No data was updated")
                return False
        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            return False
