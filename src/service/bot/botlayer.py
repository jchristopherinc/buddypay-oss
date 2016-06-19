from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities import MediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
import vobject

PAY_URL = "http://ngrok2.karthik.xyz/pay"


class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def on_message(self, msg):

        print msg

        # accept only media vcard
        if msg.getType() == TextMessageProtocolEntity.MESSAGE_TYPE_MEDIA and msg.getMediaType() == MediaMessageProtocolEntity.MEDIA_TYPE_VCARD:
            user_info = self.on_contact(msg)
            # msg_reply = TextMessageProtocolEntity(
            #         "hang tight, setting up a transfer to " + user_info['n'],
            #         to=msg.getFrom())
            msg_reply = TextMessageProtocolEntity(
                    "awesome, head over to " + PAY_URL + ", to complete the transaction for " + user_info['n'],
                    to=msg.getFrom())

            self.toLower(msg_reply)

        else:
            # if it isn't a vcard return a message
            msg_reply = TextMessageProtocolEntity(
                    "doesn't seem to be a valid message, try sending a contact ?",
                    to=msg.getFrom())
            self.toLower(msg_reply)

        # send read receipt for message
        receipt = OutgoingReceiptProtocolEntity(
                msg.getId(),
                msg.getFrom(), 'read',
                msg.getParticipant())

        self.toLower(receipt)

    # ack receipt ack, like seriously ??
    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)

    @staticmethod
    def on_contact(msg_vcard):
        # got a contact card
        print("Echoing vcard (%s, %s) to %s" %
              (msg_vcard.getName(),
               msg_vcard.getCardData(),
               msg_vcard.getFrom(False)))

        vcard = vobject.readOne(msg_vcard.getCardData())
        print vcard

        contact_info = {'n': None, 'tel':None}

        for key in contact_info.keys():
            if key in vcard.contents and len(vcard.contents[key]) > 0:
                contact_info[key] = str(vcard.contents[key][0].value).strip()

        print contact_info

        return contact_info
