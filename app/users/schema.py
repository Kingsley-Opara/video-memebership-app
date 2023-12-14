from pydantic import BaseModel, EmailStr, SecretStr, validator
from app.users.models import User
from app.users.security import verify_hash

class UserSignUpSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr

    @validator('email')
    def validate_email_exists(cls, v, values, **kwargs):
        email = v
        queryset = User.objects.filter(email= email)
        if queryset.count() > 0:
            raise ValueError("Email is not avaliable.....try using another email")
        return email

    @validator('password_confirm')
    def password_match(cls, v, values, **kwargs):
        password = values.get("password")
        password_confirm = v
        # print(password, password_confirm)

        if password != password_confirm:
            raise ValueError("Passwords do not match")
        return password_confirm
    
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr

    @validator('email')
    def validate_email_exists(cls, v, values, **kwargs):
        email = v
        password = values.get('password')
        user = User.objects.filter(email = email)
        print(password)
        if user.count() != 1:
            raise ValueError('Invalid Email and Password')
        # if user.count() == 1:
        #     raw_password = password
        #     print(raw_password)
        return email
    
    # @validator('password')
    # def verify_password(cls, v, values, **kwargs):
    #     password = v
    #     email = values.get('email')
    #     user = User.objects.filter(email = email) or None
    #     if user.count() != 0  and user != None:
    #         user_password = user[0].password
    #         raw_password = password.get_secret_value()
    #         verified, msg = verify_hash(user_password, raw_password)
    #         if not verified:
    #             raise ValueError(msg)
    #     return password

    
    