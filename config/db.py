from pymongo import MongoClient
import config.settings as settings

client = MongoClient(settings.mongodb_uri, settings.port)
db = client[settings.mongodb_user]

userCollection = db["user"]
user_collection = db["user"]
# userCollection2 = db["test2"]
# schema = {
#     '$jsonSchema': {
#         'required': ['username', 'email'],
#         'properties': {
#             "_id": {"bsonType": "objectId"},
#             'username': {'bsonType': 'string'},
#             'email': {'bsonType': 'string'},
#             'password': {'bsonType': 'string'},
#             "accountInformation": {
#                 "bsonType": "object",
#                 "required": ["firstName", "lastName"],
#                 "properties": {
#                     "firstName": {"bsonType": "string"},
#                     "lastName": {"bsonType": "string"},
#                     "dob": {"bsonType": "string"},
#                     "gender": {"bsonType": "string"},
#                     "country": {
#                         "bsonType": "object",
#                         "required": ["label", "value"],
#                         "properties": {
#                             "label": {"bsonType": "string"},
#                             "value": {"bsonType": "string"}
#                         }
#                     },
#                     "accountType": {
#                         "bsonType": "object",
#                         "required": ["label", "value"],
#                         "properties": {
#                             "label": {"bsonType": "string"},
#                             "value": {"bsonType": "string"}
#                         }
#                     },
#                     "preferredTools": {
#                         "bsonType": "array",
#                         "items": {
#                             "bsonType": "object",
#                             "properties": {
#                                 "label": {"bsonType": "string"},
#                                 "value": {"bsonType": "string"}
#                             }
#                         }
#                     },
#                     "areaOfExpertise": {
#                         "bsonType": "array",
#                         "items": {
#                             "bsonType": "object",
#                             "properties": {
#                                 "label": {"bsonType": "string"},
#                                 "value": {"bsonType": "string"}
#                             }
#                         }
#                     },
#                 }
#             },
#             "displayInformation": {
#                 "bsonType": "object",
#                 "properties": {
#                     "profilePicture": {
#                         "bsonType": "object",
#                         "required": ["pictureUuid", "croppedPictureUuid"],
#                         "properties": {
#                             "pictureUuid": {"bsonType": "string"},
#                             "croppedPictureUuid": {"bsonType": "string"}
#                         }
#                     },
#                     "coverPicture": {
#                         "bsonType": "object",
#                         "required": ["pictureUuid", "croppedPictureUuid"],
#                         "properties": {
#                             "pictureUuid": {"bsonType": "string"},
#                             "croppedPictureUuid": {"bsonType": "string"}
#                         }
#                     },
#                     "description": {"bsonType": "string"},
#                     "video": {"bsonType": "string"},
#                 }
#             },
#             "socialConnections": {
#                 "bsonType": "object",
#                 "properties": {
#                     "website": {"bsonType": "string"},
#                 }
#             },
#             'provider': {'bsonType': 'string'},
#         },
#         "additionalProperties": False
#     }
# }
#
# db.command('collMod', 'test2', validator=schema, validationLevel='moderate')

campaign_collection = db["campaigns"]
notification_collection = db["notifications"]
