from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api import google_auth, default_auth, facebook_auth, auth, user_information, user

from supertokens_python import init, InputAppInfo
from supertokens_python import SupertokensConfig
from supertokens_python.recipe import dashboard
from supertokens_python.recipe import usermetadata
from supertokens_python.recipe import userroles
from supertokens_python.recipe.thirdpartyemailpassword import Google, Facebook
from supertokens_python.recipe import thirdpartyemailpassword, session
from config import read_yaml

app = FastAPI()
# init()
init(
    app_info=InputAppInfo(
        app_name=read_yaml.app_name,
        api_domain=read_yaml.api_domain,
        website_domain=read_yaml.website_domain,
        api_base_path=read_yaml.base_path,
        website_base_path=read_yaml.base_path
    ),
    supertokens_config=SupertokensConfig(
        connection_uri=read_yaml.supertokens_core_uri,
        api_key=read_yaml.supertokens_core_api_key
    ),
    framework='fastapi',
    recipe_list=[
        session.init(),
        thirdpartyemailpassword.init(
            providers=[
                Google(
                    client_id=read_yaml.google_client_id,
                    client_secret=read_yaml.google_client_secret_key,
                    scope=[read_yaml.google_scope]
                )
                , Facebook(
                    client_id=read_yaml.facebook_client_id,
                    client_secret=read_yaml.facebook_client_secret_key
                )
            ]
        ),
        dashboard.init(api_key=read_yaml.user_management_dashboard_api_key),
        usermetadata.init(),
        userroles.init()
    ],
    mode='asgi'
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:3001', 'http://localhost:8000'],
  allow_credentials=True,
  allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
  # allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
)


# app.include_router(default_auth.router)
# app.include_router(google_auth.router)
# app.include_router(facebook_auth.router)
# app.include_router(auth.router)
app.include_router(user_information.router)
app.include_router(user.router)
