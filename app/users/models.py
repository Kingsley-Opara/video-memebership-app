from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
import uuid
from app.config import get_settings
from . import validators
from .security import *


settings = get_settings()

class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key = True)
    user_id = columns.UUID(primary_key= True, default= uuid.uuid1)
    password = columns.Text()


    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'User(email = {self.email}, user_id = {self.user_id})'
    
    def set_password(self, pw, commit=False):
        pw_hash = generate_hash(pw)
        self.password = pw_hash
        if commit:
            self.save()
        return True
    
    def verify_password(self, pw):
        pw_hash = self.password
        verified, msg= verify_hash(pw_hash, pw)
        return verified, msg


    # @staticmethod
    def create_user(email, password=None):
        user = User.objects.filter(email=email)
        if user.count() != 0:
            raise Exception('Ooops...A user has been created with this email')
        is_valid, msg, validated_email = validators._validate_email(email)
        if not is_valid:
            raise Exception(f'invalid_email: {msg}')
        obj = User(email = validated_email)
        obj.set_password(password)
        obj.save()
        return obj