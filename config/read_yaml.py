import yaml
with open('items.yaml', 'r') as file:
    values = yaml.safe_load(file)

email_condition = values['email_condition']
name_condition = values['name_condition']
username_condition = values['username_condition']
password_condition_expression = values['password_condition_expression']
dob_condition_expression = values['dob_condition_expression']

uploadcare_public_key = values['uploadcare_public_key']
uploadcare_secret_key = values['uploadcare_secret_key']

app_name = values["app_name"]
api_domain = values["api_domain"]
website_domain = values["website_domain"]
base_path = values["base_path"]

supertokens_core_api_key = values["supertokens_core_api_key"]
supertokens_core_uri = values["supertokens_core_uri"]

google_client_id = values["google_client_id"]
google_client_secret_key = values["google_client_secret_key"]
google_scope = values["google_scope"]

facebook_client_id = values["facebook_client_id"]
facebook_client_secret_key = values["facebook_client_secret_key"]

user_management_dashboard_api_key = values["user_management_dashboard_api_key"]

image_size = values["image_size"]
video_size = values["video_size"]

AWS_access_key = values["AWS_access_key"]
AWS_secret_key = values["AWS_secret_key"]
AWS_bucket = values["AWS_bucket"]
