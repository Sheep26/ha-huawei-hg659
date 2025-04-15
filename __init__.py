# HG659 home assistant integration.
import logging
from typing import Final
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectTimeout

from .client import HG659Client

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
#Platform.BINARY_SENSOR, 
PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_create_entry(hass: HomeAssistant, entry: ConfigEntry):
    try:
        # Create client with config data.
        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = HG659Client(entry.data[CONF_HOST], entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])
        
        # Attempt to login.
        login_data = hass.data[DOMAIN][entry.entry_id].login()
        
        # Check if login successful.
        if not login_data["errorCategory"] == "ok":
            _LOGGER.error("Huawei HG659, Login error.")
            hass.data[DOMAIN][entry.entry_id] = None
            return False
    except (TimeoutError, MaxRetryError, ConnectTimeout):
        # Invalid host.
        _LOGGER.error("Huawei HG659, Invalid host.")
        hass.data[DOMAIN][entry.entry_id] = None
        return False
    except Exception:
        # Something messed up.
        _LOGGER.error("Huawei HG659, Unknown error.")
        hass.data[DOMAIN][entry.entry_id] = None
        return False
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok