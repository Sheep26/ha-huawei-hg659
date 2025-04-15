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

async def async_create_entry(hass: HomeAssistant, entry: ConfigEntry):
    try:
        # Create client with config data.
        _CLIENT = HG659Client(entry.data[CONF_HOST], entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])
        
        # Attempt to login.
        login_data = _CLIENT.login()
        
        if not login_data["errorCategory"] == "ok":
            _LOGGER.error("Huawei HG659, Login error.")
            return False
        else: # Successful login.
            pass
    except (TimeoutError, MaxRetryError, ConnectTimeout):
        # Invalid host.
        _LOGGER.error("Huawei HG659, Invalid host.")
        return False
    except Exception:
        # Something fucked up.
        _LOGGER.error("Huawei HG659, Unknown error.")
        return False
    
    return True