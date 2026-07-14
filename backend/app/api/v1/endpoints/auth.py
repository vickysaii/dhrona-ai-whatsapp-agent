from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import UserLogin, Token, UserResponse
from app.repositories.db_repo import DatabaseRepository
from app.utils.security import verify_password, hash_password, create_access_token
from app.middleware.auth_middleware import get_current_user

router = APIRouter()

def ensure_default_admin_exists():
    """
    Checks if any admin exists in the system. If none, seeds a default admin.
    """
    try:
        user = DatabaseRepository.get_user_by_email("admin@business.com")
        if not user:
            print("No admin user found. Seeding default administrator: admin@business.com / adminpassword")
            hashed = hash_password("adminpassword")
            DatabaseRepository.create_user("admin@business.com", hashed, role="admin")
    except Exception as e:
        print(f"Failed to check/seed default admin user: {e}")

# Call immediately on module load
ensure_default_admin_exists()

@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    """
    Logs in an admin, returning a signed JWT access token.
    """
    ensure_default_admin_exists() # Double check seeding
    
    user = DatabaseRepository.get_user_by_email(payload.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    if not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate access token
    access_token = create_access_token(data={"email": user["email"], "role": user["role"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"]
    }

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Simulates a logout (client forgets token; backend acknowledges).
    """
    return {"success": True, "message": "Logged out successfully"}
