# from fastapi import Response, APIRouter, HTTPException
# from models import user as user_model
# from utils.auth_utils import authenticate_user_default, create_access_token, set_auth_token, add_user_default
#
# router = APIRouter()
#
#
# @router.post("/email/login", response_model=user_model.UserResponse)
# async def email_login(user: user_model.LoginUser, response: Response):
#     login_user = authenticate_user_default(user.email, user.password)
#     if login_user is None:
#         raise HTTPException(status_code=404, detail="Not registered.")
#     access_token = create_access_token(login_user["username"])
#     set_auth_token(access_token, response)
#     return login_user
#
#
# @router.post("/sign-up", response_model=user_model.UserResponse)
# async def sign_up(user: user_model.User, response: Response):
#     created_user = add_user_default(user.username, user.email, user.password)
#     access_token = create_access_token(user.username)
#     set_auth_token(access_token, response)
#     return created_user
