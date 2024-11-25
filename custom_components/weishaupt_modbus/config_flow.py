"""Config flow."""

from aiofiles.os import scandir

from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PREFIX
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv


from .const import (
    CONST,
    CONF_DEVICE_POSTFIX,
    CONF_KENNFELD_FILE,
    CONF_HK2,
    CONF_HK3,
    CONF_HK4,
    CONF_HK5,
    CONF_NAME_DEVICE_PREFIX,
    CONF_NAME_TOPIC_PREFIX,
    CONF_NAME_OLD_NAMESTYLE,
)


async def build_kennfeld_list(hass: HomeAssistant):
    """browses integration directory for kennfeld files"""
    kennfelder = []
    filelist = []

    filepath = hass.config.config_dir + "/custom_components/" + CONST.DOMAIN

    dir_iterator = await scandir(filepath)

    for filename in dir_iterator:
        filelist.append(filename)

    for _useless, item in enumerate(filelist):
        if item.name.__contains__("kennfeld.json"):
            kennfelder.append(item.name)

    if len(kennfelder) < 1:
        kennfelder.append("weishaupt_wbb_kennfeld.json")

    return kennfelder


async def validate_input(data: dict) -> dict[str, Any]:
    """Validate the input."""
    # Validate the data can be used to set up a connection.

    # This is a simple example to show an error in the UI for a short hostname
    # The exceptions are defined at the end of this file, and are used in the
    # `async_step_user` method below.
    if len(data["host"]) < 3:
        raise InvalidHost

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    # "Title" is what is displayed to the user for this hub device
    # It is stored internally in HA as part of the device config.
    # See `async_step_user` below for how this is used
    return {"title": data["host"]}


