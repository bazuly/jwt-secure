from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.users.auth.jwt import JWTHandler


class JWTBearer(HTTPBearer):
    def __init__(self, jwt_handler: JWTHandler):
        super(JWTBearer, self).__init__(auto_error=True)
        self.jwt_handler = jwt_handler

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if not credentials:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code"
            )

        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=403,
                detail="Invalid authentication scheme"
            )

        try:
            payload = await self.jwt_handler.verify_token(credentials.credentials, request)
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=403,
                detail=str(e)
            ) 