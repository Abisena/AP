from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from connection.db import conection
from models.Users import User, UpdatePassword

app = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = conection()

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post('/register')
async def register(request: User):
    user_data = db['Auth'].find_one({'email': request.email})

    if user_data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(request.password)
    role = "admin" if db['Auth'].count_documents({}) == 0 else "user"
    
    data_regis = {
        'email': request.email,
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
    user_data = db['Auth'].find_one({'email': request.email})

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


@app.put('/update_password')
async def update_password(request: UpdatePassword):
    user_data = db['Auth'].find_one({'email': request.email})

    if user_data:
        if pwd_context.verify(request.old_password, user_data['password']):
            hashed_new_password = get_password_hash(request.new_password)
            db['Auth'].update_one({'email': request.email}, {'$set': {'password': hashed_new_password}})
            return {'message': 'Password updated successfully'}
        else:
            raise HTTPException(status_code=400, detail='Password lama salah!')
    else:
        raise HTTPException(status_code=404, detail='Email tidak ditemukan!')