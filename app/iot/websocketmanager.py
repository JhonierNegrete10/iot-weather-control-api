from typing import Dict, List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, device_mac: str):
        await websocket.accept()
        if device_mac not in self.active_connections:
            self.active_connections[device_mac] = []
        self.active_connections[device_mac].append(websocket)

    def disconnect(self, websocket: WebSocket, device_mac: str):
        if device_mac in self.active_connections:
            self.active_connections[device_mac].remove(websocket)
            if not self.active_connections[device_mac]:
                del self.active_connections[device_mac]

    async def send_data(self, data: str, device_mac: str):
        print("WS Conected")
        print(self.active_connections)
        if device_mac in self.active_connections:
            for connection in self.active_connections[device_mac]:
                await connection.send_text(data)


manager = ConnectionManager()
