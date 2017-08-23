from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})
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


class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        self.data = dict(name='Luciano Costa', cpf='12345678901',
                         email='luciano@costa.com', phone='98-98334-2138')
        self.response =self.client.post('/inscricao/', self.data, follow=True)


    def test_message(self):
        self.assertContains(self.response, 'Inscrição realizada com sucesso!')


