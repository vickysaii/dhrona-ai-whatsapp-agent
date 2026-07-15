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
            print("No admin found. Creating default admin...")

            hashed = hash_password("adminpassword")

            DatabaseRepository.create_user(
                email="admin@business.com",
                password_hash=hashed,
                role="admin",
            )

            print("✅ Default admin created.")

    except Exception as e:
        print(f"❌ Failed to seed admin: {e}")


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

        print("\n" + "=" * 70)
        print("LOGIN ATTEMPT")
        print("=" * 70)
        print("Email:", payload.email)
        print("Password:", payload.password)
        print("Password Length:", len(payload.password))
        print("User Found:", user is not None)

        if not user:
            print("❌ User not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        print("Role:", user.get("role"))
        print("Hash:", user.get("password_hash"))
        print("Hash Length:", len(user.get("password_hash", "")))
        print("=" * 70)

        valid = verify_password(
            payload.password,
            user["password_hash"],
        )

        print("Password Verification:", valid)

        if not valid:
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

        print("✅ Login Successful")
        print("=" * 70)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user["role"],
        }

    except HTTPException:
        raise

    except Exception as e:

        print("\n")
        print("=" * 70)
        print("LOGIN ERROR")
        print(type(e).__name__)
        print(str(e))
        print("=" * 70)
        print("\n")

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