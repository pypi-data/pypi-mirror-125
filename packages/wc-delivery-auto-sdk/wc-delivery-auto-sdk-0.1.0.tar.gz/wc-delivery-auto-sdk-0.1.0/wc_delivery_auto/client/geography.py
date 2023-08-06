from typing import Optional
from px_client_builder import NestedClient


from .utils import query_caller
from ..const import Culture


__all__ = (
    'CitiesClient',
    'RegionsClient',
    'GeographyClient',
)


class CitiesClient(NestedClient):
    _cities_q = query_caller('GetAreasList')

    def get_list(
        self, culture: str = Culture.UA, country: Optional[int] = None,
        region: Optional[int] = None, all: bool = True,
        q: Optional[str] = None
    ) -> dict:
        return self._cities_q(params={
            'culture': culture, 'country': country, 'regionId': region,
            'fl_all': 'true' if all else 'false', 'cityName': q
        })


class RegionsClient(NestedClient):
    _areas_q = query_caller('GetRegionList')

    def get_list(
        self, culture: str = Culture.UA, country: Optional[int] = None
    ) -> dict:
        return self._areas_q(params={'culture': culture, 'country': country})


class GeographyClient(NestedClient):
    regions: RegionsClient = RegionsClient.as_property()
    cities: CitiesClient = CitiesClient.as_property()
