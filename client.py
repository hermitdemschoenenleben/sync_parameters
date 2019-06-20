"""
    communication.client
    ~~~~~~~~~~~~~~~~~~~~

    Contains the client that can be used to access a service with easy access
    to the server's parameters.
"""
import rpyc
import uuid
from .remote_parameters import RemoteParameters


class ClientService(rpyc.Service):
    def __init__(self, uuid):
        super().__init__()

        self.exposed_uuid = uuid


class BaseClient:
    def __init__(self, server, port, use_parameter_cache):
        self.use_parameter_cache = use_parameter_cache
        self.uuid = uuid.uuid4().hex

        self.client_service = ClientService(self.uuid)

        self.connect(server, port, use_parameter_cache)

    def connect(self, server, port, use_parameter_cache):
        return self._connect(server, port, use_parameter_cache)

    def _connect(self, server, port, use_parameter_cache):
        self.connection = rpyc.connect(server, port, service=self.client_service)
        self.parameters = RemoteParameters(
            self.connection.root,
            self.uuid,
            use_parameter_cache
        )