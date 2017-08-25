from django.test import TestCase
from django.core import mail
from django.shortcuts import resolve_url as r


class SubscribePostTest(TestCase):
    def setUp(self):
        self.data = dict(name='Luciano Costa', cpf='12345678901',
                    email='luciano@costa.com', phone='98-98334-2138')
        self.response = self.client.post(r('subscriptions:new'), self.data)
        self.email = mail.outbox[0]


    def test_post(self):
        """ Valid POST should redirect to '/inscricao/' """
        self.assertEqual(302, self.response.status_code)


    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)


    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)


    def test_subscription_email_to(self):
        expect = [
            'contato@eventex.com',
            self.data['email'],
        ]
        self.assertEqual(expect, self.email.to)


    def test_subscription_email_body(self):
        self.assertIn(self.data['name'], self.email.body)
        self.assertIn(self.data['cpf'], self.email.body)
        self.assertIn(self.data['email'], self.email.body)
        self.assertIn(self.data['phone'], self.email.body)
