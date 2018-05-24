# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import mock
from botocore.vendored.requests import ConnectionError

from tests import BaseSessionTest
from botocore.config import Config
from botocore.exceptions import ConnectionClosedError
from botocore.exceptions import EndpointConnectionError


class TestConnectionExceptions(BaseSessionTest):
    def setUp(self):
        super(TestConnectionExceptions, self).setUp()
        self.client = self.session.create_client(
            'ec2', 'us-west-2',
            config=Config(retries={'max_attempts': 0})
        )
        self.fake_request = mock.Mock(
            url='https://ec2.us-west-2.amazonaws.com')

    def test_raises_endpoint_connection_error(self):
        connection_error = ConnectionError(
            "Fake gaierror(8, node or host not known)",
            request=self.fake_request)
        with mock.patch('botocore.endpoint.Session.send') as mock_send:
            mock_send.side_effect = connection_error
            with self.assertRaises(EndpointConnectionError):
                self.client.describe_regions()

    def test_raises_connection_closed_error(self):
        connection_error = ConnectionError(
            """'Connection aborted.', BadStatusLine("''",)""",
            request=self.fake_request)
        with mock.patch('botocore.endpoint.Session.send') as mock_send:
            mock_send.side_effect = connection_error
            with self.assertRaises(ConnectionClosedError):
                self.client.describe_regions()

    def test_raises_general_connection_error(self):
        connection_error = ConnectionError(
            'Unhandled connection exception', request=self.fake_request)
        with mock.patch('botocore.endpoint.Session.send') as mock_send:
            mock_send.side_effect = connection_error
            with self.assertRaises(ConnectionError):
                self.client.describe_regions()
