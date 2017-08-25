from django.test import TestCase
from django.core import mail
from django.shortcuts import resolve_url as r
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionNewPostValid(TestCase):
    def setUp(self):
        self.data = dict(name='Luciano Costa', cpf='12345678901',
                    email='luciano@costa.com', phone='98-98334-2138')
        self.response = self.client.post(r('subscriptions:new'), self.data)
        self.email = mail.outbox[0]


    def test_post(self):
        """ Valid POST should redirect to '/inscricao/1/' """
        self.assertRedirects(self.response, r('subscriptions:detail', 1))


    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post(r('subscriptions:new'), {})
        self.form = self.response.context['form']


    def test_post(self):
        """ Invalid POST should not redirect """
        self.assertEqual(200, self.response.status_code)


    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')


    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)


    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)


    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())

