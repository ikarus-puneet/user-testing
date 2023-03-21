from fastapi import HTTPException, status, UploadFile, File
from passlib.context import CryptContext
from config.db import userCollection, notification_collection
from utils import regex_check
from utils.user_utils import get_user_from_user_id
from log import logger
from pyuploadcare.client import Uploadcare
# import yaml
from starlette.background import BackgroundTasks
import os
from bson.objectid import ObjectId
from config import read_yaml
import boto3

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
#     patterns = yaml.load(f, Loader=yaml.FullLoader)

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = patterns.get('secret_key') or None
# ALGORITHM = patterns.get('algorithm') or None
# ACCESS_TOKEN_EXPIRE_MINUTES = patterns.get('access_token_expire_minutes') or None
# ACCESS_TOKEN_EXPIRE_SECONDS = patterns.get('access_token_expire_seconds') or None
# TEMPORARY_TOKEN_EXPIRE_MINUTES = patterns.get('temporary_token_expire_minutes') or None
# UPLOADCARE_PUBLIC_KEY = patterns.get('uploadcare_public_key') or None
# UPLOADCARE_SECRET_KEY = patterns.get('uploadcare_secret_key') or None
# if SECRET_KEY is None or ALGORITHM is None or ACCESS_TOKEN_EXPIRE_MINUTES is None or ACCESS_TOKEN_EXPIRE_SECONDS is None or UPLOADCARE_PUBLIC_KEY is None or UPLOADCARE_SECRET_KEY is None:
#     raise BaseException('Missing env variables')

# credentials_exception = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
# )


def add_my_profile_data(data: dict, user_id: str):
    # username = auth_utils.check_auth_token(auth_token)
    # if username is None:
    #     return None
    # user = auth_utils.get_user_username(username)
    # if len(user) == 0:
    #     logger.create_error_log('Not able to get the user'.format(username))
    #     raise HTTPException(status_code=404, detail="No user with the username exists.")
    logger.info(f"Calling Function for adding profile database for userid:{user_id}")
    user = get_user_from_user_id(user_id)
    new_display_information = dict()
    if "displayInformation" in user.keys():
        new_display_information = user["displayInformation"]
    new_display_information["description"] = data["displayInformationData"]["description"]
    user.update({"email": data["email"], "accountInformation": data["accountInformationData"],
                 "displayInformation": new_display_information, "socialConnections": data["socialConnectionsData"]})
    userCollection.find_one_and_update({"_id": ObjectId(user_id)}, {
        "$set": dict(user)
    })
    logger.debug(f"Profile Data added to db for userid:{user_id}")
    return user


def add_profile_and_cover_pictures(picture: UploadFile, cropped_picture: UploadFile, picture_type: str, name: str, user_id: str, background_tasks: BackgroundTasks):
    # username = auth_utils.check_auth_token(auth_token)
    # if username is None:
    #     return None
    # user = auth_utils.get_user_username(username)
    # if len(user) == 0:
    #     logger.create_error_log('Not able to get the user'.format(username))
    #     raise HTTPException(status_code=404, detail="No user with the username exists.")
    user = get_user_from_user_id(user_id)
    logger.info(f"Calling function for adding profile and cover pictures for user:{user}")
    if picture_type == "profile picture":
        new_display_information = dict()
        if "displayInformation" in user.keys():
            new_display_information = user["displayInformation"]
        old_pictures = []
        if "profilePicture" in new_display_information.keys():
            old_pictures.append(new_display_information["profilePicture"]["pictureUrl"])
            old_pictures.append(new_display_information["profilePicture"]["croppedPictureUrl"])
        profile_picture = dict()
        profile_picture["pictureUrl"] = upload_picture_to_uploadcare(picture, f"{name}-profile-picture", background_tasks)
        profile_picture["croppedPictureUrl"] = upload_picture_to_uploadcare(cropped_picture, f"{name}-cropped-profile-picture", background_tasks)
        new_display_information["profilePicture"] = profile_picture
        userCollection.find_one_and_update({"_id": ObjectId(user_id)}, {
            "$set": {"displayInformation": new_display_information}
        })
        if len(old_pictures) > 0:
            delete_pictures_from_uploadcare(old_pictures)
        logger.debug(f"Picture added to db for user:{user}")    
        return profile_picture
    elif picture_type == "cover picture":
        new_display_information = dict()
        
        if "displayInformation" in user.keys():
            new_display_information = user["displayInformation"]
        old_pictures = []
        if "coverPicture" in new_display_information.keys():
            old_pictures.append(new_display_information["coverPicture"]["pictureUrl"])
            old_pictures.append(new_display_information["coverPicture"]["croppedPictureUrl"])
        cover_picture = dict()
        cover_picture["pictureUrl"] = upload_picture_to_uploadcare(picture, f"{name}-cover-picture", background_tasks)
        cover_picture["croppedPictureUrl"] = upload_picture_to_uploadcare(cropped_picture, f"{name}-cropped-cover-picture", background_tasks)
        new_display_information["coverPicture"] = cover_picture
        userCollection.find_one_and_update({"_id": ObjectId(user_id)}, {
            "$set": {"displayInformation": new_display_information}
        })
        logger.debug(f"Picture added to db for user:{user}")
        if len(old_pictures) > 0:
            delete_pictures_from_uploadcare(old_pictures)
        return cover_picture
    else:
        return None


