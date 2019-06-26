"""
    communication.client
    ~~~~~~~~~~~~~~~~~~~~

    Contains the client that can be used to access a service with easy access
    to the server's parameters.
"""
import rpyc
import uuid
from plumbum import colors
from .remote_parameters import RemoteParameters


class ClientService(rpyc.Service):
    def __init__(self, uuid):
        super().__init__()

        self.exposed_uuid = uuid


class BaseClient:
    def __init__(self, server, port, use_parameter_cache, call_on_error=None):
        self.use_parameter_cache = use_parameter_cache
        self.uuid = uuid.uuid4().hex

        self.client_service = ClientService(self.uuid)

        self.connect(server, port, use_parameter_cache, call_on_error=call_on_error)
        self.connected = True

    def connect(self, server, port, use_parameter_cache, call_on_error=None):
        return self._connect(server, port, use_parameter_cache, call_on_error=call_on_error)

    def _connect(self, server, port, use_parameter_cache, call_on_error=None):
        self.connection = rpyc.connect(server, port, service=self.client_service)

        cls = RemoteParameters
        if call_on_error:
            cls = self.catch_network_errors(cls, call_on_error)

        self.parameters = cls(
            self.connection.root,
            self.uuid,
            use_parameter_cache
        )

    def catch_network_errors(self, cls, call_on_error):
        function_type = type(lambda x: x)
        for attr_name in dir(cls):
            if not attr_name.startswith('__'):
                attr = getattr(cls, attr_name)

                if isinstance(attr, function_type):
                    method = attr
                    def wrapped(*args, method=method, **kwargs):
                        try:
                            return method(*args, **kwargs)
                        except (EOFError,):
                            print(colors.red | 'Connection lost')
                            self.stop()
                            call_on_error()
                            raise

                    setattr(cls, attr_name, wrapped)

        return cls

    def stop(self):
        self.connected = False