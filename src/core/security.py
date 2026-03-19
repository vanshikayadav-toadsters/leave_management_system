from jose import jwt, JWTError
from datetime import datetime , timedelta

class JWTManager:
    def __init__(
            self,
            secret_key:str,
            algorithm:str,
            access_expiry_minutes:int,
            refresh_expiry_days:int
    ):
        self.secret_key=secret_key
        self.algorithm=algorithm
        self.access_expiry_minutes=access_expiry_minutes
        self.refresh_expiry_days=refresh_expiry_days


def create_access_token(self,data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow() + timedelta(
        minutes=self.access_expiry_minutes
    )

    to_encode.update({"exp":expire , "type":"access"})

    return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)


def create_refresh_token(self,data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow + timedelta(
        days=self.refresh_expiry_days
    )

    to_encode.update({"exp":expire, "type":"refresh"})

    return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

def decode_token(self , token:str):
    try:
        payload=jwt.decode(
            token,
            self.secret_key,
            algorithm=self.algorithm
        )

        return payload
    
    except JWTError:
        raise Exception("Invalid or expired token ")
