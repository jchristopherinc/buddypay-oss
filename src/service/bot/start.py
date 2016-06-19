from botlayer import EchoLayer
from yowsup.layers import YowParallelLayer
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_media import YowMediaProtocolLayer
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.axolotl import YowAxolotlLayer
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup import env

import ConfigParser
from configreader import FakeSecHead

config = ConfigParser.SafeConfigParser()
config.readfp(FakeSecHead(open('../yowsup.conf')))
PHONE = config.get('asection', 'phone')
PASS = config.get('asection', 'password')

CREDENTIALS = (PHONE, PASS)  # replace with your phone and password

if __name__ == "__main__":
    # import all required stacks
    layers = (
                 EchoLayer,
                 YowParallelLayer(
                         [YowAuthenticationProtocolLayer,
                          YowMessagesProtocolLayer,
                          YowReceiptProtocolLayer,
                          YowMediaProtocolLayer,
                          YowAckProtocolLayer]),
                 YowAxolotlLayer,  # required for reading encrypted messages
             ) + YOWSUP_CORE_LAYERS

    stack = YowStack(layers)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)  # setting credentials
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])  # whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())  # info about us as WhatsApp client

    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))  # sending the connect signal

    stack.loop()  # this is the program mainloop
