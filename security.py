from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")

def hash_password(password: str):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def hash_token(token: str):
    return hashlib.sha256(token.encode('utf-8')).hexdigest()

def verify_password(plain_password,hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)