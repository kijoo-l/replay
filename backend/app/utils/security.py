from datetime import datetime, timedelta
from typing import Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.config import settings


# --------------------------------------------------------------------
# 1. 비밀번호 해시/검증
# --------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    평문 비밀번호를 bcrypt 해시로 변환합니다.
    이후 DB에는 이 해시 문자열만 저장합니다.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    입력된 평문 비밀번호와 DB에 저장된 해시가 일치하는지 검증합니다.
    """
    return pwd_context.verify(plain_password, hashed_password)


# --------------------------------------------------------------------
# 2. JWT 토큰 페이로드 정의
# --------------------------------------------------------------------
class TokenPayload(BaseModel):
    """
    Access Token에 담길 기본 페이로드 구조입니다.

    - sub: 사용자 ID
    - role: 사용자 역할 (예: "ADMIN", "USER")
    - exp: 만료 시간 (Unix timestamp) - jose 라이브러리가 내부에서 사용
    """
    sub: int
    role: str
    exp: int


# --------------------------------------------------------------------
# 3. JWT 발급/검증
# --------------------------------------------------------------------
ALGORITHM = settings.JWT_ALGORITHM


def create_access_token(
    data: Dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    주어진 데이터(dict)를 기반으로 Access Token을 발급합니다.

    data 예시:
    {
        "sub": user_id,
        "role": "ADMIN" 또는 "USER"
    }
    """
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def decode_token(token: str) -> TokenPayload:
    """
    JWT 문자열을 디코딩하여 TokenPayload로 반환합니다.
    검증 실패 시 JWTError 예외가 발생하며,
    상위 레벨에서 AppException 등으로 변환해 사용할 수 있습니다.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        token_data = TokenPayload(**payload)
        return token_data
    except JWTError as exc:
        # 이 단계에서는 라이브러리 예외만 던지고,
        # 실제 API 레벨에서는 AppException으로 감싸서 공통 에러 포맷으로 응답하도록 처리 예정입니다.
        raise exc