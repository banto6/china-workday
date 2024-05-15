import logging
from datetime import datetime

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    async_add_entities([ChinaWorkdayBinarySensor(hass.data[DOMAIN]['coordinator'])])


class ChinaWorkdayBinarySensor(CoordinatorEntity, BinarySensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = '{}.{}'.format(DOMAIN, 'is_workday').lower()
        self.entity_id = self._attr_unique_id
        self._attr_name = '是否工作日'

        self._update_value()

    @callback
    def _handle_coordinator_update(self):
        self._update_value()
        self.async_write_ha_state()

    def _update_value(self):
        self._attr_is_on = self.coordinator.data['workday']
        self._attr_extra_state_attributes = {
            'holiday': self.coordinator.data['holiday']
        }
