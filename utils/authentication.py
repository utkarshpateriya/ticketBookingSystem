from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from config import USERNAME, PASSWORD

class AdminAuthentication:
    security = HTTPBasic()
    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        try:
            if cls.pwd_context.verify(plain_password, hashed_password):
                return True
        except Exception as e:
            print(e)
        finally:
            return False
    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def authenticate_user(cls, credentials: HTTPBasicCredentials = Depends(security)):
        if not (credentials.username == USERNAME and credentials.password == PASSWORD):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return True