from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback

from datetime import timedelta

from .const import DOMAIN, CONF_HOST
from .coordinator import HG659UpdateCoordinator

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: HG659UpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    host = entry.data[CONF_HOST]

    # Add entities
    entities = [
        HG659UptimeSensor(coordinator),
        HG659DeviceCountSensor(coordinator),
        HG659ExternalIPAddrSensor(coordinator),
        HG659Sensor(coordinator, host)
    ]
    
    async_add_entities(entities)

class HG659UptimeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator):
        self._attr_name = "HG659 Uptime"
        self._attr_unique_id = "hg659_uptime"
        #self._state = None
        self._attr_native_unit_of_measurement = "s"
        self._attr_suggested_unit_of_measurement = "d"
        self._attr_device_class = "duration"
        self._attr_state_class = "measurement"
        
        # Init coordinator.
        super().__init__(coordinator)
    
    @property
    def native_value(self):
        return self.coordinator.data["uptime"] if not self.coordinator.data == None else None
    
    #@property
    #def state(self):
        #return self._state
    
    @property
    def available(self):
        return self.native_value is not None

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

class HG659DeviceCountSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator):
        self._attr_name = "HG659 Device count"
        self._attr_unique_id = "hg659_device_count"
        #self._attr_native_value = None
        self._attr_device_class = None
        self._attr_state_class = "measurement"
        self.coordinator_data = {}
        
        # Init coordinator.
        super().__init__(coordinator)
    
    @property
    def native_value(self):
        return self.coordinator.data["device_count"] if not self.coordinator.data == None else None
    
    @property
    def extra_state_attributes(self):
        return {
            "Devices": [{
                "Hostname": d["HostName"],
                "IP Address": d["IPAddress"],
                "MAC Address": d["MACAddress"],
                "Connection Time": str(timedelta(seconds=int(d["LeaseTime"]))),
            } for d in self.coordinator.data["devices"]] if not self.coordinator.data == None else None
        }

    @property
    def available(self):
        return self.native_value is not None

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

class HG659ExternalIPAddrSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator):
        self._attr_name = "HG659 External IP Address"
        self._attr_unique_id = f"hg659_external_ip_addr"
        
        # Init coordinator.
        super().__init__(coordinator)
    
    @property
    def native_value(self):
        return self.coordinator.data["external_ip"] if not self.coordinator.data == None else None
    
    @property
    def available(self):
        return self.native_value is not None
    
    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

class HG659Sensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator, host):
        self._host = host
        self._attr_name = f"HG659 @ {host}"
        self._attr_unique_id = f"hg659_{host}"
        self.coordinator_data = {}
        
        # Init coordinator.
        super().__init__(coordinator)
    
    @property
    def extra_state_attributes(self):
        return {
            "Serial number": self.coordinator.data["serial_number"] if not self.coordinator.data == None else None,
            "Software version": self.coordinator.data["software_version"] if not self.coordinator.data == None else None,
            "MAC Address": self.coordinator.data["mac_addr"] if not self.coordinator.data == None else None,
            "DNS servers": self.coordinator.data["dns_servers"] if not self.coordinator.data == None else None,
            "External IP": self.coordinator.data["external_ip"] if not self.coordinator.data == None else None,
            "Uptime": self.coordinator.data["uptime"] if not self.coordinator.data == None else None
        }
    
    @property
    def native_value(self):
        return self._host
    
    @property
    def available(self):
        return self.native_value is not None

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()