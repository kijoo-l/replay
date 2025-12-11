# app/database.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.config import settings

# --------------------------------------------------------------------
# 1. DATABASE_URL 검증
# --------------------------------------------------------------------
if not getattr(settings, "DATABASE_URL", None):
    # 기존 배포 설정과 동일하게, 환경 변수 누락 시 바로 예외 발생
    raise ValueError("DATABASE_URL is not set in environment variables")

# --------------------------------------------------------------------
# 2. SQLAlchemy Engine / Session 설정
# --------------------------------------------------------------------
# ENV 값에 따라 echo 옵션 등 조절 가능
# - local / development: SQL 쿼리 로그 확인
# - production: 조용히 동작
is_dev = getattr(settings, "ENV", "production") != "production"

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=is_dev,   # 로컬 개발 환경에서만 SQL 출력
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)

# --------------------------------------------------------------------
# 3. Base 선언 (모든 도메인 모델이 상속받을 부모 클래스)
# --------------------------------------------------------------------
Base = declarative_base()


# --------------------------------------------------------------------
# 4. FastAPI Dependency - get_db
# --------------------------------------------------------------------
def get_db():
    """
    요청 단위로 DB 세션을 열고, 요청이 끝나면 반드시 닫아주는 의존성 주입 함수.
    FastAPI 엔드포인트에서 `Depends(get_db)`로 사용.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------------------------
# 5. 연결 테스트용 TestItem 모델 + 테이블 생성 함수
# --------------------------------------------------------------------
class TestItem(Base):
    """
    DB 연결 상태를 빠르게 검증하기 위한 테스트용 모델.
    실제 비즈니스 로직에서는 사용하지 않고, 이후 필요 시 삭제 가능.
    """
    __tablename__ = "test_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)


def init_test_model() -> None:
    """
    앱 시작 시 한 번 호출하여 DB 연결 여부를 확인하고
    TestItem 테이블을 생성하는 용도.

    - 연결 실패 시 여기에서 바로 예외가 발생하므로
      잘못된 DATABASE_URL / 드라이버 문제를 빠르게 발견할 수 있음.
    """
    Base.metadata.create_all(bind=engine)
