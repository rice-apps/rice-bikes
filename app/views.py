from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from app.forms import CustomerForm, RepairsForm
from app.models import Customer, Service, Part

NEW_ORDER_TEMPLATES = {'0': 'app/create_customer.html', '1': 'app/repairs.html', '2': 'app/parts.html'}


def test(request):
    """
    A very simple page that just renders to test url routing
    """
    return HttpResponse("You've loaded the test page")

@login_required
def index(request):
    """
    Displays a table of all active Customers
    """
    customers_list = Customer.objects.filter(completed=False).order_by('date_submitted')
    return render(request, 'app/index.html', {'customers_list': customers_list})

@login_required
def mark_as_completed(request, customer_id):
    """
    Called when the user marks a customer's case as completed, and sends an email to the customer
    """
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.completed = True
    customer.save()
    send_completion_email(customer)
    return HttpResponseRedirect(reverse('app:index'))

@login_required
def send_completion_email(customer):
    """
    Forms and send the email for when a customer is marked as completed
    """
    email = customer.email
    subject_line = "Rice Bikes status update"
    body = "%s %s, your bike is available at Rice Bikes. Please come pick it up at your earliest convenience." \
           % (customer.first_name, customer.last_name)
    # print(email, subject_line[:5], body[:5])
    email = EmailMessage(subject_line, body, to=[email])
    email.send(fail_silently=False)


class LoggedInMixin(object):
    """
    This class handles user authentication for all of the class-based views I use
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class CustomerDetail(LoggedInMixin, DetailView):
    """
    Displays all the details about a customer
    """
    model = Customer
    template_name = "app/detail.html"


class CustomerUpdate(UpdateView):
    """
    Displays a form that allows a customer's info to be updated. Redirects to customer's detail page.
    """
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'completed', 'date_submitted']
    template_name = "app/edit.html"

    def get_success_url(self):
        return u"/%s" % self.kwargs['pk']

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(CustomerUpdate, self).post(request, *args, **kwargs)


def process_customer(form):
    customer = Customer()
    customer.first_name = form.first_name
    customer.last_name = form.last_name
    customer.email = form.email
    customer.affiliation = form.affiliation
    customer.save()
    return customer.id


def process_repairs(form, customer_id):
    for category in form.cleaned_data:
        for repair in category:
            service = Service()
            service.type = repair
            service.price = 5
            service.customer = get_object_or_404(Customer, pk=customer_id)
            service.employee_id = get_user_model().employee.id
            service.save()


class CustomerWizard(SessionWizardView):

    def get_template_names(self):
        return [NEW_ORDER_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # print ("HI")
        # print ("Form_List:\n", form_list)
        # print ("Form_List[0]:\n", form_list[0])
        # print ("BYE")

        # customer_id = process_customer(form_list['0'])
        # process_repairs(form_list[1], customer_id)
        return HttpResponseRedirect(reverse('app:index'))