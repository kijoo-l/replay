from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_admin
from app.schemas.common import ok
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(data: UserCreate, db: Session = Depends(get_db)):
    """
    회원가입: 일반 사용자 기준 이메일·비밀번호·이름 등으로 계정 생성
    """
    user = UserService().signup(db, data)
    return ok(user)


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    로그인: 이메일·비밀번호 검증 후 Access Token 발급
    """
    result = UserService().login(db, data.email, data.password)
    return ok(result)


@router.get("/admin-test")
def admin_test(user=Depends(require_admin)):
    """
    관리자 전용 접근 테스트 엔드포인트
    """
    return ok({"message": "관리자만 접근 가능", "user": user})
