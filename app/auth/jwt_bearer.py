from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decode_access_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            token = credentials.credentials
            payload = decode_access_token(token)
            if payload is None:
                raise HTTPException(status_code=403, detail="Token inválido o expirado")
            return payload
        else:
            raise HTTPException(status_code=403, detail="Credenciales no encontradas")
