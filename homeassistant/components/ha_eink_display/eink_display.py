"""Connects with the HA E-Ink Display."""

import logging
import time

from bleak_retry_connector import BleakClient, BLEDevice, establish_connection

_LOGGER = logging.getLogger(__name__)


class EInkDisplay:
    """Connects to an E-Ink Display to get and set information."""

    def __init__(self, ble_device: BLEDevice) -> None:
        """Initialize the class object."""

        self.ble_device = ble_device
        self._cached_services = None
        self.client = None
        self.name = "E-Ink Display"
        self.prev_time = 0

        self.result = {"battery": 85, "fw_version": "1.0.0"}

    def disconnect(self) -> None:
        self.client = None
        self.ble_device = None

    async def connect(self) -> None:
        if self.client and self.client.is_connected:
            return
        _LOGGER.debug(f"{self.name}: Connecting...")

        try:
            self.client = await establish_connection(
                BleakClient,
                self.ble_device,
                self.name,
                self._disconnected,
                cached_services=self._cached_services,
                ble_device_callback=lambda: self.ble_device,
            )
            _LOGGER.debug(f"{self.name}: Connected! RSSI: {self.ble_device.rssi}")
        except Exception:
            _LOGGER.debug(f"{self.name}: Error connecting to device")

    def _disconnect(self, client: BleakClient) -> None:
        """BLE disconnected callback."""
        _LOGGER.debug(f"{self.name}: disconnected from device.")
        self.client = None

    async def read_data(self):
        if self.ble_device is None:
            return self.result

        time = time.time()
        if time - self.prev_time < 1:
            return self.result

        self.prev_time = time
        await self.connect()
        # TODO: continue:
        # https://github.com/bkbilly/OralB/blob/main/oralb/__init__.py
