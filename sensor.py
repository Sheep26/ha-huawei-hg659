from homeassistant.components.sensor import SensorEntity
from datetime import timedelta

from .const import DOMAIN
from .coordinator import HG659UpdateCoordinator

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: HG659UpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Add entities
    entities = [
        HG659UptimeSensor(coordinator),
        HG659DeivceCountSensor(coordinator),
        HG659ExternalIPAddrSensor(coordinator),
        HG659Sensor(coordinator)
    ]
    
    async_add_entities(entities)

class HG659UptimeSensor(SensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator):
        self._coordinator = coordinator
        self._attr_name = "HG659 Uptime"
        self._attr_unique_id = "hg659_uptime"
        #self._state = None
        self._attr_native_unit_of_measurement = "s"
        self._attr_suggested_unit_of_measurement = "d"
        self._attr_device_class = "duration"
        self._attr_state_class = "measurement"
    
    @property
    def native_value(self):
        return self._coordinator.data["uptime"]
    
    #@property
    #def state(self):
        #return self._state
    
    @property
    def available(self):
        return self.native_value is not None

class HG659DeivceCountSensor(SensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator):
        self._coordinator = coordinator
        self._attr_name = "HG659 Device count"
        self._attr_unique_id = "hg659_device_count"
        #self._attr_native_value = None
        self._attr_device_class = None
        self._attr_state_class = "measurement"
    
    @property
    def native_value(self):
        return self._coordinator.data["device_count"]
    
    @property
    def extra_state_attributes(self):
        return {
            "Devices": [{
                "Hostname": d["HostName"],
                "IP Address": d["IPAddress"],
                "MAC Address": d["MACAddress"],
                "Connection Time": str(timedelta(seconds=int(d["LeaseTime"]))),
            } for d in self._coordinator.data["devices"]]
        }

    @property
    def available(self):
        return self.native_value is not None

class HG659ExternalIPAddrSensor(SensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator):
        self._coordinator = coordinator
        self._attr_name = "HG659 External IP Address"
        self._attr_unique_id = f"hg659_external_ip_addr"
    
    @property
    def native_value(self):
        return self._coordinator.data["external_ip"]
    
    @property
    def available(self):
        return self.native_value is not None

class HG659Sensor(SensorEntity):
    def __init__(self, coordinator: HG659UpdateCoordinator):
        self._coordinator = coordinator
        _LOGGER.error(coordinator.data["host"])
        self._attr_name = f"HG659 @ {coordinator.data["host"]}"
        self._attr_unique_id = f"hg659_{coordinator.data["host"]}"
    
    @property
    def extra_state_attributes(self):
        return {
            "Serial number": self._coordinator.data["serial_number"],
            "Software version": self._coordinator.data["software_version"],
            "MAC Address": self._coordinator.data["mac_addr"],
            "DNS servers": self._coordinator.data["dns_servers"],
            "External IP": self._coordinator.data["external_ip"],
            "Uptime": self._coordinator.data["uptime"]
        }
    
    @property
    def native_value(self):
        return self._coordinator.data["host"]