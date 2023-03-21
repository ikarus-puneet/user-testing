from pydantic import BaseModel


class PictureUrls(BaseModel):
    pictureUrl: str
    croppedPictureUrl: str


class AccountInformationClass(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    dob: str | None = None
    gender: str | None = None
    country: dict | None = None
    accountType: dict | None = None
    preferredTools: list | None = None
    areaOfExpertise: list | None = None


class DisplayInformationClass(BaseModel):
    profilePicture: PictureUrls | None = None
    coverPicture: PictureUrls | None = None
    description: dict | None = None
    video: str | None = None


class SocialConnectionsClass(BaseModel):
    website: str | None = None
    instagram: str | None = None
    facebook: str | None = None
    artStation: str | None = None
    behance: str | None = None


class UserResponse(BaseModel):
    username: str | None = None
    email: str
    accountInformation: AccountInformationClass | None = None
    displayInformation: DisplayInformationClass | None = None
    socialConnections: SocialConnectionsClass | None = None


# class User(BaseModel):
#     username: str | None = None
#     email: str
#     accountInformation: AccountInformationClass | None = None
#     displayInformation: DisplayInformationClass | None = None
#     socialConnections: SocialConnectionsClass | None = None


# class SignUpUserResponse(User):
#     username: str | None = None
#
#
# class UserResponse(User):
#     username: str


# class User(UserResponse):
#     password: str


# class PasswordUpdate(BaseModel):
#     current_password: str
#     new_password: str


# class LoginUser(BaseModel):
#     email: str
#     password: str


# class UserResponseForToken(BaseModel):
#     username: str | None = None
#     email: str | None = None
#     accountInformation: dict | None = None
#     displayInformation: dict | None = None
#     socialConnections: dict | None = None
#     provider: str | None = None
