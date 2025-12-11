import logging
from typing import List, Any, Dict

from fastapi import WebSocket

logger = logging.getLogger("replay.websocket")


class WebSocketManager:
    """
    WebSocket 연결을 관리하는 기본 매니저.
    - 현재는 메모리 기반 리스트로 연결 관리
    - TODO: 추후 Redis 등 외부 스토리지/브로커로 확장 가능
    """

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """
        새로운 클라이언트 연결을 받아들이고 목록에 추가한다.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("WebSocket connected. current=%d", len(self.active_connections))

    def disconnect(self, websocket: WebSocket) -> None:
        """
        클라이언트 연결을 목록에서 제거한다.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("WebSocket disconnected. current=%d", len(self.active_connections))

    async def send_personal_text(self, websocket: WebSocket, message: str) -> None:
        await websocket.send_text(message)

    async def send_personal_json(self, websocket: WebSocket, data: Dict[str, Any]) -> None:
        await websocket.send_json(data)

    async def broadcast_text(self, message: str) -> None:
        """
        연결된 모든 클라이언트에게 텍스트 메시지를 전송한다.
        """
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.warning("Broadcast text failed: %s", e)

    async def broadcast_json(self, data: Dict[str, Any]) -> None:
        """
        연결된 모든 클라이언트에게 JSON 메시지를 전송한다.
        """
        for connection in list(self.active_connections):
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.warning("Broadcast json failed: %s", e)