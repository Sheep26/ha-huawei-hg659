# HG659 home assistant integration.
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Setup component.
    pass