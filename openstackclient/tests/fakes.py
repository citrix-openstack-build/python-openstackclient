#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import copy
import json
import mock
import six
import sys
import uuid

from keystoneauth1 import fixture
import requests


AUTH_TOKEN = "foobar"
AUTH_URL = "http://0.0.0.0"
USERNAME = "itchy"
PASSWORD = "scratchy"
PROJECT_NAME = "poochie"
REGION_NAME = "richie"
INTERFACE = "catchy"
VERSION = "3"

TEST_RESPONSE_DICT = fixture.V2Token(token_id=AUTH_TOKEN,
                                     user_name=USERNAME)
_s = TEST_RESPONSE_DICT.add_service('identity', name='keystone')
_s.add_endpoint(AUTH_URL + '/v2.0')

TEST_RESPONSE_DICT_V3 = fixture.V3Token(user_name=USERNAME)
TEST_RESPONSE_DICT_V3.set_project_scope()

TEST_VERSIONS = fixture.DiscoveryList(href=AUTH_URL)


class FakeStdout(object):
    def __init__(self):
        self.content = []

    def write(self, text):
        self.content.append(text)

    def make_string(self):
        result = ''
        for line in self.content:
            result = result + line
        return result


class FakeLog(object):
    def __init__(self):
        self.messages = {}

    def debug(self, msg):
        self.messages['debug'] = msg

    def info(self, msg):
        self.messages['info'] = msg

    def warning(self, msg):
        self.messages['warning'] = msg

    def error(self, msg):
        self.messages['error'] = msg

    def critical(self, msg):
        self.messages['critical'] = msg


class FakeApp(object):
    def __init__(self, _stdout, _log):
        self.stdout = _stdout
        self.client_manager = None
        self.stdin = sys.stdin
        self.stdout = _stdout or sys.stdout
        self.stderr = sys.stderr
        self.log = _log


class FakeClient(object):
    def __init__(self, **kwargs):
        self.endpoint = kwargs['endpoint']
        self.token = kwargs['token']


class FakeClientManager(object):
    def __init__(self):
        self.compute = None
        self.identity = None
        self.image = None
        self.object_store = None
        self.volume = None
        self.network = None
        self.session = None
        self.auth_ref = None
        self.auth_plugin_name = None

    def get_configuration(self):
        return {
            'auth': {
                'username': USERNAME,
                'password': PASSWORD,
                'token': AUTH_TOKEN,
            },
            'region': REGION_NAME,
            'identity_api_version': VERSION,
        }


class FakeModule(object):
    def __init__(self, name, version):
        self.name = name
        self.__version__ = version


class FakeResource(object):
    def __init__(self, manager=None, info={}, loaded=False, methods={}):
        """Set attributes and methods for a resource.

        :param manager:
            The resource manager
        :param Dictionary info:
            A dictionary with all attributes
        :param bool loaded:
            True if the resource is loaded in memory
        :param Dictionary methods:
            A dictionary with all methods
        """
        self.__name__ = type(self).__name__
        self.manager = manager
        self._info = info
        self._add_details(info)
        self._add_methods(methods)
        self._loaded = loaded

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            setattr(self, k, v)

    def _add_methods(self, methods):
        """Fake methods with MagicMock objects.

        For each <@key, @value> pairs in methods, add an callable MagicMock
        object named @key as an attribute, and set the mock's return_value to
        @value. When users access the attribute with (), @value will be
        returned, which looks like a function call.
        """
        for (name, ret) in six.iteritems(methods):
            method = mock.MagicMock(return_value=ret)
            setattr(self, name, method)

    def __repr__(self):
        reprkeys = sorted(k for k in self.__dict__.keys() if k[0] != '_' and
                          k != 'manager')
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)


class FakeResponse(requests.Response):
    def __init__(self, headers={}, status_code=200, data=None, encoding=None):
        super(FakeResponse, self).__init__()

        self.status_code = status_code

        self.headers.update(headers)
        self._content = json.dumps(data)
        if not isinstance(self._content, six.binary_type):
            self._content = self._content.encode()


class FakeModel(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)


class FakeServer(object):
    """Fake one or more compute servers."""

    @staticmethod
    def create_one_server(attrs={}, methods={}):
        """Create a fake server.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param Dictionary methods:
            A dictionary with all methods
        :return:
            A FakeResource object, with id, name, metadata
        """
        # Set default attributes.
        server_info = {
            'id': 'server-id-' + uuid.uuid4().hex,
            'name': 'server-name-' + uuid.uuid4().hex,
            'metadata': {},
        }

        # Overwrite default attributes.
        server_info.update(attrs)

        server = FakeResource(info=copy.deepcopy(server_info),
                              methods=methods,
                              loaded=True)
        return server

    @staticmethod
    def create_servers(attrs={}, methods={}, count=2):
        """Create multiple fake servers.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param Dictionary methods:
            A dictionary with all methods
        :param int count:
            The number of servers to fake
        :return:
            A list of FakeResource objects faking the servers
        """
        servers = []
        for i in range(0, count):
            servers.append(FakeServer.create_one_server(attrs, methods))

        return servers

    @staticmethod
    def get_servers(servers=None, count=2):
        """Get an iterable MagicMock object with a list of faked servers.

        If servers list is provided, then initialize the Mock object with the
        list. Otherwise create one.

        :param List servers:
            A list of FakeResource objects faking servers
        :param int count:
            The number of servers to fake
        :return:
            An iterable Mock object with side_effect set to a list of faked
            servers
        """
        if servers is None:
            servers = FakeServer.create_servers(count)
        return mock.MagicMock(side_effect=servers)
