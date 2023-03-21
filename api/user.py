from fastapi import HTTPException, status, APIRouter, UploadFile, File, Form, Depends
from config.db import user_collection
from bson.objectid import ObjectId
from utils.user_utils import add_user_to_db, add_username_to_user_data, delete_user_from_db, get_user_from_user_id, check_if_username_exists
from models.user import UserResponse
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
# from models.user import User, SignUpUserResponse, UserResponse
from utils import regex_check
from log import logger
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

index="/api/v1"

@router.post("/user")
def add_user(uid: str, email: str):
    logger.info(f"{index}/user Api Called . Adding User with id :{uid} , email:{email}")
    user_id = add_user_to_db(email, uid)
    logger.debug("User Added To Db with id :{user_id}")
    logger.debug(f"{index}/user Api Executed")
    return user_id


@router.post("/username")
def add_username(uid: str, username: str):
    logger.info(f"{index}/username Api Called . Adding Username  with id :{uid} , name:{username}")
    add_username_to_user_data(username, uid)
    logger.debug("Username Added to db succesfully")
    logger.debug(f"{index}/username Api Execuetd")    
    return {"exists": False, "updated_db": True}
    # return "Added username Successfully"


@router.delete("/user/{user_id}")
def delete_user(user_id: str):
    logger.info(f"{index}/user/{user_id} Api Called . Deleting User with id :{user_id}")
    delete_user_from_db(user_id)
    logger.debug(f"User with id:{user_id} deleted succesfully ")
    logger.debug(f"{index}/user/{user_id} Api Executed")
    return "Deleted Successfully"


@router.get("/is-username-taken/{username}")
def is_username_valid(username: str):
    logger.info(f"{index}/is-username-taken/{username} Api Called . Checking username is taken for username:{username}")
    is_present = check_if_username_exists(username)
    if is_present:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken.")
    logger.debug(f"No match found for username:{username}")
    logger.debug(f"{index}/is-username-taken/{username} Api Executed")
    return "Username available."


@router.get("/current-user", response_model=UserResponse)
async def get_current_user(session: SessionContainer = Depends(verify_session())):
    logger.info(f"{index}/current-user Api Called . For Getting current user ")
    if session is None:
        return credentials_exception
    user_id = session.get_user_id()
    logger.debug(f"User found with userid:{user_id}")
    user = get_user_from_user_id(user_id)
    logger.debug(f"{index}/current-user Api Executed")
    return user

# from supertokens_python.recipe.session.asyncio import get_session_information, merge_into_access_token_payload
# async def get_custom_payload_value(handle, key):
#     session_information = await get_session_information(handle)
#     current_access_token_payload = session_information.access_token_payload
#     custom_claim_value = current_access_token_payload[key]
#     return custom_claim_value


@router.get("/check-username")
def check_if_username_is_present(session: SessionContainer = Depends(verify_session())):
    logger.info(f"{index}/check-username Api called . Checking username is present in payload or not")
    username_present = session.access_token_payload["username_bool"]
    logger.debug(f"Username Checked Succesfully in payload")
    logger.debug(f"{index}/current-username Api Executed")
    return username_present
