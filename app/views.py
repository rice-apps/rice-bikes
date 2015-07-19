from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from app.models import Transaction, Task, RentalBike, RefurbishedBike, \
    RevenueUpdate, TotalRevenue
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DetailView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from django.contrib.auth import authenticate, login, logout
from app.forms import TasksForm, RepairsForm, RentalForm, RefurbishedForm, RevenueForm, TransactionForm
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
    return render(request, 'app/index.html', {'transactions_list': transactions_list, 'complete': False, 'home':True})

@login_required
def history(request):
    transactions_list = Transaction.objects.filter(completed=True).order_by('date_submitted').reverse
    return render(request, 'app/history.html', {'transactions_list': transactions_list, 'complete': True})


@login_required
def mark_as_completed(request, pk):
    # save completed transaction
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.completed = True
    transaction.save()

    # send email
    send_completion_email(transaction)

    return HttpResponseRedirect(reverse('app:index'))


def send_completion_email(transaction):
    email_address = transaction.email
    subject_line = "[Rice Bikes] Ready For Pickup"
    tasks = [str(task.name) for task in transaction.task_set.all()]
    task_string = "\n".join(tasks)
    body = "%s,\n\n" \
           " Your bike is ready for pickup! The following repairs were completed:\n" \
           "%s\n\n" \
           "Total: $%d\n\n" \
           "Please pick up your bicycle during our regular business hours (Monday -" \
           "Friday, 2-5pm) within the next 2 business days to avoid a $5 per day storage" \
           " fee. At this time we only accept cash or check payments, but there is an ATM" \
           " machine around the corner from our shop. We hope to see you soon." \
           "\n\n" \
           "-The Rice Bikes Team" \
           % (transaction.first_name, task_string, transaction.price)

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
        context['parent_url'] = self.kwargs['parent_url']
        return context


class TransactionDetailComplete(LoggedInMixin, DetailView):
    model = Transaction
    template_name = "app/detail_complete.html"

    def get_context_data(self, **kwargs):
        context = super(TransactionDetailComplete, self).get_context_data(**kwargs)
        context['tasks'] = Transaction.objects.filter(pk=self.kwargs['pk']).first().task_set.all()
        context['parent_url'] = self.kwargs['parent_url']
        return context


def process_transaction_edit(form_data, transaction, request):

    payment_difference = form_data['amount_paid'] - transaction.amount_paid

    if payment_difference != 0:
        # make revenue update
        if TotalRevenue.objects.count() == 0:
            total_revenue = TotalRevenue(
                total_revenue=0
            )
            total_revenue.save()
        total_revenue = TotalRevenue.objects.first()
        total_revenue.total_revenue += payment_difference
        total_revenue.save()

        revenue_update = RevenueUpdate(
            amount=payment_difference,
            employee=request.user.get_username(),
            transaction=transaction,
            new_total_revenue=total_revenue.total_revenue,
        )
        revenue_update.save()

    transaction.service_description = form_data['service_description']
    transaction.amount_paid = form_data['amount_paid']
    transaction.price = form_data['price']
    transaction.save()


def update(request, *args, **kwargs):
    # model = Transaction
    # template_name = "app/edit.html"

    transaction = Transaction.objects.filter(pk=kwargs['pk']).first()
    tasks = transaction.task_set.all()

    if request.method == 'POST':
        url = u"/%s/%s/detail" % (kwargs['pk'], kwargs['parent_url'])
        if "cancel" in request.POST:
            return HttpResponseRedirect(url)
        else:
            print request.POST

            posted_strings = [str(key) for key in request.POST]
            print posted_strings

            form = TransactionForm(request.POST)
            if form.is_valid():
                process_transaction_edit(form.cleaned_data, transaction, request)

            for task in tasks:
                print "task.name = " + task.name

                if task.name in posted_strings:
                    print task.name + " in posted_strings"
                    task.completed = True
                else:
                    task.completed = False
                task.save()
            return HttpResponseRedirect(url)

    category_dict = TasksForm.get_category_dict()
    info_dict = TasksForm.get_info_dict()

    transaction_form = TransactionForm(instance=transaction)

    return render_to_response("app/edit.html", {'tasks': tasks, 'category_dict': category_dict, 'info_dict': info_dict,
                                                'transaction_form': transaction_form},
                              context_instance=RequestContext(request))


def rental(request):
    rentals = RentalBike.objects.all().order_by('date_submitted').reverse
    return render(request, "app/rental.html", {'rentals': rentals})


def refurbished(request):
    refurbished_list = RefurbishedBike.objects.all().order_by('date_submitted').reverse
    return render(request, "app/refurbished.html", {'refurbished_list': refurbished_list})


class RentalDetail(LoggedInMixin, DetailView):
    model = RentalBike
    template_name = "app/rental_detail.html"

    def get_context_data(self, **kwargs):
        context = super(RentalDetail, self).get_context_data(**kwargs)
        print "rental kwargs: " + str(self.kwargs)
        context['vin'] = RentalBike.objects.filter(pk=self.kwargs['pk']).first().vin
        context['transactions'] = RentalBike.objects.filter(pk=self.kwargs['pk']).first().transaction_set.all()
        return context


