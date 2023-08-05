from typing import List

from azure.graphrbac.models import ServicePrincipal

from whizbang.config.app_config import AppConfig
from whizbang.domain.handler.handler_base import HandlerBase

from whizbang.domain.manager.az.az_service_principal_manager import AzServicePrincipalManager


class ServicePrincipalHandler(HandlerBase):
    def __init__(self, app_config: AppConfig, service_principal_manager: AzServicePrincipalManager):
        HandlerBase.__init__(self, app_config=app_config)
        self.__service_principal_manager = service_principal_manager

    def save(self, display_name: str, scopes: List[str], years: int = 1) -> ServicePrincipal:
        service_principal = ServicePrincipal(display_name=display_name)
        result = self.__service_principal_manager.create_for_rbac(
            service_principal=service_principal,
            scopes=scopes,
            years=years
        )
        return result

    def add_group_members_as_owner(self, app_id: str, group_object_id: str) -> None:
        self.__service_principal_manager.add_group_members_as_owner(app_id=app_id, group_object_id=group_object_id)

