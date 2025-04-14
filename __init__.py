# HG659 home assistant integration.
import logging
from typing import Final
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .client import HG659Client

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_create_entry(hass: HomeAssistant, entry: ConfigEntry):
    _CLIENT = HG659Client(entry.data[CONF_HOST], entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])
    
    login_data = _CLIENT.login()
    
    # Setup component.
    return True