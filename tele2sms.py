# -*- coding: utf-8 -*-
import re
from urllib import urlencode
import urllib2

class Tele2SMS:
    _address = 'https://secure.eurobate.com/tele2no/sms.php'
    _max_length = 480
    _re_valid_number = re.compile("(4|9)[0-9]{7}")
    _re_response_check = re.compile("Din melding er sendt til")
    id = None
    sender = None

    def __init__(self, id, sender):
        """ Usage: Tele2SMS(id, sender)
        Where id = Tele2 Eurobate ID (find in iframe URL on Tele2 send-sms-page)
        and sender = cell number for the Tele2 account."""
        if id is None:
            raise ValueError("id cannot be None.")
        if sender is None:
            raise ValueError("sender cannot be None.")

        if not self.is_valid_number(sender):
            raise ValueError("Invalid sender number.")

        self.id = id
        self.sender = sender

    def send(self, recipients, message, alfa_sender=None):
        """ Sends an SMS.
        Usage: send(recipients, message, alfa_sender)
        Where recipients is a string of the reciever cell number, or a list of several recipients,
        message is the message to send
        and alfa_sender is the 'sender' string that will appear for recipient. Ex: 'Matt' or a number
        alfa_sender can be omitted and will default to the sms account number.
        """
 
        if message is None:
            raise ValueError("message cannot be None.")
        if len(message) > self._max_length:
            raise ValueError("Message cannot be over 480 chars.")

        if alfa_sender is None:
            alfa_sender = self.sender

        if type(recipients) != 'list':
            recipients = [recipients,]

        for number in recipients:
            if not self.is_valid_number(number):
                raise ValueError("Invalid recipient number: %s" % number)

        data = urlencode({
                'id': self.id,
                'avsender': self.sender,
                'MessageSMS': message,
                'avsender_alfa': alfa_sender,
                'mottaker': ','.join(recipients)
            })

        request = urllib2.Request(url=self._address, data=data)
        response = urllib2.urlopen(request)

        if self._re_response_check.search(response.read()) is not None:
            return True
        else:
            # TODO: error msg?
            return False


    def is_valid_number(self, number):
        if self._re_valid_number.match(number) is not None:
            return True
        else:
            return False
