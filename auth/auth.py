from redis import Redis
from config.redis import settings
from fastapi import Header, Request, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from config.settings import app_config
from datetime import datetime, timedelta

# Initialize Redis client
redis_client =Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, admin_required: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.admin_required = admin_required  # Flag to check if admin access is required

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
            token = credentials.credentials

            # Check if token is blacklisted (invalidated)
            if redis_client.get(f"blacklist:{token}"):
                raise HTTPException(status_code=401, detail="Token has been revoked.")

            payload = self.verify_jwt(token)

            # If admin access is required, check is_admin field
            if self.admin_required and not payload.get("is_admin"):
                raise HTTPException(status_code=403, detail="Admin access required.")
            
            return token
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

    @staticmethod
    def logout(token: str):
        """Blacklist the token by storing it in Redis until it expires."""
        try:
            payload = jwt.decode(token, app_config["SECRET_KEY"], algorithms=[app_config["ALGORITHM"]])
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                expiry_time = datetime.utcfromtimestamp(exp_timestamp) - datetime.utcnow()
                redis_client.setex(f"blacklist:{token}", int(expiry_time.total_seconds()), "revoked")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")



