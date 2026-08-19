from passlib.context import CryptContext

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")
tkn_context = CryptContext(schemes="bcrypt", deprecated="auto")

def hash_password(password: str):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def hash_token(token: str):
    hashed_token = tkn_context.hash(token)
    return hashed_token

def verify_password(plain_password,hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)