class RefurbishedDetail(LoggedInMixin, DetailView):
    model = RefurbishedBike
    template_name = "app/refurbished_detail.html"

    def get_context_data(self, **kwargs):
        context = super(RefurbishedDetail, self).get_context_data(**kwargs)
        print "refurbished kwargs: " + str(self.kwargs)
        context['vin'] = RefurbishedBike.objects.filter(pk=self.kwargs['pk']).first().vin
        context['transactions'] = RefurbishedBike.objects.filter(pk=self.kwargs['pk']).first().transaction_set.all()
        return context


def process_rental(form_data):
    rental_bike = RentalBike(
        vin=form_data['vin']
    )
    rental_bike.save()


def new_rental(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            process_rental(form.cleaned_data)
            return render_to_response('app/confirm_rental.html', {})
    else:
        form = RentalForm()

    return render(request, 'app/new_rental.html', {
        'form': form,
    })


def process_refurbished(form_data):
    refurbished_bike = RefurbishedBike(
        vin=form_data['vin']
    )
    refurbished_bike.save()


def new_refurbished(request):
    if request.method == 'POST':
        form = RefurbishedForm(request.POST)
        if form.is_valid():
            process_refurbished(form.cleaned_data)
            return render_to_response('app/confirm_refurbished.html', {})
    else:
        form = RefurbishedForm()

    return render(request, 'app/new_refurbished.html', {
        'form': form,
    })


def process(form_data):
    print form_data
    new_transaction = Transaction(
        first_name=form_data[0]['first_name'],
        last_name=form_data[0]['last_name'],
        email=form_data[0]['email'],
        affiliation=form_data[0]['affiliation'],
        price=form_data[1]['price'],
        service_description=form_data[1]['service_description'],
    )

    # map transaction to rental/refurbished bike
    if form_data[1]['rental_vin']:
        rental_bike = RentalBike.objects.filter(vin=form_data[1]['rental_vin']).first()
        if rental_bike is None:
            rental_bike = RentalBike(
                vin=form_data[1]['rental_vin'],
            )
            rental_bike.save()
        new_transaction.rental_bike = rental_bike
    elif form_data[1]['refurbished_vin']:
        refurbished_bike = RefurbishedBike.objects.filter(vin=form_data[1]['refurbished_vin']).first()
        new_transaction.refurbished_bike = refurbished_bike

    new_transaction.save()

    all_tasks = TasksForm().fields.keys()
    print "form_data[1] = "
    print form_data[1]

    # map tasks to this transaction
    for name in all_tasks:
        if name in form_data[1]:
            task = Task(
                name=name,
                completed=False,
                category=form_data[1][name]['category'],
                transaction=new_transaction
            )
            task.save()


class TransactionWizard(SessionWizardView):
    """
    Wizard view for creating a new transaction in two steps.
    """
    def get_template_names(self):
        return [NEW_ORDER_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(TransactionWizard, self).get_context_data(form=form, **kwargs)

        if self.steps.current == '1':
            category_dict = TasksForm.get_category_dict()
            non_task_fields = TasksForm.get_non_task_fields()
            context.update({'category_dict': category_dict})
            context.update({'non_task_fields': non_task_fields})
        return context

    def done(self, form_list, **kwargs):
        # form_data is a list of dicts (one for each form in the wizard)

        form_data = list()
        form_data.append(form_list[0].cleaned_data)
        form_data.append({})

        info_dict = TasksForm.get_info_dict()

        for field in form_list[1].cleaned_data:
            print str(field)
            print "with value "
            print (form_list[1].cleaned_data[field])
            print "end"
            if not (isinstance(form_list[1].cleaned_data[field], bool) and not form_list[1].cleaned_data[field]):
                if field.replace("_", " ") in info_dict:
                    print field + "in info_dict"
                    form_data[1][field] = info_dict[field.replace("_", " ")]
                else:
                    form_data[1][field] = form_list[1].cleaned_data[field]

        print "In done, form_list[1].cleaned_data = "
        form_list[1]

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


def balance(request):
    revenue_updates = RevenueUpdate.objects.all().order_by('date_submitted').reverse()
    return render(request, 'app/balance.html', {'revenue_updates': revenue_updates})


def process_revenue_update(form_data, request):

    if TotalRevenue.objects.count() == 0:
        total_revenue = TotalRevenue(
            total_revenue=0
        )
        total_revenue.save()
    total_revenue = TotalRevenue.objects.first()
    total_revenue.total_revenue += form_data['amount']
    total_revenue.save()

    revenue_update = RevenueUpdate(
        amount=form_data['amount'],
        employee=request.user.get_username(),
        completed_transaction=None,
        description=form_data['description'],
        new_total_revenue=total_revenue.total_revenue,
    )
    revenue_update.save()


def revenue_update(request):
    if request.method == 'POST':
        form = RevenueForm(request.POST)
        if form.is_valid():
            process_revenue_update(form.cleaned_data, request)
            return render_to_response('app/confirm_revenue.html', {})
    else:
        form = RevenueForm()

    return render(request, 'app/revenue_update.html', {
        'form': form,
    })
