from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Секретный ключ (сгенерируй случайную строку!)
SECRET_KEY = "super-secret-key-change-me-be-be-be"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Токен будет жить 30 минут

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt