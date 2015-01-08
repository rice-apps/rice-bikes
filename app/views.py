from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from app.models import Customer
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from app.forms import CustomerForm


def index(request):
    print "Index view"
    customers_list = Customer.objects.order_by('date_submitted')
    return render(request, 'app/index.html', {'customers_list': customers_list})


def detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    form = CustomerForm(instance=customer)
    return render(request, 'app/detail.html', {
        'customer': customer,
        'form': form,
    })


class CustomerUpdate(UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'service_description', 'price', 'completed', 'date_submitted']
    template_name = "app/detail.html"
    success_url = "/app"