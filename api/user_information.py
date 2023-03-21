from fastapi import HTTPException, status, APIRouter, UploadFile, File, Form, Depends
from models.user import UserResponse, PictureUrls
from utils.user_information_utils import add_my_profile_data, change_notifications_util, add_profile_and_cover_pictures, get_notification_data, change_cropped_picture_util, upload_video_to_s3
from starlette.background import BackgroundTasks
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from config import read_yaml

import logging

log_format= '[%(asctime)s] %(levelname)s:%(name)s %(message)s '
log_file= 'user.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



router = APIRouter()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)

index ="/api/v1"

@router.put("/profile-information", response_model=UserResponse)
def profile_information(data: dict, session: SessionContainer = Depends(verify_session())):
    logger.info(f"{index}/profile-information Api Called. For adding profile data")
    if session is None:
        return credentials_exception
    user_id = session.get_user_id()
    user = add_my_profile_data(data, user_id)
    if user is None:
        return
    logger.debug(f"Profile info for userid:{user_id} added succesfully")
    logger.debug(f"{index}/profile-information Api Executed")
    return user


@router.post("/upload-picture")
def upload_picture(background_tasks: BackgroundTasks, pictureType: str = Form(), name: str = Form(), picture: UploadFile = File(...), croppedPicture: UploadFile = File(...), session: SessionContainer = Depends(verify_session())):
    logger.info(f"{index}/upload-picture Api Called. For uploading picture")
    if session is None:
        return credentials_exception
    user_id = session.get_user_id()
    pictures = add_profile_and_cover_pictures(picture, croppedPicture, pictureType, name, user_id, background_tasks)
    if pictures is None:
        return
    logger.debug(f"picture for userid:{user_id} added succesfully")
    logger.debug(f"{index}/profile-information Api Executed")
    return pictures


@router.put("/change-picture")
def change_cropped_picture(background_tasks: BackgroundTasks, pictureType: str = Form(), name: str = Form(), croppedPicture: UploadFile = File(...), session: SessionContainer = Depends(verify_session())):
    logger.info(f"{index}/change-picture Api Called. For changing picture")
    if session is None:
        return credentials_exception
    user_id = session.get_user_id()
    pictures = change_cropped_picture_util(croppedPicture, pictureType, name, user_id, background_tasks)
    if pictures is None:
        return
    logger.debug(f"picture for userid:{user_id} changeded succesfully")
    logger.debug(f"{index}/change-picture Api Executed")
    return pictures


@router.post("/introductory-video")
async def upload_introductory_video(video: UploadFile = File(...), session: SessionContainer = Depends(verify_session())):
    logger.info(f"{index}/introductory-video Api Called. For uploading introductory video")
    if session is None:
        return credentials_exception
    user_id = session.get_user_id()
    data = await video.read()
    size = len(data)
    if size > read_yaml.video_size:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Maximum allowed video size is 50MB.")
    extension = video.filename.split('.')[-1]
    url = upload_video_to_s3(data, f"{user_id}/introductory-video/video.{extension}", user_id)
    logger.debug("Introductory video uploaded tpo s3 ")
    logger.debug(f"{index}/introductory-video Api Executed")
    return url


@router.post("/notifications-information")
def notifications_information(data: dict, session: SessionContainer = Depends(verify_session())):
    logger.info(f"{index}/notifications-information Api Called. For posting information of notification")
    if session is None:
        return credentials_exception
    user_id = session.get_user_id()
    notification_data = change_notifications_util(data, user_id)
    if notification_data is None:
        return credentials_exception
    logger.debug("Notification Information Posted")
    logger.debug(f"{index}/notifications-information Api Executed")
    return notification_data

@router.get("/notification-data")
def notification_data(session: SessionContainer = Depends(verify_session())):
    logger.info(f"{index}/notifications-data Api Called. Forgetting information of notification")
    if session is None:
        return credentials_exception
    user_id = session.get_user_id()
    notification_data = get_notification_data(user_id)
    if notification_data is None:
        return credentials_exception
    logger.debug("Notification Information recieved")
    logger.debug(f"{index}/notifications-data Api Executed")
    return notification_data


# @router.put("/change-password", response_model=UserResponse)
# def change_password(data: dict, auth_token: Optional[str] = Cookie(None)):
#     user = change_password_util(data, auth_token)
#     if user is None:
#         return
#     return user


# @router.get("/user/{username}")
# def get_user_details(username):
#     print("here", username)
#     user = get_user_username(username)
#     print("user", user)
#     if user is None:
#         return HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Could not find user with username {username}",
#     )
#     return user