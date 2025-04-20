from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback

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

class HG659OnlineSensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator):
        self._attr_name = "HG659 Connected"
        self._attr_unique_id = "hg659_connected"
        self._attr_device_class = "connectivity"
        self._attr_is_on = None
        
        # Init coordinator.
        super().__init__(coordinator)
    
    @property
    def available(self):
        return self._attr_is_on is not None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.coordinator.data["connected"]
        self.async_write_ha_state()