from django.http import HttpResponse
from django.shortcuts import render
from app.models import Customer
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView


def index(request):
    customers_list = Customer.objects.order_by('date_submitted')
    return render(request, 'app/index.html', {'customers_list': customers_list})


def test(request):
    return HttpResponse("You loaded the test page")


class CustomerDetail(DetailView):
    model = Customer
    template_name = "app/detail.html"


class CustomerUpdate(UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'service_description', 'price', 'completed', 'date_submitted']
    template_name = "app/edit.html"
    success_url = "/" # TODO find out how to insert pk