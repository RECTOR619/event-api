# for protecting routes with JWT Bearer token

from fastapi import Request, HTTPException
from fastapi .security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decodeJWT



# class jwtBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(jwtBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
#         if credentials:
#             if not self.verify_jwt(credentials.credentials):
#                 raise HTTPException(status_code=403, detail="Could not validate credentials")
#             return credentials.credentials
#         else:
#             raise HTTPException(status_code=403, detail="Could not validate credentials")
 
#     def verify_jwt(self, jwtoken: str) -> bool:
#         isTokenValid : bool = False
#         payload = decodeJWT(jwtoken)
#         if payload :
#             isTokenValid = True
#         return isTokenValid    

class jwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or expired token")
 
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid : bool = False
        payload = decodeJWT(jwtoken)
        if payload :
            isTokenValid = True
        return isTokenValid