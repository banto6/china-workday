import logging
from typing import Any, Dict

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ChinaWorkdayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: Dict[str, str] = {}
        if user_input is not None:
            return self.async_create_entry(title='ChinaWorkday', data={
                'datasource': user_input['datasource'],
            })

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required('datasource', default='https://ghfast.top/https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/{year}.json'): str,
                }
            ),
            errors=errors
        )

    # @staticmethod
    # @callback
    # def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
    #     return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """
        功能菜单
        :param user_input:
        :return:
        """
        return self.async_show_menu(
            step_id="init",
            menu_options=['update_datasource', 'clear_cache']
        )

    async def async_step_update_datasource(self,  user_input: dict[str, Any] | None = None) -> FlowResult:
        """
        更新数据源
        :param user_input:
        :return:
        """
        errors: Dict[str, str] = {}
        if user_input is not None:
            # TODO
            return self.async_create_entry(title='', data={})

        return self.async_show_form(
            step_id="update_datasource",
            data_schema=vol.Schema(
                {
                    vol.Required('datasource', default=self.config_entry.data['datasource']): str,
                }
            ),
            errors=errors
        )

    async def async_step_clear_cache(self,  user_input: dict[str, Any] | None = None) -> FlowResult:
        """
        清除缓存数据
        :param user_input:
        :return:
        """
        errors: Dict[str, str] = {}
        if user_input is not None:
            # TODO
            return self.async_create_entry(title='', data={})

        return self.async_show_form(
            step_id="clear_cache",
            data_schema=vol.Schema(
                {
                    vol.Required('datasource', default=self.config_entry.data['datasource']): str,
                }
            ),
            errors=errors
        )
