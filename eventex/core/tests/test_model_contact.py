from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='John Doe',
            slug='john-doe',
            photo='https://pbs.twimg.com/profile_images/750110556137324544/ANycYL3f_400x400.jpg',
        )

    def test_create(self):
        contact = Contact.objects.create(speaker=self.speaker,kind=Contact.EMAIL,
                                         value='johndoe@email.com',)
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.PHONE,
                                         value='98-984743028', )
        self.assertTrue(Contact.objects.exists())

    def test_choises(self):
        """ Contact kind should be limited to E or P """
        contact = Contact.objects.create(speaker=self.speaker, kind='a', value='b', )
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.EMAIL,
                                         value='johndoe@email.com', )
        self.assertEqual('johndoe@email.com', str(contact))