class ConfigFlow(config_entries.ConfigFlow, domain=CONST.DOMAIN):
    """Class config flow."""

    VERSION = 5
    # Pick one of the available connection classes in homeassistant/config_entries.py
    # This tells HA if it should be asking for updates, or it'll be notified of updates
    # automatically. This example uses PUSH, as the dummy hub will notify HA of
    # changes.
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Step for setup process."""
        # This goes through the steps to take the user through the setup process.
        # Using this it is possible to update the UI and prompt for additional
        # information. This example provides a single form (built from `DATA_SCHEMA`),
        # and when that has some validated input, it calls `async_create_entry` to
        # actually create the HA config entry. Note the "title" value is returned by
        # `validate_input` above.

        # DATA_SCHEMA = vol.Schema({("host"): str, ("port"): cv.port})
        # The caption comes from strings.json / translations/en.json.
        # strings.json can be processed into en.json with some HA commands.
        # did not find out how this works yet.
        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_PORT, default="502"): cv.port,
                vol.Optional(CONF_PREFIX, default=CONST.DEF_PREFIX): str,
                vol.Optional(CONF_NAME_OLD_NAMESTYLE, default=False): bool,
                vol.Optional(CONF_DEVICE_POSTFIX, default=""): str,
                #        vol.Optional(CONF_KENNFELD_FILE, default=CONST.DEF_KENNFELDFILE): str,
                vol.Optional(
                    CONF_KENNFELD_FILE, default="weishaupt_wbb_kennfeld.json"
                ): vol.In(await build_kennfeld_list(self.hass)),
                vol.Optional(CONF_HK2, default=False): bool,
                vol.Optional(CONF_HK3, default=False): bool,
                vol.Optional(CONF_HK4, default=False): bool,
                vol.Optional(CONF_HK5, default=False): bool,
                vol.Optional(CONF_NAME_DEVICE_PREFIX, default=False): bool,
                vol.Optional(CONF_NAME_TOPIC_PREFIX, default=False): bool,
            }
        )

        errors = {}
        info = None
        if user_input is not None:
            try:
                info = await validate_input(user_input)

                return self.async_create_entry(title=info["title"], data=user_input)

            except Exception:  # noqa: BLE001
                errors["base"] = "unknown error"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Trigger a reconfiguration flow."""
        errors: dict[str, str] = {}
        reconfigure_entry = self._get_reconfigure_entry()

        if user_input:
            return self.async_update_reload_and_abort(
                reconfigure_entry, data_updates=user_input
            )

        schema_reconfigure = vol.Schema(
            {
                vol.Required(CONF_HOST, default=reconfigure_entry.data[CONF_HOST]): str,
                vol.Optional(
                    CONF_PORT, default=reconfigure_entry.data[CONF_PORT]
                ): cv.port,
                vol.Optional(
                    CONF_PREFIX, default=reconfigure_entry.data[CONF_PREFIX]
                ): str,
                # use old namestyle without device prefix when true
                vol.Optional(
                    CONF_NAME_OLD_NAMESTYLE,
                    default=reconfigure_entry.data[CONF_NAME_OLD_NAMESTYLE],
                ): bool,
                # reconfigure of device postfix leads to duplicated devices
                vol.Optional(
                    CONF_DEVICE_POSTFIX,
                    default=reconfigure_entry.data[CONF_DEVICE_POSTFIX],
                ): str,
                # vol.Optional(CONF_KENNFELD_FILE, default=CONST.DEF_KENNFELDFILE): str,
                vol.Optional(
                    CONF_KENNFELD_FILE,
                    default=reconfigure_entry.data[CONF_KENNFELD_FILE],
                ): vol.In(await build_kennfeld_list(self.hass)),
                vol.Optional(CONF_HK2, default=reconfigure_entry.data[CONF_HK2]): bool,
                vol.Optional(CONF_HK3, default=reconfigure_entry.data[CONF_HK3]): bool,
                vol.Optional(CONF_HK4, default=reconfigure_entry.data[CONF_HK4]): bool,
                vol.Optional(CONF_HK5, default=reconfigure_entry.data[CONF_HK5]): bool,
                vol.Optional(
                    CONF_NAME_DEVICE_PREFIX,
                    default=reconfigure_entry.data[CONF_NAME_DEVICE_PREFIX],
                ): bool,
                vol.Optional(
                    CONF_NAME_TOPIC_PREFIX,
                    default=reconfigure_entry.data[CONF_NAME_TOPIC_PREFIX],
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=schema_reconfigure,
            errors=errors,
            description_placeholders={
                CONF_HOST: "myhostname",
            },
        )

    # @staticmethod
    # @callback
    # def async_get_options_flow(
    #    config_entry: config_entries.ConfigEntry,
    # ) -> config_entries.OptionsFlow:
    #    """Create the options flow."""
    #    return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """options flow handler"""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""

        schema_options_flow = vol.Schema(
            {
                vol.Optional(CONF_PORT, default="502"): cv.port,
                vol.Optional(CONF_PREFIX, default=CONST.DEF_PREFIX): str,
                # use old namestyle without device prefix when true
                vol.Optional(CONF_NAME_OLD_NAMESTYLE, default=False): bool,
                vol.Optional(CONF_DEVICE_POSTFIX, default=""): str,
                #        vol.Optional(CONF_KENNFELD_FILE, default=CONST.DEF_KENNFELDFILE): str,
                vol.Optional(
                    CONF_KENNFELD_FILE, default="weishaupt_wbb_kennfeld.json"
                ): vol.In(await build_kennfeld_list(self.hass)),
                vol.Optional(CONF_HK2, default=False): bool,
                vol.Optional(CONF_HK3, default=False): bool,
                vol.Optional(CONF_HK4, default=False): bool,
                vol.Optional(CONF_HK5, default=False): bool,
                vol.Optional(CONF_NAME_DEVICE_PREFIX, default=False): bool,
                vol.Optional(CONF_NAME_TOPIC_PREFIX, default=False): bool,
            }
        )

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init", data_schema=schema_options_flow)


class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""


class ConnectionFailed(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
