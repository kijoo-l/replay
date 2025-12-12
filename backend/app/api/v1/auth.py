from fastapi import APIRouter, Depends
from app.dependencies.auth import require_admin
from app.schemas.common import ok

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/admin-test")
def admin_test(user = Depends(require_admin)):
    return ok({"message": "관리자만 접근 가능", "user": user})
