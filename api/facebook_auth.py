# from fastapi import HTTPException, APIRouter
# from fastapi.requests import Request
# from fastapi_sso.sso.facebook import FacebookSSO
# from fastapi.responses import RedirectResponse
# from utils.auth_utils import authenticate_user_provider, create_access_token, set_auth_token, create_temporary_token, set_temporary_token
# import yaml
#
# global patterns
# with open('items.yaml') as f:
#         patterns = yaml.load(f, Loader=yaml.FullLoader)
# router = APIRouter()
#
# FACEBOOK_APP_ID = patterns.get('facebook_app_id') or None
# FACEBOOK_APP_SECRET = patterns.get('facebook_app_secret') or None
# if FACEBOOK_APP_ID is None or FACEBOOK_APP_SECRET is None:
#     raise BaseException('Missing env variables')
#
#
# facebook_sso = FacebookSSO(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, "http://localhost:8000/facebook/redirect")
#
#
# @router.get("/facebook/authenticate")
# async def facebook_oauth():
#     """Generate login url and redirect"""
#     return await facebook_sso.get_login_redirect()
#
#
# @router.get("/facebook/redirect")
# async def facebook_oauth_redirect(request: Request):
#     """Process login response from Google and return user info"""
#     user = await facebook_sso.verify_and_process(request)
#     if user is None:
#         raise HTTPException(401, "Failed to fetch user information")
#     verified_user = authenticate_user_provider(user.email)
#     if verified_user is None:
#         add_username_url = "http://localhost:3000/signup/username"
#         response = RedirectResponse(add_username_url, 303)
#         temporary_access_token = create_temporary_token(user.email, user.first_name, user.last_name)
#         set_temporary_token(temporary_access_token, response)
#         return response
#     access_token = create_access_token(verified_user["username"])
#     main_page_url = "http://localhost:3000"
#     response = RedirectResponse(main_page_url, 303)
#     set_auth_token(access_token, response)
#     return response