from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if not form.is_valid():
            return render(request, 'subscriptions/subscription_form.html',
                          {'form': form})

        subscription = form.save()

        body = render_to_string('subscriptions/subscription_email.txt',
                                {'subscription' : subscription})

        mail.send_mail('Confirmação de inscrição',
                       body,
                       'contato@eventex.com.br',
                       ['contato@eventex.com', form.cleaned_data['email']]
        )

        return HttpResponseRedirect(r('subscriptions:detail', subscription.pk))

    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html',
                  {'subscription': subscription})