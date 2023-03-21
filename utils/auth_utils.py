# from fastapi import Response, HTTPException, status
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from config.db import userCollection
# from schemas.user import users_serializer
# from utils import regex_check
# from log import logger
# import yaml
# import pprint
# from bson.objectid import ObjectId
#
# global patterns
# with open('items.yaml') as f:
#         patterns = yaml.load(f, Loader=yaml.FullLoader)
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# SECRET_KEY = patterns.get('secret_key') or None
# ALGORITHM = patterns.get('algorithm') or None
# ACCESS_TOKEN_EXPIRE_MINUTES = patterns.get('access_token_expire_minutes') or None
# ACCESS_TOKEN_EXPIRE_SECONDS = patterns.get('access_token_expire_seconds') or None
# TEMPORARY_TOKEN_EXPIRE_MINUTES = patterns.get('temporary_token_expire_minutes') or None
# if SECRET_KEY is None or ALGORITHM is None or ACCESS_TOKEN_EXPIRE_MINUTES is None or ACCESS_TOKEN_EXPIRE_SECONDS is None:
#     raise BaseException('Missing env variables')
#
# credentials_exception = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
# )
#
#
# # PASSWORD
# def hash_password(password: str):
#     return pwd_context.hash(password)
#
#
# def verify_password(password: str, hashed_password: str):
#     return pwd_context.verify(password, hashed_password)
#
#
# # CHECK IF VALUE ALREADY EXISTS IN DB
# def check_if_email_exists(email: str):
#     # finding_user_email = users_serializer(userCollection.find({"email": email}))
#     # return not len(finding_user_email) == 0
#     finding_user_email = userCollection.find_one({"email": email})
#     return finding_user_email is not None
#
#
# def check_if_username_exists(username: str):
#     # finding_user_name = users_serializer(userCollection.find({"username": username}))
#     # return not len(finding_user_name) == 0
#     finding_user_name = userCollection.find_one({"username": username})
#     return finding_user_name is not None
#
#
# # COOKIE/TOKEN RELATED
# def create_access_token(username: str):
#     access_token_expires = timedelta(seconds=int(ACCESS_TOKEN_EXPIRE_SECONDS))
#     data = {"username": username, "exp": datetime.utcnow() + access_token_expires}
#     to_encode = data.copy()
#     access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return access_token
#
#
# def create_temporary_token(email: str, first_name: str, last_name: str):
#     access_token_expires = timedelta(seconds=int(TEMPORARY_TOKEN_EXPIRE_MINUTES)*60)
#     data = {"email": email, "first_name": first_name, "last_name": last_name, "exp": datetime.utcnow() + access_token_expires}
#     to_encode = data.copy()
#     access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return access_token
#
#
# def set_auth_token(access_token: str, response: Response):
#     response.set_cookie(key="auth_token", value=access_token, httponly=True, max_age=ACCESS_TOKEN_EXPIRE_SECONDS)
#
#
# def set_temporary_token(temporary_access_token: str, response: Response):
#     response.set_cookie(key="temporary_token", value=temporary_access_token, httponly=True, max_age=TEMPORARY_TOKEN_EXPIRE_MINUTES*60)
#
#
# def delete_auth_token(response: Response):
#     expires = datetime.utcnow() + timedelta(seconds=1)
#     response.set_cookie(
#         key="auth_token",
#         value="",
#         httponly=True,
#         expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
#     )
#     return True
#
#
# def delete_temporary_token(response: Response):
#     expires = datetime.utcnow() + timedelta(seconds=1)
#     response.set_cookie(
#         key="temporary_token",
#         value="",
#         httponly=True,
#         expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
#     )
#     return True
#
#
# def check_auth_token(auth_token: str):
#     if auth_token is None:
#         return None
#     try:
#         payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("username")
#         if username is None:
#             return None
#     except JWTError:
#         return None
#     if not check_if_username_exists(username):
#         return None
#     return username
#
#
# def check_temporary_token(temporary_token: str):
#     if temporary_token is None:
#         return None
#     try:
#         payload = jwt.decode(temporary_token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("email")
#         first_name: str = payload.get("first_name")
#         last_name: str = payload.get("last_name")
#         if email is None or first_name is None or last_name is None:
#             return None
#     except JWTError:
#         return None
#     return {"email": email, "first_name": first_name, "last_name": last_name}
#
#
# # ADD USER/INFO TO DB
# def add_user_default(username: str, email: str, password: str):
#     if check_if_username_exists(username):
#         logger.create_error_log('User creation failed as the username {} was taken '.format(username))
#         raise HTTPException(status_code=409, detail="Username already taken.")
#     if check_if_email_exists(email):
#         logger.create_error_log('User creation failed as the email: {} was taken '.format(email))
#         raise HTTPException(status_code=409, detail="Email already taken.")
#     errors = regex_check.check_values(email=email, username=username, password=password)
#     if not len(errors) == 0:
#         logger.create_error_log('User creation failed due to invalid input data')
#         raise HTTPException(status_code=400, detail=errors)
#     user = {"username": username, "email": email, "password": hash_password(password), "accountInformation": {},
#             "displayInformation": {}, "socialConnections": {}, "campaignsCreated": [], "campaignsFunded": [],
#             "provider": "false"}
#     # _id = userCollection.insert_one(dict(user))
#     # user = users_serializer(userCollection.find({"_id": _id.inserted_id}))
#     # logger.create_info_log('Created user: {} - {} -'.format(user[0].get("username"), user[0].get("email")))
#     # return user[0]
#     # user = {"username": username, "email": email, "password": hash_password(password), "provider": "false"}
#     _id = userCollection.insert_one(dict(user))
#     user = userCollection.find_one({"_id": _id.inserted_id}, {'_id': 0})
#     logger.create_info_log('Created user: {} - {} -'.format(user.get("username"), user.get("email")))
#     return user
#
#
# def add_user_provider(username: str, temporary_token: str):
#     user_data = check_temporary_token(temporary_token)
#     if user_data is None:
#         return None
#     if check_if_username_exists(username):
#         logger.create_error_log('User creation failed as the username {} was taken '.format(username))
#         raise HTTPException(status_code=409, detail="Username already taken.")
#     if check_if_email_exists(user_data["email"]):
#         logger.create_error_log('User creation failed as the email: {} was taken '.format(user_data["email"]))
#         raise HTTPException(status_code=409, detail="Email already taken.")
#     errors = regex_check.check_values_provider(email=user_data["email"], username=username)
#     if not len(errors) == 0:
#         logger.create_error_log('User creation failed due to invalid input data')
#         raise HTTPException(status_code=400, detail=errors)
#     account_info = {"firstName": user_data["first_name"], "lastName": user_data["last_name"]}
#     user = {"username": username, "email": user_data["email"], "password": "", "accountInformation": account_info,
#             "displayInformation": {}, "socialConnections": {}, "campaignsCreated": [], "campaignsFunded": [],
#             "provider": "true"}
#     # _id = userCollection.insert_one(dict(user))
#     # user = users_serializer(userCollection.find({"_id": _id.inserted_id}))
#     # logger.create_info_log('Created user: {}'.format(user[0].get("email")))
#     # return user[0]
#     # user = {"username": username, "email": user_data["email"], "password": "", "accountInformation": account_info,
#     #         "provider": "true"}
#     _id = userCollection.insert_one(dict(user))
#     user = userCollection.find_one({"_id": _id.inserted_id}, {'_id': 0})
#     logger.create_info_log('Created user: {}'.format(user.get("email")))
#     return user
#
#
#
# # AUTHENTICATION
# def authenticate_user_default(email: str, password: str):
#     if not check_if_email_exists(email):
#         return None
#     user = get_user_email(email)
#     hashed_password = user.get("password")
#     if not verify_password(password, hashed_password):
#         raise credentials_exception
#     return user
#
#
# def authenticate_user_provider(email: str):
#     if not check_if_email_exists(email):
#         return None
#     return get_user_email(email)
#
#
# # Get User From DB
# def get_user_email(email: str):
#     # user = users_serializer(userCollection.find({"email": email}))
#     # if len(user) == 0:
#     #     logger.create_error_log('Not able to get the user'.format(email))
#     #     raise HTTPException(status_code=404, detail="No user with the email exists.")
#     # return user[0]
#     user = userCollection.find_one({"email": email}, {'_id': 0})
#     if user is None:
#         logger.create_error_log('Not able to get the user'.format(email))
#         raise HTTPException(status_code=404, detail="No user with the email exists.")
#     return user
#
#
# def get_user_username(username: str):
#     # user = users_serializer(userCollection.find({"username": username}))
#     # if len(user) == 0:
#     #     logger.create_error_log('Not able to get the user'.format(username))
#     #     raise HTTPException(status_code=404, detail="No user with the username exists.")
#     # return user[0]
#     user = userCollection.find_one({"username": username}, {'_id': 0})
#     if user is None:
#         logger.create_error_log('Not able to get the user'.format(username))
#         raise HTTPException(status_code=404, detail="No user with the username exists.")
#     return user
#
#
# def get_user_object_id_from_username(username: str):
#     user = userCollection.find_one({"username": username})
#     if user is None:
#         return None
#     return str(user["_id"])
