from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if not form.is_valid():
            return render(request, 'subscriptions/subscription_form.html',
                          {'form': form})

        form.full_clean()
        body = render_to_string('subscriptions/subscription_email.txt',
                                form.cleaned_data)
        mail.send_mail('Confirmação de inscrição',
                       body,
                       'contato@eventex.com.br',
                       ['contato@eventex.com', form.cleaned_data['email']]
        )
        Subscription.objects.create(**form.cleaned_data)

        messages.success(request, 'Inscrição realizada com sucesso!')

        return HttpResponseRedirect('/inscricao/')

    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)
