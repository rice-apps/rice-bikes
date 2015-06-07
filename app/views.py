from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from app.models import Transaction
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DetailView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from django.contrib.auth import get_user_model
from app.forms import CustomerForm, RepairsForm

NEW_ORDER_TEMPLATES = {'0': 'app/create_customer.html', '1': 'app/new_repair.html'}

def test(request):
    return HttpResponse("You've loaded the test page")

@login_required
def index(request):
    transactions_list = Transaction.objects.filter(completed=False).order_by('date_submitted')
    return render(request, 'app/index.html', {'transactions_list': transactions_list})

@login_required
def mark_as_completed(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    transaction.completed = True
    transaction.save()
    send_completion_email(transaction)
    return HttpResponseRedirect(reverse('app:index'))

@login_required
def send_completion_email(transaction):
    email = transaction.email
    subject_line = "Rice Bikes status update"
    body = "%s %s, your bike is available at Rice Bikes. Please come pick it up at your earliest convenience." \
           % (transaction.first_name, transaction.last_name)
    print(email, subject_line[:5], body[:5])
    email = EmailMessage(subject_line, body, to=[email])
    email.send(fail_silently=False)


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class TransactionDetail(LoggedInMixin, DetailView):
    model = Transaction
    template_name = "app/detail.html"


class TransactionUpdate(UpdateView):
    model = Transaction
    fields = ['first_name', 'last_name', 'email', 'service_description', 'price', 'completed', 'date_submitted']
    template_name = "app/edit.html"

    def get_success_url(self):
        return u"/%s" % self.kwargs['pk']

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(TransactionUpdate, self).post(request, *args, **kwargs)

def process(form_data):
    new_transaction = Transaction(
        first_name = form_data[0]['first_name'],
        last_name = form_data[0]['last_name'],
        email = form_data[0]['email'],
        affiliation = form_data[0]['affiliation'],
        price = form_data[1]['price'])
    new_transaction.save()

class TransactionWizard(SessionWizardView):
    """
    wizard view for creating a new transaction in two steps. 
    """

    def get_template_names(self):
        return [NEW_ORDER_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # form_data is a list of dicts (one for each form in the wizard)
        form_data = [form.cleaned_data for form in form_list]
        process(form_data)
        return render_to_response('app/confirm.html', {'form_data': form_data})

