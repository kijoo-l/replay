from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class ErrorInfo(BaseModel):
    code: str
    message: str


class ApiResponse(GenericModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorInfo] = None


# 성공 응답 헬퍼
def ok(data: T):
    return ApiResponse(success=True, data=data)


def created(data: T):
    return ApiResponse(success=True, data=data)


# 실패 응답 헬퍼
def fail(code: str, message: str):
    return ApiResponse(
        success=False,
        error=ErrorInfo(code=code, message=message)
    )
