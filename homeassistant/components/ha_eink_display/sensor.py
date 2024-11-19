"""Support for E-Ink Display sensors."""

from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass
class EInkDisplayEntityDescription(SensorEntityDescription):
    """Provides a description for a HA E-Ink Display sensor."""

    unique_id: str | None = None


SENSORS = (
    EInkDisplayEntityDescription(
        key="battery",
        name="Battery",
        unique_id="eink_display_battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    EInkDisplayEntityDescription(
        key="last_updated",
        name="Last updated",
        unique_id="eink_display_last_updated",
        icon="mdi:update",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up E-Ink Display sensors based on a config entry."""

    # data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([EInkDisplaySensor(description) for description in SENSORS])


class EInkDisplaySensor(SensorEntity):
    """Representation of an E-Ink Display sensor."""

    _attr_has_entity_name = True

    def __init__(self, description: EInkDisplayEntityDescription) -> None:
        """Initialize the sensor."""
        self.entity_description = description
        # self.device = device

        # Set up the device registry information
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, "1234")},
            manufacturer="Anderloid",
            name="E-Ink Display",
            sw_version="1.0.0",
        )

        self._attr_unique_id = f"1234_{description.unique_id}"

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            self._attr_native_value = (
                await self._fetch_battery_level()
                if self.entity_description.key == "battery"
                else dt_util.utcnow()
            )
        except Exception as error:
            _LOGGER.error("Could not read state: %s", error)

    async def _fetch_battery_level(self) -> int:
        # async with BleakClient(self._address) as client:
        #    services = await client.get_services()
        #    service = next((s for s in services if s.uuid == SERVICE_UUID), None)
        #    if service:
        #        for char in service.characteristics:
        #            if "read" in char.properties:
        #                data = await client.read_gatt_char(char.uuid)
        #                self._state = int.from_bytes(data, byteorder="little")
        #                break
        #    else:
        #        _LOGGER.error("Service not found")
        return 85
