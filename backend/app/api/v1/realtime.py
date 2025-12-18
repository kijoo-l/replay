import json
import logging
from typing import Any, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.utils.websocket_manager import WebSocketManager

router = APIRouter(
    prefix="/ws",
    tags=["실시간"],
)

logger = logging.getLogger("replay.websocket")
manager = WebSocketManager()


@router.websocket("/echo")
async def websocket_echo(websocket: WebSocket) -> None:
    """
    WebSocket echo / broadcast / notification 수신 엔드포인트

    지원 메시지 타입:
    - echo        : 개인 echo
    - broadcast   : 전체 브로드캐스트
    - notification: 서버 발행 알림 수신용 (push 전용)
    """
    await manager.connect(websocket)
    logger.info("Client connected to /ws/echo")

    try:
        while True:
            raw = await websocket.receive_text()
            logger.debug("Received raw message: %s", raw)

            try:
                payload: Dict[str, Any] = json.loads(raw)
            except json.JSONDecodeError:
                payload = {"type": "echo", "payload": raw}

            msg_type = payload.get("type", "echo")
            data = payload.get("payload")

            # broadcast
            if msg_type == "broadcast":
                await manager.broadcast_json({
                    "type": "broadcast",
                    "payload": data,
                })

            # notification (클라이언트 송신은 무시, 서버 push 전용)
            elif msg_type == "notification":
                continue

            # default echo
            else:
                await manager.send_personal_json(
                    websocket,
                    {
                        "type": "echo",
                        "payload": data,
                    }
                )

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected from /ws/echo")
        manager.disconnect(websocket)

    except Exception:
        logger.exception("Unexpected WebSocket error")
        manager.disconnect(websocket)
