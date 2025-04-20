# HG659 home assistant integration.
import logging
from typing import Final
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectTimeout

from .client import HG659Client
from .coordinator import HG659UpdateCoordinator, HG659UpdateCoordinatorConfig
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
#Platform.BINARY_SENSOR, 
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    _LOGGER.info("Hello world from Huawei HG659.")
    
    try:
        # Create client with config data. Store it in home assistant data.
        client = await hass.async_add_executor_job(lambda: HG659Client(entry.data[CONF_HOST], entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD]))
        
        # Attempt to login.
        login_data = await hass.async_add_executor_job(client.login)
        
        # Check if login successful.
        if not login_data["errorCategory"] == "ok":
            raise ConfigEntryAuthFailed(f"Invalid username or password.")
    except (TimeoutError, MaxRetryError, ConnectTimeout):
        # Invalid host.
        _LOGGER.error("Invalid host.")
        raise ConfigEntryNotReady(f"Timeout while connecting to {entry.data[CONF_HOST]}")
    except Exception as e:
        # Something messed up.
        _LOGGER.error("Unknown error.")
        _LOGGER.error(e)
        raise ConfigEntryNotReady(f"Timeout while connecting to {entry.data[CONF_HOST]}")
    
    config = HG659UpdateCoordinatorConfig(
        client=client
    )
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = HG659UpdateCoordinator(hass, config)
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok