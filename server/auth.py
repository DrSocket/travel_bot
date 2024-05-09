import os
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from models import UserIdentity
from dotenv import load_dotenv
load_dotenv()

PUBLIC_SUPABASE_URL=os.getenv('PUBLIC_SUPABASE_URL')
PUBLIC_SUPABASE_ANON_KEY=os.getenv('PUBLIC_SUPABASE_ANON_KEY')
PRIVATE_SUPABASE_SERVICE_ROLE=os.getenv('PRIVATE_SUPABASE_SERVICE_ROLE')
PRIVATE_STRIPE_API_KEY='REPLACE_ME'
SECRET_KEY=os.getenv('SECRET_KEY')

ALGORITHM = "HS256"


def decode_access_token(token: str) -> UserIdentity:
    # print ('Decoding token')
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_aud": False}
        )
        # print(f'Payload: {payload}')
    except JWTError as e:
        # print ('Error decoding token', e)
        return None # pyright: ignore reportPrivateUsage=none

    return UserIdentity(
        email=payload.get("email"),
        id=payload.get("sub"), # pyright: ignore reportPrivateUsage=none
    )


def verify_token(token: str):
    payload = decode_access_token(token)
    # print(f'Verifying token: {payload}')
    return payload is not None


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
    ):
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request
        )
        self.check_scheme(credentials)
        token = credentials.credentials  # pyright: ignore reportPrivateUsage=none
        # print(f'Authenticating token: {token}')
        return await self.authenticate(
            token,
        )

    def get_test_user(self) -> UserIdentity:
        return UserIdentity(
            email="test@example.com", id="696dda89-d395-4601-af3d-e1c66de3df1a" # type: ignore
        ) # replace with test user information
            
    def check_scheme(self, credentials):
        if credentials and credentials.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Token must be Bearer")
        elif not credentials:
            raise HTTPException(
                status_code=403, detail="Authentication credentials missing"
            )

    async def authenticate(
        self,
        token: str,
    ) -> UserIdentity:

        if os.environ.get("AUTHENTICATE") == "false":
            return self.get_test_user()
        elif verify_token(token):
            return decode_access_token(token)
        else:
            raise HTTPException(status_code=401, detail="Invalid token or api key.")

def get_current_user(user: UserIdentity = Depends(AuthBearer())) -> UserIdentity:
    return user
