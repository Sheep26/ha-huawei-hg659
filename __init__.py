# HG659 home assistant integration.
import logging
from typing import Final

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    # Setup component.
    return True