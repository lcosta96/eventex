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

    def test_email_is_optional(self):
        """ Email is optional """
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """ Phone is optional """
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """ Email and Phone are optional, but one must be informed """
        form = self.make_validated_form(email='', phone='')
        self.assertListEqual(['__all__'], list(form.errors))

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


class FormRegressionTest(TestCase):
    def test_send_wrong_email_and_empty_phone(self):
        """ Email and Phone are optional, but email, if inserted, must be valid """
        invalid_data = dict(name='John Doe', cpf='12345678901',
                            email='johndoe', phone='')
        form = SubscriptionForm(invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)