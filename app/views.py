from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from app.models import Customer
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView


def index(request):
    customers_list = Customer.objects.order_by('date_submitted')
    return render(request, 'app/index.html', {'customers_list': customers_list})


def test(request):
    return HttpResponse("You've loaded the test page")


def send_customer_email(request, customer_id):
    customer = get_object_or_404(Customer, customer_id)
    email = customer.email
    subject_line = "Rice Bikes status update"
    content = u"%s %s, your bike is available at Rice Bikes. Please come pick it up at your earliest convenience." \
              % customer.first_name % customer.last_name
    # TODO send email using send_email or whatever, I can't remember because I'm on a plane if anyone is looking at this


class CustomerDetail(DetailView):
    model = Customer
    template_name = "app/detail.html"


class CustomerUpdate(UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'service_description', 'price', 'completed', 'date_submitted']
    template_name = "app/edit.html"

    def get_success_url(self):
        return  u"/%s" % self.kwargs['pk']