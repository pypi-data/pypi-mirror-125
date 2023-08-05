from whizbang.domain.manager.az.az_manager_base import AzManagerBase
from whizbang.domain.repository.az.az_container_registry_repository import AzContainerRegistryRepository


class AzContainerRegistryManager(AzManagerBase):
    def __init__(self, repository: AzContainerRegistryRepository):
        AzManagerBase.__init__(self, repository)
        self._repository: AzContainerRegistryRepository = self._repository

    def get_tags(self, registry_name, repository_name):
        return self._repository.get_tags(registry_name=registry_name,
                                         repository_name=repository_name)
