import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectTimeout

from .const import DOMAIN

from .client import HG659Client

class HuaweiHG659ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                client = HG659Client(user_input[CONF_HOST], user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
                
                login_data = client.login()
                
                if login_data["errorCategory"] == "ok":
                    return self.async_create_entry(
                        title=f"HG659 @ {user_input[CONF_HOST]}",
                        data=user_input
                    )
                else:
                    errors[CONF_PASSWORD] = "Invalid username or password"
            except (TimeoutError, MaxRetryError, ConnectTimeout):
                errors[CONF_HOST] = "Invalid host."
            except Exception:
                errors["_base"] = "Unknown error."

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors
        )