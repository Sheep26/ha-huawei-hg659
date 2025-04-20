from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DOMAIN
from .coordinator import HG659UpdateCoordinator

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: HG659UpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Add entities
    entities = [
        HG659OnlineSensor(coordinator),
    ]
    
    async_add_entities(entities)

class HG659OnlineSensor(BinarySensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator):
        self._coordinator = coordinator
        self._attr_name = "HG659 Connected"
        self._attr_unique_id = "hg659_connected"
        self._attr_device_class = "connectivity"
        self._attr_is_on = None

    def update(self):
        """Fetch new state data from the router asynchronously."""
        try:
            self._attr_is_on = self._coordinator.data["connected"]
        except Exception as e:
            _LOGGER.warning(f"Failed to update HG659 online sensor: {e}")
    
    @property
    def available(self):
        return self._attr_is_on is not None