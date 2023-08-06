from typing import Optional
from px_client_builder import NestedClient


from .utils import query_caller
from ..const import SEARCH_LIMIT


__all__ = (
    'CitiesClient',
    'SettlementsClient',
    'AreasClient',
    'GeographyClient',
)


class CitiesClient(NestedClient):
    _cities_q = query_caller('Address', 'getCities')

    def get_list(
        self,
        page: int = 1,
        ref: Optional[str] = None,
        q: Optional[str] = None
    ) -> dict:
        return self._cities_q(Page=page, Ref=ref, FindByString=q)


class SettlementsClient(NestedClient):
    search_limit: int

    _settlement_types_q = query_caller('Address', 'getSettlementTypes')
    _settlements_q = query_caller('Address', 'getSettlements')
    _settlements_search_q = query_caller('Address', 'searchSettlements')

    def __init__(
        self, *_, search_limit: int = SEARCH_LIMIT, **kw
    ) -> None:
        super().__init__(**kw)

        self.search_limit = search_limit

    def get_types_list(self) -> dict:
        return self._settlement_types_q()

    def get_list(
        self,
        page: int = 1,
        region_ref: Optional[str] = None,
        ref: Optional[str] = None,
        warehouse: Optional[str] = None,
        q: Optional[str] = None
    ) -> dict:
        return self._settlements_q(
            Page=page, Ref=ref, FindByString=q, RegionRef=region_ref,
            Warehouse=warehouse,
        )

    def get_search_list(
        self, q: str, limit: Optional[int] = None,
    ) -> dict:
        return self._settlements_search_q(
            CityName=q, Limit=limit or self.search_limit,
        )


class AreasClient(NestedClient):
    _areas_q = query_caller('Address', 'getAreas')

    def get_list(self) -> dict:
        return self._areas_q()


class GeographyClient(NestedClient):
    areas: AreasClient = AreasClient.as_property()
    cities: CitiesClient = CitiesClient.as_property()
    settlements: SettlementsClient = SettlementsClient.as_property()