def change_cropped_picture_util(cropped_picture: UploadFile, picture_type: str, name: str, user_id: str, background_tasks: BackgroundTasks):
    # username = auth_utils.check_auth_token(auth_token)
    # if username is None:
    #     return None
    # user = auth_utils.get_user_username(username)
    # if len(user) == 0:
    #     logger.create_error_log('Not able to get the user'.format(username))
    #     raise HTTPException(status_code=404, detail="No user with the username exists.")
    user = get_user_from_user_id(user_id)
    logger.info(f"Calling function for adding croped picture for user:{user}")
    if picture_type == "profile picture":
        new_display_information = user["displayInformation"]
        old_pictures = []
        if "profilePicture" in new_display_information.keys():
            old_pictures.append(new_display_information["profilePicture"]["croppedPictureUrl"])
        profile_picture = dict()
        profile_picture["pictureUrl"] = user["displayInformation"]["profilePicture"]["pictureUrl"]
        profile_picture["croppedPictureUrl"] = upload_picture_to_uploadcare(cropped_picture, f"{name}-cropped-profile-picture", background_tasks)
        new_display_information["profilePicture"] = profile_picture
        userCollection.find_one_and_update({"_id": ObjectId(user_id)}, {
            "$set": {"displayInformation": new_display_information}
        })
        logger.debug(f"Cropped picture added to db for user:{user}")
        if len(old_pictures) > 0:
            delete_pictures_from_uploadcare(old_pictures)
        return profile_picture
    elif picture_type == "cover picture":
        new_display_information = user["displayInformation"]
        old_pictures = []
        if "coverPicture" in new_display_information.keys():
            old_pictures.append(new_display_information["coverPicture"]["croppedPictureUrl"])
        cover_picture = dict()
        cover_picture["pictureUrl"] = user["displayInformation"]["coverPicture"]["pictureUrl"]
        cover_picture["croppedPictureUrl"] = upload_picture_to_uploadcare(cropped_picture, f"{name}-cropped-cover-picture", background_tasks)
        new_display_information["coverPicture"] = cover_picture
        userCollection.find_one_and_update({"_id": ObjectId(user_id)}, {
            "$set": {"displayInformation": new_display_information}
        })
        logger.debug(f"Cropped picture added to db for user:{user}")
        if len(old_pictures) > 0:
            delete_pictures_from_uploadcare(old_pictures)
        return cover_picture
    else:
        return None


def upload_picture_to_uploadcare(picture: UploadFile, name: str, background_tasks: BackgroundTasks):
    logger.info(f"Calling Function for uploading in uploadcare of name:{name}")
    contents = picture.file.read()
    with open(f"temp/{name}.jpeg", 'wb') as f:
        f.write(contents)
    uploadcare = Uploadcare(public_key=read_yaml.uploadcare_public_key, secret_key=read_yaml.uploadcare_secret_key)
    with open(f"temp/{name}.jpeg", 'rb') as created_picture:
        uploaded_picture: File = uploadcare.upload(created_picture)
    background_tasks.add_task(delete_created_picture, f"temp/{name}.jpeg")
    print("uuid", uploaded_picture.uuid)
    logger.debug(f"Picture uploaded to uploadcare with id:{uploaded_picture.uuid}")
    return f"https://ucarecdn.com/{uploaded_picture.uuid}/"


