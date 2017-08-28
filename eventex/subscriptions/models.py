from django.db import models

from eventex.subscriptions.validators import validate_cpf


class Subscription(models.Model):
    name = models.CharField('nome', max_length=100)
    cpf = models.CharField('cpf', max_length=11, validators=[validate_cpf])
    email = models.EmailField('email', blank=True)
    phone = models.CharField('telefone', max_length=20, blank=True)
    paid = models.BooleanField('pago', default=False)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        verbose_name_plural='incrições'
        verbose_name='inscrição'
        ordering = ('-created_at',)


    def __str__(self):
        return self.name