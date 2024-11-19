"""The HA E-Ink Display integration."""

# HA needs to be restarted many times from the comman line in a zsh terminal by
# > hass
# At the moment the HA E-Ink Display config flow succeeds!
# davebot, D are the creds http://localhost:8123

from __future__ import annotations

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .eink_display import EInkDisplay

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA E-Ink Display from a config entry."""
    address: str = entry.data[CONF_MAC]
    ble_device = bluetooth.async_ble_device_from_address(hass, address.upper(), True)
    if not ble_device:
        raise ConfigEntryNotReady(
            f"Could not find an E-Ink Display with address {address}"
        )

    # Initialize storage for this integration if it doesn't exist
    eink = EInkDisplay(ble_device)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "title": entry.title,
        "device": eink,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    data.device.disconnect()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
