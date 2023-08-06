from .AirzoneCloudConnector import AirzoneCloudConnector
from .AirzoneDevice import AirzoneDevice, AirzoneDevice_az_system, AirzoneDevice_az_zone
import asyncio


class AirzoneInstallation:
    def __init__(self, installation_id, conn=None, email=None, password=None):
        if conn is None:
            conn = AirzoneCloudConnector(email, password)
        self._conn = conn
        self._id = installation_id
        self._inited = False
        self.devices = []
        self.system_device = None

    async def start(self):
        data = await self._conn.get_installation(self._id)
        if data:
            self._inited = True
            for group in data["groups"]:
                for device in group["devices"]:
                    dev = AirzoneDevice.get_device(device, self._conn, self)
                    self.devices.append(dev)
                    if isinstance(dev, AirzoneDevice_az_system):
                        self.system_device = dev

    async def connect_live_updates(self):
        ws_client = self._conn.get_websocket()
        ws_client.append_startup_command(ws_client.listen_instalation, (self._id,))
        asyncio.create_task(self._conn.get_websocket().open_client())

    def get_system_status(self):
        status = False
        for device in self.devices:
            if isinstance(device, AirzoneDevice_az_zone):
                status = status or device.status.get("power", False)

        return status
    
    def get_system_idle(self):
        status = False
        for device in self.devices:
            if isinstance(device, AirzoneDevice_az_zone):
                status = status or (
                    device.status.get("power", False)
                    and device.status.get("setpoint_air_heat", {"celsius": 0}).get(
                        "celsius", 0
                    )
                    > device.status.get("local_temp", {"celsius": 0}).get(
                        "celsius", 0
                    )
                )

        return status