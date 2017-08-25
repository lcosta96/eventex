from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """ Get '/inscricao/ must return status code 200 """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """ Must use 'subscriptions/subscription_form.html' """
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """ HTML must contain input tags """
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csfr(self):
        """ HTML must contain csfr"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have subscription form """
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """ Form must have 4 fields """
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

    def test_cfp_is_digit(self):
        """ CFP must only accept digits """
        form = self.make_validated_form(cpf='ABCD567890')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_eleven_digits(self):
        """ CPF must have 11 digits """
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """ Name must be capitalized """
        form = self.make_validated_form(name='JOHN doe')
        self.assertEqual('John Doe', form.cleaned_data['name'])


    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def make_validated_form(self, **kwargs):
        valid = dict(name='John Doe', cpf='12345678901',
                     email='johndoe@email.com', phone='98-984743028')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form
