# import yaml
# from fastapi import HTTPException, APIRouter
# from starlette.requests import Request
# from fastapi_sso.sso.google import GoogleSSO
# from fastapi.responses import RedirectResponse
# from utils.auth_utils import authenticate_user_provider, create_access_token, set_auth_token, create_temporary_token, set_temporary_token
#
# global patterns
# with open('items.yaml') as f:
#         patterns = yaml.load(f, Loader=yaml.FullLoader)
# router = APIRouter()
#
# GOOGLE_CLIENT_ID = patterns.get('google_client_id') or None
# GOOGLE_CLIENT_SECRET = patterns.get('google_client_secret') or None
# if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
#     raise BaseException('Missing env variables')
#
#
# google_sso = GoogleSSO(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, "http://localhost:8000/google/redirect")
#
#
# @router.get("/google/authenticate")
# async def google_oauth():
#     """Generate login url and redirect"""
#     return await google_sso.get_login_redirect()
#
#
# @router.get("/google/redirect")
# async def google_oauth_redirect(request: Request):
#     """Process login response from Google and return user info"""
#     user = await google_sso.verify_and_process(request)
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
