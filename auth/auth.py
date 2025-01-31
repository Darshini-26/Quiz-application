from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from config.settings import app_config

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, admin_required: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.admin_required = admin_required  # Flag to check if admin access is required

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
            payload = self.verify_jwt(credentials.credentials)
            
            # If admin access is required, check is_admin field
            if self.admin_required and not payload.get("is_admin"):
                raise HTTPException(status_code=403, detail="Admin access required.")
            
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, app_config["SECRET_KEY"], algorithms=[app_config["ALGORITHM"]])
            user_id = payload.get("user_id")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token: user_id not found")
            return payload  # Return payload so we can check is_admin
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        
    @staticmethod
    def get_user_id_from_token(token: str) -> str:
        """Extract user_id from JWT token."""
        try:
            payload = jwt.decode(token, app_config["SECRET_KEY"], algorithms=[app_config["ALGORITHM"]])
            user_id = payload.get("user_id")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token: user_id not found")
            return user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
