from django.test import SimpleTestCase, tag

from openlxp_notifications.models import (ReceiverEmailConfiguration,
                                          SenderEmailConfiguration,
                                          EmailConfiguration)


@tag('unit')
class ModelTests(SimpleTestCase):

    def test_create_sender_email_config(self):
        """Test that creating a new Sender Email Configuration entry is
        successful with defaults """
        sender_email_address = 'example@test.com'

        sender_email_Config = SenderEmailConfiguration(
            sender_email_address=sender_email_address)

        self.assertEqual(sender_email_Config.sender_email_address,
                         sender_email_address)

    def test_create_receiver_email_config(self):
        """Test that creating a new Receiver Email Configuration entry is
        successful with defaults """
        email_address = 'example@test.com'

        receiver_email_Config = ReceiverEmailConfiguration(
            email_address=email_address)

        self.assertEqual(receiver_email_Config.email_address,
                         email_address)

    def test_create_email_config(self):
        """Test that creating a Email Configuration entry is
        successful with defaults """
        Subject = 'Notifications'
        Email_Content = 'Please find the email'
        Signature = 'OpenLXP'
        Email_Us = 'example@test.com'
        FAQ_URL = 'https.abc.xyz'
        Unsubscribe_Email_ID = 'example@test.com'
        Logs_Type = 'Message'

        email_config = EmailConfiguration(
            Subject=Subject, Email_Content=Email_Content,
            Signature=Signature, Email_Us=Email_Us, FAQ_URL=FAQ_URL,
            Unsubscribe_Email_ID=Unsubscribe_Email_ID, Logs_Type=Logs_Type)

        self.assertEqual(email_config.Subject,
                         Subject)
        self.assertEqual(email_config.Email_Content,
                         Email_Content)
        self.assertEqual(email_config.Signature,
                         Signature)
        self.assertEqual(email_config.Email_Us,
                         Email_Us)
        self.assertEqual(email_config.FAQ_URL,
                         FAQ_URL)
        self.assertEqual(email_config.Unsubscribe_Email_ID,
                         Unsubscribe_Email_ID)
        self.assertEqual(email_config.Logs_Type,
                         Logs_Type)
