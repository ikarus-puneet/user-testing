# from fastapi import HTTPException, status, Response, Cookie, APIRouter
# from typing import Optional
# from utils.auth_utils import add_user_provider, check_auth_token, get_user_username, delete_auth_token, delete_temporary_token, create_access_token, set_auth_token
# from models import user as user_model
#
# router = APIRouter()
# credentials_exception = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
# )
#
#
# @router.get("/get-current-user", response_model=user_model.UserResponseForToken)
# def get_current_user(auth_token: Optional[str] = Cookie(None)):
#     if auth_token is None:
#         return {}
#     username = check_auth_token(auth_token)
#     if username is None:
#         return {}
#     user = get_user_username(username)
#     return user
#
#
# @router.get("/logout")
# def logout(response: Response):
#     delete_auth_token(response)
#     return "Logged Out Successfully"
#
#
# @router.get("/check-temporary-token")
# def check_temporary_token(temporary_token: Optional[str] = Cookie(None)):
#     if temporary_token is None or check_temporary_token(temporary_token) is None:
#         raise credentials_exception
#     return "Verified"
#
#
# @router.post("/add-username")
# def add_username(username_data: dict, response: Response, temporary_token: Optional[str] = Cookie(None)):
#     if temporary_token is None:
#         raise credentials_exception
#     temporary_token_value = temporary_token
#     delete_temporary_token(response)
#     user = add_user_provider(username_data["username"], temporary_token_value)
#     if user is None:
#         raise credentials_exception
#     access_token = create_access_token(user["username"])
#     set_auth_token(access_token, response)
#     return user
