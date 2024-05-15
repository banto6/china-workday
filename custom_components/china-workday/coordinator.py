import datetime
import logging

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class ChinaWorkdayCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, datasource):
        super().__init__(
            hass,
            _LOGGER,
            name="ChinaWorkday Coordinator",
            update_interval=datetime.timedelta(minutes=1)
        )
        self._hass = hass
        self._datasource = datasource

    async def _async_update_data(self):
        now = datetime.datetime.now()

        date_key = now.strftime('%Y-%m-%d')
        holidays = await self._get_holiday_by_cache(str(now.year))
        for holiday in holidays:
            if holiday['date'] == date_key:
                return {
                    'workday': not holiday['isOffDay'],
                    'holiday': holiday['name']
                }

        return {
            'workday': now.weekday() not in [5, 6],
            'holiday': '',
        }

    async def _get_holiday_by_cache(self, year: str):
        """
        从缓存中获取节假日信息，未获取到则从数据源中获取
        :param year:
        :return:
        """
        store = Store(self._hass, 1, 'china-workday/cache.json')

        try:
            cache = await store.async_load()
            if cache is not None and year in cache:
                return cache[year]
        except Exception as e:
            _LOGGER.warning("{} cache load error: {}".format(year, e))
            await store.async_remove()

        if cache is None:
            cache = {}

        _LOGGER.debug("get {} holiday by datasource".format(year))
        cache[year] = await self._get_holiday_by_datasource(year)
        await store.async_save(cache)

        return cache[year]

    async def _get_holiday_by_datasource(self, year: str):
        """
        从设置的数据源中获取节假日信息
        :param year:
        :return:
        """
        session = async_get_clientsession(self._hass)
        async with session.get(url=self._datasource.replace('{year}', str(year))) as response:
            content = await response.json(content_type=None)
            if 'days' not in content:
                raise RuntimeError('days field is missing')

            return content['days']
