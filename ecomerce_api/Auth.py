from fastapi import APIRouter, HTTPException, Depends, status
from passlib.context import CryptContext
from connection.db import conection
from models.Users import User, UpdatePassword, Token
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

app = APIRouter()

SECRET_KEY = "ecomerce"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = conection()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return email

def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = db['Auth'].find_one({'username': form_data.username})

    if user_data:
        if verify_password(form_data.password, user_data['password']):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": form_data.username}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
    else:
        raise HTTPException(status_code=404, detail="Email not found")
    

@app.post('/register')
async def register(request: User):
    user_data = db['Auth'].find_one({'username': request.Username})

    if user_data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(request.password)
    role = "admin" if db['Auth'].count_documents({}) == 0 else "user"
    
    data_regis = {
        'username': request.Username,
        'password': hashed_password,
        'role': role
    }
    
    try:
        db['Auth'].insert_one(data_regis)
        return {"message": "Registration successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/login')
async def login(request: User):
    user_data = db['Auth'].find_one({'username': request.Username})

    if user_data:
        role = user_data.get('role', 'user')
        if pwd_context.verify(request.password, user_data['password']):
            if role == 'admin':
                return {'message': f'Selamat, Anda adalah seorang {role}!'}
            else:
                return {'message': f'Selamat, Anda adalah seorang {role}!'}
        else:
            raise HTTPException(status_code=400, detail='Password salah!')
    else:
        raise HTTPException(status_code=404, detail='Email tidak ditemukan!')
    
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    user_data = db['Auth'].find_one({'username': current_user})
    if user_data:
        return User(**user_data)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.put('/update_password')
async def update_password(request: UpdatePassword):
    user_data = db['Auth'].find_one({'username': request.Username})

    if user_data:
        if pwd_context.verify(request.old_password, user_data['password']):
            hashed_new_password = get_password_hash(request.new_password)
            db['Auth'].update_one({'username': request.email}, {'$set': {'password': hashed_new_password}})
            return {'message': 'Password updated successfully'}
        else:
            raise HTTPException(status_code=400, detail='Password lama salah!')
    else:
        raise HTTPException(status_code=404, detail='Email tidak ditemukan!')