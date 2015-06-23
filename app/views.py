from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from app.models import Transaction, Task
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DetailView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from django.contrib.auth import authenticate, login, logout
from app.forms import TasksForm, RepairsForm
from django.template import RequestContext
from django import forms

NEW_ORDER_TEMPLATES = {'0': 'app/create_transaction.html', '1': 'app/create_transaction.html'}

def test(request):
    """
    A very simple page that just renders to test url routing
    """
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
    """
    This class handles user authentication for all of the class-based views I use
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class TransactionDetail(LoggedInMixin, DetailView):
    model = Transaction
    template_name = "app/detail.html"

    def get_context_data(self, **kwargs):
        context = super(TransactionDetail, self).get_context_data(**kwargs)
        context['tasks'] = Transaction.objects.filter(pk=self.kwargs['pk']).first().task_set.all()
        return context


def update(request, *args, **kwargs):
    # model = Transaction
    # template_name = "app/edit.html"

    tasks = Transaction.objects.filter(pk=kwargs['pk']).first().task_set.all()

    if request.method == 'POST':
        url = u"/%s" % kwargs['pk']
        if "cancel" in request.POST:
            return HttpResponseRedirect(url)
        else:
            print request.POST

            posted_strings = [str(key) for key in request.POST]
            print posted_strings

            for task in tasks:
                print "task.name = " + task.name

                if task.name in posted_strings:
                    print task.name + " in posted_strings"
                    task.completed = True
                else:
                    task.completed = False
                task.save()
            return HttpResponseRedirect(url)

    return render_to_response("app/edit.html", {'tasks': tasks}, context_instance=RequestContext(request))


def process(form_data):
    print form_data
    new_transaction = Transaction(
        first_name=form_data[0]['first_name'],
        last_name=form_data[0]['last_name'],
        email=form_data[0]['email'],
        affiliation=form_data[0]['affiliation'],
        price=form_data[1]['price'],
        service_description=form_data[1]['service_description']
    )
    new_transaction.save()

    all_tasks = TasksForm().fields.keys()
    print "form_data[1] = "
    print form_data[1]

    for name in all_tasks:
        if name in form_data[1]:
            task = Task(
                name=name,
                completed=False,
                price=form_data[1]['price'],
                transaction=new_transaction
            )
            task.save()


    if not form_data[0]['no_receipt']: # send receipt by default. the employee must check the box to not send.
        send_receipt_email(new_transaction)


class TransactionWizard(SessionWizardView):
    """
    Wizard view for creating a new transaction in two steps. 
    """
    def get_template_names(self):
        return [NEW_ORDER_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(TransactionWizard, self).get_context_data(form=form, **kwargs)

        if self.steps.current == '1':
            info_dict = TasksForm.get_info_dict()
            context.update({'info_dict': info_dict})

        return context

    def done(self, form_list, **kwargs):
        # form_data is a list of dicts (one for each form in the wizard)

        form_data = list()
        form_data.append(form_list[0].cleaned_data)
        form_data.append({})

        info_dict = TasksForm.get_info_dict()
        for field in form_list[1].cleaned_data:
            print form_list[1].cleaned_data[field]
            if form_list[1].cleaned_data[field] != False:
                print "IN"
                if field in info_dict:
                    form_data[1][field] = info_dict[field]
                else:
                    form_data[1][field] = form_list[1].cleaned_data[field]

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













