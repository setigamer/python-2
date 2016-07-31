import logging
import tornado
import pubnub as pn

from tornado.testing import AsyncTestCase
from pubnub.models.consumer.common import PNStatus
from pubnub.models.consumer.pubsub import PNPublishResult
from pubnub.pubnub_tornado import PubNubTornado, TornadoEnvelope
from tests.helper import pnconf_ssl_copy

pn.set_stream_logger('pubnub', logging.DEBUG)

ch = "tornado-int-publish"


class TestPubNubAsyncPublish(AsyncTestCase):
    @tornado.testing.gen_test
    def test_publish_ssl(self):
        pubnub = PubNubTornado(pnconf_ssl_copy())
        pubnub.set_ioloop(self.io_loop)
        msg = "hey"
        pub = pubnub.publish().channel(ch).message(msg)

        envelope = yield pub.future()

        assert isinstance(envelope, TornadoEnvelope)
        assert isinstance(envelope.result, PNPublishResult)
        assert isinstance(envelope.status, PNStatus)
        assert envelope.result.timetoken > 0
        assert len(envelope.status.original_response) > 0

        pubnub.stop()
