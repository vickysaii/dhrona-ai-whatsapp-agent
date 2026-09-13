from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import UserLogin, Token
from app.repositories.db_repo import DatabaseRepository
from app.utils.security import (
    verify_password,
    hash_password,
    create_access_token,
)
from app.middleware.auth_middleware import get_current_user

router = APIRouter()


def ensure_default_admin_exists():
    """
    Checks if any admin exists in the system.
    If none exists, create the default administrator.
    """
    try:
        user = DatabaseRepository.get_user_by_email("admin@business.com")

        if not user:
            print("[AUTH] No admin found. Creating default admin...")

            hashed = hash_password("adminpassword")

            DatabaseRepository.create_user(
                email="admin@business.com",
                password_hash=hashed,
                role="admin",
            )

            print("[AUTH] Default admin created successfully.")

    except Exception as e:
        print(f"[AUTH] Failed to seed admin: {e}")


# Run once on startup
ensure_default_admin_exists()


@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    """
    Admin login endpoint.
    """

    ensure_default_admin_exists()

    try:
        user = DatabaseRepository.get_user_by_email(payload.email)

        print("\n" + "=" * 50)
        print(f"[AUTH] Login attempt for: {payload.email}")
        print(f"[AUTH] User found in DB: {user is not None}")

        if not user:
            print("[AUTH] Login failed: User not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        valid = verify_password(
            payload.password,
            user["password_hash"],
        )

        print(f"[AUTH] Password valid: {valid}")

        if not valid:
            print("[AUTH] Login failed: Password mismatch")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            {
                "email": user["email"],
                "role": user["role"],
            }
        )

        print("[AUTH] Login successful. Access token generated.")
        print("=" * 50 + "\n")

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user["role"],
        }

    except HTTPException:
        raise

    except Exception as e:
        print("\n" + "=" * 50)
        print(f"[AUTH ERROR] {type(e).__name__}: {str(e)}")
        print("=" * 50 + "\n")

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout endpoint.
    JWT logout is handled client-side by deleting the token.
    """

    return {
        "success": True,
        "message": "Logged out successfully",
    }