from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from app.models import Transaction, Status
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DetailView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from django.contrib.auth import authenticate, login, logout
from app.forms import CustomerForm, RepairsForm, UserForm
from django.template import RequestContext
from django import forms

NEW_ORDER_TEMPLATES = {'0': 'app/create_transaction.html', '1': 'app/create_transaction.html'}

def test(request):
    return HttpResponse("You've loaded the test page")

@login_required
def index(request):
    transactions_list = Transaction.objects.filter(completed=False).order_by('date_submitted').reverse
    return render(request, 'app/index.html', {'transactions_list': transactions_list, 'complete': False})

@login_required
def history(request):
    transactions_list = Transaction.objects.filter(completed=True).order_by('date_submitted')
    return render(request, 'app/index.html', {'transactions_list': transactions_list, 'complete': True})


@login_required
def mark_as_completed(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.completed = True
    transaction.save()
    send_completion_email(transaction)
    return HttpResponseRedirect(reverse('app:index'))

def send_receipt_email(transaction):
    '''
    Sends a form receipt to the customer's email address.
    '''
    email_address = transaction.email
    subject_line = "Rice Bikes receipt"
    body = "%s, this is your receipt for your order placed on %s. Here are the details:\n %s\nPrice: %s" \
    % (transaction.first_name, transaction.date_submitted, transaction.service_description, transaction.price)
    email = EmailMessage(subject_line, body, to=[email_address])
    email.send(fail_silently=False)

def send_completion_email(transaction):
    email_address = transaction.email
    subject_line = "Rice Bikes status update"
    body = "%s, your bike is available at Rice Bikes. Please come pick it up at your earliest convenience." \
           % (transaction.first_name)
    email = EmailMessage(subject_line, body, to=[email_address])
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
    fields = ['brakes', 'frame', 'handlebars']
    template_name = "app/myEdit.html"
    form_class = RepairsForm

    def get_success_url(self):
        return u"/%s" % self.kwargs['pk']

    def post(self, request, *args, **kwargs):
        # print request
        print kwargs
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(TransactionUpdate, self).post(request, *args, **kwargs)


    # def get_initial(self):
    #     initial = {}
    #     for field in self.fields:
    #         my_field = str(field)
    #         model_info = str(self.get_queryset().filter(pk=self.kwargs['pk']).values()[0][str(my_field)])
    #         if model_info == 'IN_PROGRESS':
    #             field = 'IN_PROGRESS'
    #         elif model_info == 'COMPLETE':
    #             initial[my_field] = 'COMPLETE'
    #         print field
    #     return initial

def process(form_data):
    print form_data
    new_transaction = Transaction(
        first_name=form_data[0]['first_name'],
        last_name=form_data[0]['last_name'],
        email=form_data[0]['email'],
        affiliation=form_data[0]['affiliation'],
        price=form_data[1]['price'])
    new_transaction.service_description = form_data[1]['service_description']
    choices = dict(Status.choices())
    NOT_ASSIGNED = str(Status.NOT_ASSIGNED.value)
    IN_PROGRESS = str(Status.IN_PROGRESS.value)
    new_transaction.handlebars = choices[IN_PROGRESS] if form_data[1]['handlebars'] else \
        choices[NOT_ASSIGNED]
    new_transaction.brakes = choices[IN_PROGRESS] if form_data[1]['brakes'] else \
        choices[NOT_ASSIGNED]
    new_transaction.frame = choices[IN_PROGRESS] if form_data[1]['frame'] else \
        choices[NOT_ASSIGNED]
    if not form_data[0]['receipt']: # send receipt by default. the employee must check the box to not send.
        send_receipt_email(new_transaction)
    else:
        new_transaction.receipt = False
    # new_transaction = Transaction(form_data)
    # print new_transaction.handlebars
    # print new_transaction.brakes
    new_transaction.save()

class TransactionWizard(SessionWizardView):
    """
    Wizard view for creating a new transaction in two steps. 
    """
    def get_template_names(self):
        return [NEW_ORDER_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # form_data is a list of dicts (one for each form in the wizard)
        form_data = [form.cleaned_data for form in form_list]
        # print form_data
        process(form_data)
        return render_to_response('app/confirm.html', {'form_data': form_data})

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                print "Logging in to active account!"
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login credentials: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('registration/login.html', {}, context)


def user_logout(request):
    logout(request)
    context = RequestContext(request)
    return render_to_response('registration/logout.html', {}, context)













