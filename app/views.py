from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from app.models import Transaction, Task, RentalBike, RefurbishedBike, \
    RevenueUpdate, TotalRevenue, PartCategory, PartOrder, MenuItem, MiscRevenueUpdate
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DetailView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from django.contrib.auth import authenticate, login, logout
from app.forms import RentalForm, RefurbishedForm, RevenueForm, TaskForm, PartCategoryForm, \
    PartOrderForm, CustomerForm, DisabledPartCategoryForm, MiscRevenueUpdateForm
from django.template import RequestContext
from django import forms
import csv

NEW_ORDER_TEMPLATES = {'0': 'app/create_transaction.html', '1': 'app/create_transaction.html',
                       '2': 'app/create_trans_parts.html'}


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
def mark_as_completed(request, **kwargs):
    # save completed transaction
    pk = kwargs['trans_pk']
    num_parent_args = kwargs['num_parent_args']

    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.completed = True
    transaction.save()

    # send email
    send_completion_email(transaction)

    url = get_url(num_parent_args, kwargs)

    return HttpResponseRedirect(url)  # want to go back to parent_url, not always index


def send_completion_email(transaction):
    email_address = transaction.email
    subject_line = "[Rice Bikes] Ready For Pickup"
    tasks = [str(task.menu_item.name) for task in transaction.task_set.all()]
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
           % (transaction.first_name, task_string, transaction.cost)

    email = EmailMessage(subject_line, body, to=[email_address])
    email.send(fail_silently=False)


