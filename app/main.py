import json
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from . import config
from cassandra.cqlengine.management import sync_table
from app.users.models import User
# from .db import BASE_DIR, ASTRADB_CONNECT_BUNDLE
from app.db import get_session
import os
from pydantic.error_wrappers import ValidationError
import pathlib
from app.users.schema import UserSignUpSchema, UserLoginSchema
from app.utilis import validate_schema_or_errors


BASE_DIR = pathlib.Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR/'templates'

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app = FastAPI()

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'
@app.on_event('startup')
def on_startup():
    # print(BASE_DIR)
    get_session()
    session = get_session()
    sync_table(User)
    if row := session.execute("select release_version from system.local").one():
        print('nice one')
    else:
        print("An error occurred.")
    
    print('Hello world')

@app.get('/', response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        'request': request,
        'abc': 123
    }
    return templates.TemplateResponse('home.html', context)

@app.get('/list')
def listView():
    obj = User.objects.all()
    return list(obj)

@app.get('/login', response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        'request': request,
        'abc': 123
    }
    return templates.TemplateResponse('form.html', context)

@app.post('/login', response_class=HTMLResponse)
def homepage(request: Request, email: str = Form(...), password: str = Form(...)):
    print(email, password)
    context = {
        'request': request,
        'abc': 123
    }
    return templates.TemplateResponse('form.html', context)

@app.get('/signup', response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        'request': request,
        'abc': 123
    }
    return templates.TemplateResponse('signup.html', context)

@app.post('/signup', response_class=HTMLResponse)
def signupView(request: Request, email: str = Form(...), 
               password: str = Form(...),
               confirm_password: str = Form(...)
               ):
    print(confirm_password)
    raw_data = {
        'email': email,
        'password': password,
        'password_confirm': confirm_password
    }
    # print(raw_data)

    data, errors, password = validate_schema_or_errors(raw_data= raw_data, schema_model= UserSignUpSchema)

    if not errors:
        validated_email = data['email']
        validated_password = password
        User.create_user(email=email, password=password)
    context = {
        'request': request,
        'data': data,
        'errors': errors,
    }
    return templates.TemplateResponse('signup.html', context)

@app.get('/signin', response_class=HTMLResponse)
def SignInVeiw(request: Request):
    context = {
        'request': request,
        'abc': 123
    }
    return templates.TemplateResponse('signin.html', context)

@app.post('/signin', response_class=HTMLResponse)
def signInView(request: Request, email: str = Form(...), 
             password: str = Form(...), 
             ):

    raw_data = {
        'email': email,
        'password': password,
        
    }

    data, errors, _ = validate_schema_or_errors(raw_data= raw_data, schema_model= UserLoginSchema)
    context = {
        'request': request,
        'data': data,
        'errors': errors,
    }
    return templates.TemplateResponse('signin.html', context)
