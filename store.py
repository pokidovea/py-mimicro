from dataclasses import dataclass
from typing import Optional

from multidict import CIMultiDictProxy, MultiDictProxy


@dataclass
class ResourceOverride:
    domain: str
    resource: str
    method: str
    content: str
    status: int = 200


@dataclass
class RequestLogRecord:
    domain: str
    resource: str
    method: str
    path: str
    payload: str
    request_headers: CIMultiDictProxy
    request_params: MultiDictProxy
    response: str
    status: int

    @property
    def as_dict(self):
        return {
            **self.__dict__,
            'request_headers': list(self.request_headers.items()),
            'request_params': list(self.request_params.items()),
        }


class ResourceOverrideStorage:
    def __init__(self):
        self._storage = []

    async def add(
        self, domain: str, resource: str, method: str, content: str, status: int = 200,
    ):
        self._storage.append(ResourceOverride(domain, resource, method, content, status))

    async def get(self, domain: str, resource: str, method: str) -> Optional[ResourceOverride]:
        for override in self._storage:
            key = (override.domain, override.resource, override.method)
            if key == (domain, resource, method):
                return override

    async def remove(self, domain: str, resource: Optional[str], method: Optional[str]):
        def keep(override) -> bool:
            if override.domain != domain:
                return True

            if resource and override.resource != resource:
                return True

            if method and override.method != method:
                return True

            return False

        self._storage = [item for item in self._storage if keep(item)]

    async def clean(self):
        self._storage = []


class RequestStorage:
    def __init__(self):
        self._storage = []

    async def add(
        self,
        domain: str,
        resource: str,
        method: str,
        path: str,
        payload: str,
        request_headers: CIMultiDictProxy,
        request_params: MultiDictProxy,
        response: str,
        status: int,
    ):
        self._storage.append(
            RequestLogRecord(
                domain=domain,
                resource=resource,
                method=method,
                path=path,
                payload=payload,
                request_headers=request_headers,
                request_params=request_params,
                response=response,
                status=status,
            )
        )

    def __iter__(self):
        return iter(self._storage)

    async def clean(self):
        self._storage = []


overrides_storage = ResourceOverrideStorage()
requests_storage = RequestStorage()
