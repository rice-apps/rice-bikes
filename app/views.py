from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from app.models import Customer
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def test(request):
    return HttpResponse("You've loaded the test page")

@login_required
def index(request):
    customers_list = Customer.objects.filter(completed=False).order_by('date_submitted')
    return render(request, 'app/index.html', {'customers_list': customers_list})

@login_required
def mark_as_completed(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.completed = True
    customer.save()
    send_completion_email(customer)
    return HttpResponseRedirect(reverse('app:index'))

@login_required
def send_completion_email(customer):
    email = customer.email
    subject_line = "Rice Bikes status update"
    body = "%s %s, your bike is available at Rice Bikes. Please come pick it up at your earliest convenience." \
           % (customer.first_name, customer.last_name)
    print(email, subject_line[:5], body[:5])
    email = EmailMessage(subject_line, body, to=[email])
    email.send(fail_silently=False)


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class CustomerDetail(LoggedInMixin, DetailView):
    model = Customer
    template_name = "app/detail.html"


class CustomerUpdate(UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'service_description', 'price', 'completed', 'date_submitted']
    template_name = "app/edit.html"

    def get_success_url(self):
        return u"/%s" % self.kwargs['pk']

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(CustomerUpdate, self).post(request, *args, **kwargs)