def delete_created_picture(path: str) -> None:
    logger.info("Deleting file from local environment")
    os.unlink(path)
    logger.debug("Picture deleted from local")

def delete_pictures_from_uploadcare(pictures_list: list):
    uuid_list = list()
    logger.info(f"Calling Function for deleting from uploadcare ")
    for picture_url in pictures_list:
        uuid = picture_url.removeprefix('https://ucarecdn.com/').removesuffix('/')
        uuid_list.append(uuid)
    uploadcare = Uploadcare(public_key=read_yaml.uploadcare_public_key, secret_key=read_yaml.uploadcare_secret_key)
    uploadcare.delete_files(uuid_list)
    logger.debug("Picture deleted from uploadcare")
    return "Deleted"


def upload_video_to_s3(video: bytes, name: str, user_id: str):
    client = boto3.Session(
        aws_access_key_id=read_yaml.AWS_access_key,
        aws_secret_access_key=read_yaml.AWS_secret_key
    )
    logger.info("Calling function for uploading video in s3")
    s3 = client.resource('s3')
    aws_bucket = s3.Bucket(read_yaml.AWS_bucket)
    print("uploading")
    try:
        aws_bucket.put_object(Key=name, Body=video)
        logger.debug(f"Asset uploaded to s3 with name:{name}")
    except Exception as e:
        raise e
    url = f"https://nest-user-test.s3.ap-south-1.amazonaws.com/{name}"
    userCollection.find_one_and_update({"_id": ObjectId(user_id)}, {
        "$set": {"displayInformation.video": url}
    })
    logger.debug(f"Asset info added in db")
    return url


def change_notifications_util(data: dict, user_id: str):
    # username = auth_utils.check_auth_token(auth_token)
    # if username is None:
    #     return None
    # user = userCollection.find_one({"username": username})
    # if user is None:
    #     return None
    # userid = auth_utils.get_user_object_id_from_username(username)
    # if userid is None:
    #     return None
    logging.info(f"Calling Function for changing notifications info for userid:{user_id}")
    notification = notification_collection.find_one({"userId": user_id}, {'_id': 0})
    if notification is None:
        new_notification = {"notificationData": data, "userId": user_id}
        notification_collection.insert_one(new_notification)
        logging.debug(f"Notifications info changed for userid:{user_id}")
        return new_notification["notificationData"]
    else:
        notification.update({"notificationData": data})
        notification_collection.find_one_and_update({"userId": user_id}, {
            "$set": dict(notification)
        })
        logging.debug(f"Notifications info changed for userid:{user_id}")
        return notification["notificationData"]


def get_notification_data(user_id: str):
    # username = auth_utils.check_auth_token(auth_token)
    # if username is None:
    #     return None
    # userid = auth_utils.get_user_object_id_from_username(username)
    # if userid is None:
    #     return None
    logging.info(f"Calling Function for getting notifications info for userid:{user_id}")
    notification = notification_collection.find_one({"userId": user_id}, {'_id': 0})
    if notification is None or notification["notificationData"] is None:
        return dict()
    logging.debug(f"Notifications data recieved for userid:{user_id}")
    return notification["notificationData"]


# def change_password_util(data: dict, auth_token: str):
#     username = auth_utils.check_auth_token(auth_token)
#     if username is None:
#         return None
#     user = auth_utils.get_user_username(username)
#     if len(user) == 0:
#         logger.create_error_log('Not able to get the user'.format(username))
#         raise HTTPException(status_code=404, detail="No user with the username exists.")
#     print("user", user)
#     if user["provider"] == "true":
#         print("in provider")
#         hashed_password = auth_utils.hash_password(data["newPassword"])
#         user.update({"password": hashed_password, "provider": "false"})
#         userCollection.find_one_and_update({"username": username}, {
#             "$set": dict(user)
#         })
#         return user
#     else:
#         print("in else")
#         if not auth_utils.verify_password(data["currentPassword"], user["password"]):
#             raise credentials_exception
#         hashed_password = auth_utils.hash_password(data["newPassword"])
#         user.update({"password": hashed_password})
#         userCollection.find_one_and_update({"username": username}, {
#             "$set": dict(user)
#         })
#         return user