class LoggedInMixin(object):
    """
    This class handles user authentication for all of the class-based views I use
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)

@login_required
def detail(request, **kwargs):

    transaction = Transaction.objects.filter(pk=kwargs['trans_pk']).first()
    tasks = transaction.task_set.all()
    part_categories = transaction.partcategory_set.all()
    parent_url = kwargs['parent_url']
    num_parent_args = kwargs['num_parent_args']
    bike_pk = None
    if 'bike_pk' in kwargs:
        bike_pk = kwargs['bike_pk']

    if transaction.completed:
        detail_page = 'detail_complete.html'
    else:
        detail_page = 'detail.html'

    return render_to_response("app/" + detail_page, {
        'transaction':transaction,
        'part_categories': part_categories,
        'parent_url': parent_url,
        'tasks': tasks,
        'num_parent_args': num_parent_args,
        'bike_pk': bike_pk,
        })


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

    if transaction:
        transaction.service_description = form_data['service_description']
        transaction.amount_paid = form_data['amount_paid']
        transaction.cost = form_data['cost']
        transaction.save()


def process_misc_trans_update(form_data, misc_update, request):

    payment_difference = form_data['amount']

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
            misc_revenue_update=misc_update,
            new_total_revenue=total_revenue.total_revenue,
        )
        revenue_update.save()


def process_part_category_forms(form_input_data, transaction):
    """ Processes form data for multiple PartCategoryForms, putting the
    resulting list of dictionaries into form_list."""

    # build the forms by iterating over the MultiValueDict
    fields = PartCategory._meta.get_all_field_names()
    non_saved_fields = ['id', 'date_submitted', 'transaction', 'transaction_id']
    fields = [el for el in fields if el not in non_saved_fields]

    s = 'category'
    print form_input_data
    num_forms = len(form_input_data.getlist(s))
    print num_forms

    print 'fields = ' + str(fields)

    # delete old PartCategories
    transaction.partcategory_set.all().delete()

    # save new PartCategories
    for i in xrange(num_forms):
        new_part_category = PartCategory()
        print "NEW PART CATEGORY: "

        for field in fields:
            value = form_input_data.getlist(field)[i]
            if field == "was_used" and value == "False":
                value = False
            if field == "price" and value == "":
                value = 0
            setattr(new_part_category, field, value)
            print "field = " + str(field)
            print "value = " + str(getattr(new_part_category, field))
        print "END"

        new_part_category.transaction = transaction
        new_part_category.save()


def get_items_by_category():
    category_tuples = MenuItem.objects.values_list('category').distinct()
    items_by_category = dict()
    for category_tuple in category_tuples:
        category = category_tuple[0]
        items_by_category[category] = list(MenuItem.objects.filter(category=category))

    return items_by_category


def get_url(num_parent_args, kwargs):
    if num_parent_args == 1:
        url = u"/%s/%s/detail" % (kwargs['parent_url'], kwargs['trans_pk'])
    else:
        url = u"/%s/%s/%s/detail" % (kwargs['bike_pk'], kwargs['parent_url'], kwargs['trans_pk'])

    return url

@login_required
def update(request, **kwargs):
    # model = Transaction
    # template_name = "app/edit.html"

    transaction = Transaction.objects.filter(pk=kwargs['trans_pk']).first()
    tasks = transaction.task_set.all()
    part_categories = transaction.partcategory_set.all()

    if request.method == 'POST':
        num_parent_args = kwargs['num_parent_args']
        url = get_url(num_parent_args, kwargs)
        if "cancel" in request.POST:
            return HttpResponseRedirect(url)
        else:
            print request.POST

            posted_strings = [str(key) for key in request.POST]
            print posted_strings

            form = TaskForm(request.POST)
            if form.is_valid():
                process_transaction_edit(form.cleaned_data, transaction, request)

            form = PartCategoryForm(request.POST)
            if form.is_valid():
                process_part_category_forms(form.data, transaction)

            for task in tasks:
                task_name = task.menu_item.name
                if task_name.replace(" ", "_") in posted_strings:
                    print task_name + " in posted_strings"
                    task.completed = True
                else:
                    task.completed = False
                task.save()
            return HttpResponseRedirect(url)

    # get list of all unique categories
    category_tuples = MenuItem.objects.values_list('category').distinct()
    categories = [tup[0] for tup in category_tuples]

    transaction_form = TaskForm(instance=transaction)

    part_category_form_list = []
    for part_category in part_categories:
        part_category_form = PartCategoryForm(instance=part_category)
        print dir(part_category_form)
        part_category_form_list.append(part_category_form)

    # new form
    new_category_form = PartCategoryForm()

    return render_to_response("app/edit.html", {'part_category_form_list': part_category_form_list, 'tasks': tasks,
                                                'categories': categories,
                                                'transaction_form': transaction_form,
                                                'new_category_form': new_category_form},
                              context_instance=RequestContext(request))

@login_required
def rental(request):
    rentals = RentalBike.objects.all().order_by('date_submitted').reverse
    return render(request, "app/rental.html", {'rentals': rentals})

@login_required
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
        context['bike_pk'] = self.kwargs['pk']
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RentalDetail, self).dispatch(*args, **kwargs)


class RefurbishedDetail(LoggedInMixin, DetailView):
    model = RefurbishedBike
    template_name = "app/refurbished_detail.html"

    def get_context_data(self, **kwargs):
        context = super(RefurbishedDetail, self).get_context_data(**kwargs)
        print "refurbished kwargs: " + str(self.kwargs)
        context['vin'] = RefurbishedBike.objects.filter(pk=self.kwargs['pk']).first().vin
        context['transactions'] = RefurbishedBike.objects.filter(pk=self.kwargs['pk']).first().transaction_set.all()
        context['bike_pk'] = self.kwargs['pk']
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RefurbishedDetail, self).dispatch(*args, **kwargs)


def process_rental(form_data):
    rental_bike = RentalBike(
        vin=form_data['vin']
    )
    rental_bike.save()


@login_required
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


@login_required
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
    print "PROCESSING create-transaction forms"
    print form_data
    new_transaction = Transaction(
        first_name=form_data[0]['first_name'],
        last_name=form_data[0]['last_name'],
        email=form_data[0]['email'],
        affiliation=form_data[0]['affiliation'],
        cost=form_data[0]['cost'],
        service_description=form_data[0]['service_description'],
    )

    # map transaction to rental/refurbished bike
    rental_vin = form_data[0]['rental_vin']
    refurbished_vin = form_data[0]['refurbished_vin']
    if rental_vin:
        rental_bike = RentalBike.objects.filter(vin=rental_vin).first()
        if rental_bike is None:
            rental_bike = RentalBike(
                vin=rental_vin,
            )
            rental_bike.save()
        new_transaction.rental_bike = rental_bike
    elif refurbished_vin:
        refurbished_bike = RefurbishedBike.objects.filter(vin=refurbished_vin).first()
        if refurbished_bike is None:
            refurbished_bike = RefurbishedBike(
                vin=refurbished_vin,
            )
            refurbished_bike.save()
        new_transaction.refurbished_bike = refurbished_bike

    new_transaction.save()

    print "form_data[1] = "
    print form_data[1]

    # map tasks to this transaction
    for menu_item in form_data[1]:
        task = Task(
            completed=False,
            transaction=new_transaction,
            menu_item=menu_item,
        )
        task.save()

    # map parts to this transaction
    for form in form_data[2]:
        if (form['was_used'] == 'True'):
            was_used = True
        else:
            was_used = False
        part_category = PartCategory(
            category=form['category'],
            price=form['price'],
            description=form['description'],
            was_used=was_used,
            transaction=new_transaction,
        )
        part_category.save()


def process_transaction(form_data):
    new_transaction = Transaction(
        first_name=form_data['first_name'],
        last_name=form_data['last_name'],
        email=form_data['email'],
        affiliation=form_data['affiliation'],
        cost=0,
    )

    # map transaction to rental/refurbished bike
    rental_vin = form_data['rental_vin']
    refurbished_vin = form_data['refurbished_vin']
    if rental_vin:
        rental_bike = RentalBike.objects.filter(vin=rental_vin).first()
        if rental_bike is None:
            rental_bike = RentalBike(
                vin=rental_vin,
            )
            rental_bike.save()
        new_transaction.rental_bike = rental_bike
    elif refurbished_vin:
        refurbished_bike = RefurbishedBike.objects.filter(vin=refurbished_vin).first()
        if refurbished_bike is None:
            refurbished_bike = RefurbishedBike(
                vin=refurbished_vin,
            )
            refurbished_bike.save()
        new_transaction.refurbished_bike = refurbished_bike

    new_transaction.save()


@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            process_transaction(form.cleaned_data)
            return render_to_response('app/confirm.html',
                                      {"text": "You successfully created the new transaction!",
                                       "absolute_url": "/",
                                      })
    else:
        form = CustomerForm()

    return render(request, 'app/create_transaction.html', {
        'form': form,
    })


def get_tasks(form_data):
    task_list = list()
    for field in form_data:
        if form_data[field] == 'on':
            print "Got a checked task field: " + str(field)
            task_list.append(field[2:].replace("_", " "))

    return task_list


def process_tasks(form_data, transaction):
    # gets all checkbox fields and returns this as the checked task fields
    task_list = get_tasks(form_data)

    menu_items = list()
    for field in task_list:
        menu_items.append(MenuItem.objects.filter(name=field).first())

    task_set_names = [task.menu_item.name for task in list(transaction.task_set.all())]

    # add new tasks
    for task_name in task_list:
        if task_name not in task_set_names:
            task = Task(
                completed=False,
                transaction=transaction,
                menu_item=MenuItem.objects.filter(name=task_name).first(),
            )
            task.save()

    # delete removed tasks
    for task in transaction.task_set.all():
        if task.menu_item.name not in task_list:
            task.delete()


def process_task_form(form_data, transaction):
    for key, value in form_data.iteritems():
        transaction.__setattr__(key, value)

    transaction.save()


@login_required
def assign_tasks(request, **kwargs):

    transaction = Transaction.objects.filter(id=kwargs['trans_pk']).first()

    if request.method == 'POST':

        num_parent_args = kwargs['num_parent_args']

        url = get_url(num_parent_args, kwargs)

        if "cancel" in request.POST:
            return HttpResponseRedirect(url)

        form = TaskForm(request.POST)

        # save tasks assigned to the transaction
        process_tasks(form.data, transaction)

        if form.is_valid():
            # save fields assigned to the transaction
            process_task_form(form.cleaned_data, transaction)
            return render_to_response('app/confirm.html',
                                      {"text": "You successfully assigned tasks!",
                                       "absolute_url": url,
                                       },
                                      )

    else:
        form = TaskForm(instance=transaction)

    items_by_category = get_items_by_category()

    # modify items_by_category to map to list of tuples with an assigned-bool
    task_set_names = [task.menu_item.name for task in transaction.task_set.all()]
    for items in items_by_category.values():
        for i in xrange(len(items)):
            if items[i].name in task_set_names:
                items[i] = (items[i], True)
            else:
                items[i] = (items[i], False)

    return render(request, 'app/assign_tasks.html', {
        'form': form,
        'items_by_category': items_by_category,
    })


@login_required
def assign_parts(request, **kwargs):
    transaction = Transaction.objects.filter(id=kwargs['trans_pk']).first()

    if request.method == 'POST':
        num_parent_args = kwargs['num_parent_args']
        url = get_url(num_parent_args, kwargs)

        if 'cancel' in request.POST:
            return HttpResponseRedirect(url)

        form = DisabledPartCategoryForm(request.POST)

        print "Part Category Form data"
        print form.data
        print "end"

        process_part_category_forms(form.data, transaction)

        # if form.is_valid():
        #     process_transaction(form.cleaned_data)
        return render_to_response('app/confirm.html', {
            "text": "You successfully assigned categories!",
            "absolute_url": url,
        })
    else:
        if transaction.partcategory_set.all():
            old_form_pairs = [(DisabledPartCategoryForm(instance=part_category),
                                PartCategoryForm(instance=part_category))
                               for part_category in transaction.partcategory_set.all()]
            new_form = PartCategoryForm()
        else:
            old_form_pairs = []
            new_form = PartCategoryForm()

    return render(request, 'app/assign_parts.html', {
        'old_form_pairs': old_form_pairs,
        'new_form': new_form,
    })


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


def make_revenue_export_file(table_rows, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = csv.writer(response)
    for update in table_rows:
        update_list = []
        if update.transaction:
            update_list.append(update.transaction.id)
        else:
            update_list.append(None)
        update_list.append(update.amount)
        update_list.append(update.employee)
        if update.transaction:
            update_list.append(update.transaction.first_name + " "
                               + update.transaction.last_name)
        else:
            update_list.append(None)
        update_list.append(update.new_total_revenue)
        update_list.append(update.date_submitted.date())
        writer.writerow(update_list)
    return response


def make_order_export_file(table_rows, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = csv.writer(response)
    for update in table_rows:
        update_list = list()
        update_list.append(update.name)
        update_list.append(update.category)
        update_list.append(update.was_ordered)
        update_list.append(update.price)
        update_list.append(update.description)
        update_list.append(update.date_submitted.date())
        writer.writerow(update_list)
    return response


def make_used_parts_export_file(table_rows, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename


    print "Hey man!"
    choices = PartCategory._meta.get_field('category').choices

    writer = csv.writer(response)
    for update in table_rows:
        update_list = list()
        if update.category:
            update_list.append(choices[int(update.category)][1])
        else:
            update_list.append(None)
        update_list.append(update.was_used)
        update_list.append(update.price)
        update_list.append(update.description)
        update_list.append(update.date_submitted.date())
        if update.transaction:
            update_list.append(update.transaction.id)
        else:
            update_list.append(None)
        writer.writerow(update_list)
    return response


@login_required
def balance(request):
    revenue_updates = RevenueUpdate.objects.all().order_by('date_submitted').reverse()

    if request.method == 'POST':
        if 'export' in request.POST:
            return make_revenue_export_file(revenue_updates, 'balance_history.csv')

    return render(request, 'app/balance.html', {'revenue_updates': revenue_updates})


def process_misc_create(form_data):
    print "YO BRO"
    print form_data['description']
    misc = MiscRevenueUpdate(
        description=form_data['description'],
    )
    misc.save()
    return misc

@login_required
def revenue_update(request):
    if request.method == 'POST':
        rev_form = RevenueForm(request.POST)
        misc_form = MiscRevenueUpdateForm(request.POST)
        if rev_form.is_valid() and misc_form.is_valid():
            print "rev_form.cleaned_data = "
            print rev_form.cleaned_data
            print "misc_form.cleaned_data = "
            print misc_form.cleaned_data

            misc = process_misc_create(misc_form.cleaned_data)
            process_misc_trans_update(rev_form.cleaned_data, misc, request)

            return render_to_response('app/confirm_revenue.html', {})
    else:
        rev_form = RevenueForm()
        misc_form = MiscRevenueUpdateForm()
    return render(request, 'app/revenue_update.html', {
        'rev_form': rev_form,
        'misc_form': misc_form,
    })


@login_required
def orders(request):
    orders = PartOrder.objects.all().order_by('date_submitted').reverse()

    if request.method == 'POST':
        if 'export_orders' in request.POST:
            return make_order_export_file(orders, 'order_history.csv')
    return render(request, 'app/order.html', {'orders': orders})


def make_revenue_update(request, order, amount):
    if amount != 0:
        # make revenue update
        if TotalRevenue.objects.count() == 0:
            total_revenue = TotalRevenue(
                total_revenue=0
            )
            total_revenue.save()
        total_revenue = TotalRevenue.objects.first()
        total_revenue.total_revenue += amount
        total_revenue.save()

        revenue_update = RevenueUpdate.objects.filter(order=order).first()

        if revenue_update is None:
            revenue_update = RevenueUpdate(
                amount=amount,
                employee=request.user.get_username(),
                transaction=None,
                order=order,
                new_total_revenue=total_revenue.total_revenue,
            )
        else:
            revenue_update.amount = amount
        revenue_update.save()


def process_order(request, form_data):

    part_order = PartOrder(
        name=form_data['name'],
        category=form_data['category'],
        was_ordered=form_data['was_ordered'],
        price=form_data['price'],
        description=form_data['description'],
    )
    part_order.save()

    if form_data['was_ordered']:
        make_revenue_update(request, part_order, form_data['price'])


def process_order_edit(request, order, form_data):

    if form_data['was_ordered']:
        make_revenue_update(request, order, form_data['price'])

    order.name = form_data['name']
    order.category = form_data['category']
    order.was_ordered = form_data['was_ordered']
    order.price = form_data['price']
    order.description = form_data['description']

    order.save()


@login_required
def make_order(request):
    absolute_url = "/orders"
    if request.method == 'POST':
        if "cancel" in request.POST:
            return HttpResponseRedirect(absolute_url)
        form = PartOrderForm(request.POST)
        if form.is_valid():
            process_order(request, form.cleaned_data)
            return render_to_response('app/confirm.html', {'absolute_url': absolute_url,
                                                           'text': "You successfully created an order request!"})

    else:
        form = PartOrderForm()

    return render(request, 'app/make_order.html', {'form': form})


@login_required
def edit_order(request, **kwargs):
    absolute_url = "/" + kwargs['parent_url']
    print "GOT TO EDIT ORDER PAGE FROM: " + str(absolute_url)
    order = PartOrder.objects.filter(id=kwargs['order_id']).first()
    if request.method == 'POST':
        if "cancel" in request.POST:
            return HttpResponseRedirect(absolute_url)
        form = PartOrderForm(request.POST)
        if form.is_valid():
            print "BRO. Order = " + str(order)
            process_order_edit(request, order, form.cleaned_data)
            return render_to_response('app/confirm.html', {'absolute_url': absolute_url,
                                                           'text': "You successfully edited the order request!"})

    else:
        form = PartOrderForm(instance=order)

    return render(request, 'app/make_order.html', {'form': form})


def delete_order(request, **kwargs):
    order_id = kwargs["order_id"]
    order = PartOrder.objects.filter(id=order_id).first()

    order_rev_updates = order.revenueupdate_set.all()
    print "ORDER REV UPDATES = "
    print str(order_rev_updates)
    for rev_update in order_rev_updates:
        rev_update.order = None
        rev_update.save()

    PartOrder.objects.filter(id=order_id).first().delete()
    return HttpResponseRedirect('/orders')


@login_required
def used_parts(request):
    used_parts = PartCategory.objects.all().order_by('date_submitted').reverse()

    if request.method == 'POST':
        print request.POST
        if 'export_used' in request.POST:
            return make_used_parts_export_file(used_parts, 'used_parts_history.csv')

    return render(request, 'app/used_parts.html', {'used_parts': used_parts})


def about(request):
    return render(request, 'app/about.html')


def process_misc_edit(form_data, misc):
    misc.description = form_data['description']
    misc.save()


def edit_misc_revenue_update(request, **kwargs):
    absolute_url = "/balance"
    misc = MiscRevenueUpdate.objects.filter(id=kwargs['misc_id']).first()
    if request.method == 'POST':
        if "cancel" in request.POST:
            return HttpResponseRedirect(absolute_url)
        misc_form = MiscRevenueUpdateForm(request.POST)
        if misc_form.is_valid():
            process_misc_edit(misc_form.cleaned_data, misc)
            return render_to_response('app/confirm.html', {'absolute_url': absolute_url,
                                                           'text': "You successfully edited the miscellaneous "
                                                                   "revenue update!"})
    else:
        misc_form = MiscRevenueUpdateForm(instance=misc)
    return render(request, 'app/edit_misc.html', {'misc_form': misc_form})