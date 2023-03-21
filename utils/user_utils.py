from fastapi import Response, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.db import userCollection, user_collection
from utils import regex_check
from log import logger
import yaml
from bson.objectid import ObjectId

import logging

log_format= '[%(asctime)s] %(levelname)s:%(name)s %(message)s '
log_file= 'user.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# global patterns
# with open('items.yaml') as f:
#         patterns = yaml.load(f, Loader=yaml.FullLoader)

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = patterns.get('secret_key') or None
# ALGORITHM = patterns.get('algorithm') or None
# ACCESS_TOKEN_EXPIRE_MINUTES = patterns.get('access_token_expire_minutes') or None
# ACCESS_TOKEN_EXPIRE_SECONDS = patterns.get('access_token_expire_seconds') or None
# TEMPORARY_TOKEN_EXPIRE_MINUTES = patterns.get('temporary_token_expire_minutes') or None
# if SECRET_KEY is None or ALGORITHM is None or ACCESS_TOKEN_EXPIRE_MINUTES is None or ACCESS_TOKEN_EXPIRE_SECONDS is None:
#     raise BaseException('Missing env variables')

# credentials_exception = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
# )


# CHECK IF VALUE ALREADY EXISTS IN DB
def check_if_email_exists(email: str):
    logger.info(f"Calling Function for verifying email:{email}")
    user = user_collection.find_one({"email": email})
    logger.debug(f"Data recieved for email:{email}")
    return user is not None


def check_if_username_exists(username: str):
    logger.info(f"Calling Function for existing of username:{username}")
    user = user_collection.find_one({"username": username})
    logger.debug(f"Data recieved for username:{username}")
    return user is not None

    

def check_if_user_id_exists(user_id: str):
    logger.info(f"Calling Function for existing of userId:{user_id}")
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    logger.debug(f"Data recieved for userId:{user_id}")    
    return user is not None


# ADD USER TO DB
def add_user_to_db(email: str, sql_id: str):
    logger.info(f"Calling Function for adding user to db with id:{sql_id} , email:{email}")
    if check_if_email_exists(email):
        logging.debug(f"email;{email} already taken")
        print("email already taken")
        logger.error(f"User creation failed as the email: {email} was taken.")
        raise HTTPException(status_code=409, detail="Email already taken.")
    errors = regex_check.check_values(email=email)
    if not len(errors) == 0:
        print("error while creating")
        logger.error('User creation failed due to invalid input data')
        raise HTTPException(status_code=400, detail=errors)
    user = {"supertokens_user_id": sql_id, "username": None, "email": email}
    _id = user_collection.insert_one(dict(user))
    print("created user")
    logger.debug(f"Created user with email: {email}")
    return str(_id.inserted_id)


def add_username_to_user_data(username: str, user_id: str):
    logger.info(f"Calling Function for adding username to db with username:{username} , userId:{user_id}")
    if check_if_username_exists(username):
        logger.error(f"Adding username failed as the username: {username} was taken.")
        raise HTTPException(status_code=409, detail="Username already taken.")
    errors = regex_check.check_values(username=username)
    if not len(errors) == 0:
        logger.create_error_log('Adding username failed due to invalid input data')
        raise HTTPException(status_code=400, detail=errors)
    user_collection.find_one_and_update({'_id': ObjectId(user_id)}, {"$set": {"username": username}})
    logger.debug(f"Added username: {username} to user with id: {user_id}")
    return "Added username Successfully"


def delete_user_from_db(user_id: str):
    logger.info(f"Calling Function for deleting user to db with  userId:{user_id}")
    if not check_if_user_id_exists(user_id):
        logger.create_error_log(f"User deletion failed as user with id: {user_id} is not found.")
        raise HTTPException(status_code=404, detail="User not found.")
    user_collection.delete_one({"_id": ObjectId(user_id)})
    logger.info(f"User with  userId:{user_id} deleted succesfully")
    return "Deleted Successfully"


def get_user_from_user_id(user_id: str):
    logger.info(f"Calling Function for getting user with  userId:{user_id}")
    user = userCollection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        logger.create_error_log(f"User with id: {user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found.")
    logger.debug(f"Data for userId:{user_id} recieved succesfully")
    return user
