"""Data coordinator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import HG659Client

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=30)

@dataclass
class HG659UpdateCoordinatorConfig:
    """Class representing coordinator configuration."""

    client: HG659Client
    update_interval = UPDATE_INTERVAL

class HG659UpdateCoordinator(DataUpdateCoordinator):
    """The HG659 data coordinator."""
    
    def __init__(self, hass: HomeAssistant, config: HG659UpdateCoordinatorConfig):
        """Init."""
        
        self._hass = hass
        self._client = config.client
        
        super().__init__(
            hass,
            _LOGGER,
            name="HG659UpdateCoordinator",
            update_interval=config.update_interval
        )
    
    @property
    def client(self) -> HG659Client:
        return self._client
    
    async def _async_update_data(self) -> dict:
        try:
            device_info = await self._hass.async_add_executor_job(self.client.get_device_info)
            diagnose_internet = await self._hass.async_add_executor_job(self.client.get_diagnose_internet)
            device_count = await self._hass.async_add_executor_job(self.client.get_device_count)
            devices = await self._hass.async_add_executor_job(self.client.get_active_devices)
            return {
                "host": self.client.host,
                "connected": True if diagnose_internet["ConnectionStatus"] == "Connected" else False,
                "serial_number": device_info["SerialNumber"],
                "software_version": device_info["SoftwareVersion"],
                "mac_addr": diagnose_internet["MACAddress"],
                "uptime": device_info["UpTime"],
                "device_count": device_count,
                "devices": devices,
                "external_ip": diagnose_internet["ExternalIPAddress"],
                "dns_servers": diagnose_internet["DNSServers"],
            }
        except Exception as err:
            _LOGGER.error("Error updating HG659 data: %s", err)
            raise UpdateFailed(f"Error communicating with HG659 device: {err}")