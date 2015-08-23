from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from app.models import Transaction, Task, Part, Accessory, RentalBike, RefurbishedBike, \
    RevenueUpdate, TotalRevenue, PartCategory, PartOrder, TaskMenuItem, MiscRevenueUpdate, \
    AccessoryMenuItem, PartMenuItem
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
    PartOrderForm, CustomerForm, DisabledPartCategoryForm, MiscRevenueUpdateForm, SingleNumberForm
from django.template import RequestContext
from django.forms.formsets import formset_factory
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
    parts = transaction.part_set.all()
    accessories = transaction.accessory_set.all()
    parent_url = kwargs['parent_url']
    num_parent_args = kwargs['num_parent_args']
    bike_pk = None
    if 'bike_pk' in kwargs:
        bike_pk = kwargs['bike_pk']

    if transaction.completed:
        detail_page = 'detail_complete.html'
    else:
        detail_page = 'detail.html'

    print "Banana Anna! Parts = "
    print parts
    print "END"

    return render_to_response("app/" + detail_page, {
        'transaction': transaction,
        'parent_url': parent_url,
        'tasks': tasks,
        'parts': parts,
        'accessories': accessories,
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


def get_tasks_by_category():
    category_tuples = TaskMenuItem.objects.values_list('category').distinct()
    tasks_by_category = dict()
    for category_tuple in category_tuples:
        category = category_tuple[0]
        tasks_by_category[category] = list(TaskMenuItem.objects.filter(category=category))

    return tasks_by_category


def get_parts_by_category():
    category_tuples = PartMenuItem.objects.values_list('category').distinct()
    parts_by_category = dict()
    for category_tuple in category_tuples:
        category = category_tuple[0]
        parts_by_category[category] = list(PartMenuItem.objects.filter(category=category))

    return parts_by_category


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
    parts = transaction.part_set.all()

    accessories = transaction.accessory_set.all()

    if request.method == 'POST':
        num_parent_args = kwargs['num_parent_args']
        url = get_url(num_parent_args, kwargs)
        if "cancel" in request.POST:
            return HttpResponseRedirect(url)
        else:

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

    # get list of all unique task categories
    task_category_tuples = TaskMenuItem.objects.values_list('category').distinct()
    task_categories = [tup[0] for tup in task_category_tuples]

    # get list of all unique part categories
    part_category_tuples = PartMenuItem.objects.values_list('category').distinct()
    part_categories = [tup[0] for tup in part_category_tuples]

    transaction_form = TaskForm(instance=transaction)

    # new form
    new_category_form = PartCategoryForm()

    return render_to_response("app/edit.html", {'tasks': tasks,
                                                'parts': parts,
                                                'accessories': accessories,
                                                'task_categories': task_categories,
                                                'part_categories': part_categories,
                                                'transaction_form': transaction_form
                                                },
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


def process_tasks(form_data, transaction):
    # gets all checkbox fields and returns this as the checked task fields
    task_dict = get_items(form_data, "task_")

    # delete all tasks
    for task in transaction.task_set.all():
            task.delete()

    # add all marked tasks
    for task_name in task_dict:
        print task_name, "number", task_dict[task_name]
        task = Task(
            completed=False,
            transaction=transaction,
            menu_item=TaskMenuItem.objects.filter(name=task_name).first(),
            number=task_dict[task_name]
        )
        task.save()


def get_items(form_data, prefix):
    part_dict = dict() # maps selected parts to number
    # print form_data
    prefix_len = len(prefix)
    for field in form_data:
        # check for part field

        if field.startswith(prefix):
            part_name = field[prefix_len:]
            # check that part was selected
            if form_data.getlist(field)[0] == 'on':
                print "Got a checked part field: " + str(part_name)
                print form_data.getlist(field)
                part_dict[part_name.replace("_", " ")] = form_data.getlist(field)[1]

    return part_dict


def process_parts(form_data, transaction):
    # gets all checkbox fields and returns this as the checked part fields
    part_dict = get_items(form_data, "part_")

    # delete all parts
    for part in transaction.part_set.all():
            part.delete()

    # add all marked parts
    for part_name in part_dict:
        print part_name, "number", part_dict[part_name]
        part = Part(
            completed=False,
            transaction=transaction,
            menu_item=PartMenuItem.objects.filter(name=part_name).first(),
            number=part_dict[part_name]
        )
        part.save()


def process_accessories(form_data, transaction):
    # gets all checkbox fields and returns this as the checked accessory fields
    accessory_dict = get_items(form_data, "accessory_")

    # delete all accessorys
    for accessory in transaction.accessory_set.all():
            accessory.delete()

    # add all marked accessorys
    for accessory_name in accessory_dict:
        print accessory_name, "number", accessory_dict[accessory_name]
        accessory = Accessory(
            completed=False,
            transaction=transaction,
            menu_item=AccessoryMenuItem.objects.filter(name=accessory_name).first(),
            number=accessory_dict[accessory_name]
        )
        accessory.save()


def process_task_form(form_data, transaction):
    for key, value in form_data.iteritems():
        transaction.__setattr__(key, value)

    transaction.save()


def get_task_number_from_name(name, transaction):
    for task in transaction.task_set.all():
        if name == task.menu_item.name:
            return task.number
    return 1


def get_part_number_from_name(name, transaction):
    for part in transaction.part_set.all():
        if name == part.menu_item.name:
            return part.number
    return 1


def get_accessory_number_from_name(name, transaction):
    for accessory in transaction.accessory_set.all():
        if name == accessory.menu_item.name:
            return accessory.number
    return 1

@login_required
def assign_items(request, **kwargs):

    transaction = Transaction.objects.filter(id=kwargs['trans_pk']).first()

    if request.method == 'POST':

        num_parent_args = kwargs['num_parent_args']

        url = get_url(num_parent_args, kwargs)

        if "cancel" in request.POST:
            return HttpResponseRedirect(url)

        form = TaskForm(request.POST)

        # save tasks
        print "PROCESS TASKS now.."
        process_tasks(form.data, transaction)

        # save parts
        print "PROCESS PARTS now.."
        process_parts(form.data, transaction)

        # save accessories
        print "PROCESS Accessories now.."
        process_accessories(form.data, transaction)

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


    # GET TASK DATA
    tasks_by_category = get_tasks_by_category()

    # modify tasks_by_category to map to list of tuples with an assigned-bool
    task_set_names = [task.menu_item.name for task in transaction.task_set.all()]

    for category in tasks_by_category:
        category_id = str(category).replace(" ", "_")
        items = tasks_by_category[category]
        print tasks_by_category[category]
        for i in xrange(len(items)):
            item = items[i]
            item_id = str(item.name).replace(" ", "_")
            single_number_form = SingleNumberForm(auto_id='task_' + category_id + "_%s")
            single_number_form.fields["task_" + item_id] = single_number_form.fields['number']
            del single_number_form.fields['number']

            if items[i].name in task_set_names:
                task_number = get_task_number_from_name(items[i].name, transaction)
                single_number_form.initial = {"task_" + item_id: task_number}
                items[i] = (items[i], True, single_number_form)
            else:
                items[i] = (items[i], False, single_number_form)

    # GET PART DATA
    parts_by_category = get_parts_by_category()

    # modify parts_by_category to map to list of tuples with an assigned-bool
    part_set_names = [part.menu_item.name for part in transaction.part_set.all()]
    for category in parts_by_category:
        category_id = str(category).replace(" ", "_")
        items = parts_by_category[category]
        for i in xrange(len(items)):
            item = items[i]
            item_id = str(item.name).replace(" ", "_")
            single_number_form = SingleNumberForm(auto_id='part_' + category_id + "_%s")
            single_number_form.fields["part_" + item_id] = single_number_form.fields['number']
            del single_number_form.fields['number']
            if items[i].name in part_set_names:
                part_number = get_part_number_from_name(items[i].name, transaction)
                single_number_form.initial = {"part_" + item_id: part_number}
                items[i] = (items[i], True, single_number_form)
            else:
                items[i] = (items[i], False, single_number_form)


    # GET ACCESSORY DATA
    accessory_items = list(AccessoryMenuItem.objects.all())

    accessory_set_names = [accessory.menu_item.name for accessory in transaction.accessory_set.all()]
    for i in xrange(len(accessory_items)):
        item = accessory_items[i]
        item_id = str(item.name).replace(" ", "_")
        single_number_form = SingleNumberForm(auto_id='accessory_' + "_%s")
        single_number_form.fields["accessory_" + item_id] = single_number_form.fields['number']
        del single_number_form.fields['number']

        if item.name in accessory_set_names:
            accessory_number = get_accessory_number_from_name(item.name, transaction)
            single_number_form.initial = {"accessory_" + item_id: accessory_number}
            accessory_items[i] = (item, True, single_number_form)
        else:
            accessory_items[i] = (item, False, single_number_form)

    return render(request, 'app/assign_items.html', {
        'form': form,
        # 'single_number_formset': single_number_formset,
        'tasks_by_category': tasks_by_category,
        'parts_by_category': parts_by_category,
        'accessory_items': accessory_items,
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

    # Item Type-ID, Amount, Employee, Customer, Total, Date

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = csv.writer(response)

    writer.writerow(["Item", "Amount", "Employee", "Customer",
                     "Total", "Date"])

    for update in table_rows:
        update_list = []
        if update.transaction:
            update_list.append("T-" + str(update.transaction.id))
        elif update.order:
            update_list.append("P-" + str(update.order.id))
        elif update.misc_revenue_update:
            update_list.append("M-" + str(update.misc_revenue_update.id))
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

    # ID, Name, Installed, Price, Date

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = csv.writer(response)

    writer.writerow(["ID", "Name", "Category", "Installed", "Price", "Date"])

    for order in table_rows:
        order_list = list()
        order_list.append(order.id)
        order_list.append(order.name)
        order_list.append(order.get_category_display())
        order_list.append(order.was_ordered)
        order_list.append(order.price)
        order_list.append(order.date_submitted.date())
        writer.writerow(order_list)
    return response


def make_used_parts_export_file(table_rows, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    # Transaction ID, Category, Price, Installed, Date

    choices = PartCategory._meta.get_field('category').choices

    writer = csv.writer(response)

    writer.writerow(["Transaction ID", "Category", "Price", "Installed", "Date"])

    for part in table_rows:
        parts_list = list()
        if part.transaction:
            parts_list.append(part.transaction.id)
        else:
            parts_list.append(None)
        if part.category:
            parts_list.append(part.get_category_display())
        else:
            parts_list.append(None)
        parts_list.append(part.price)
        parts_list.append(part.was_used)
        parts_list.append(part.date_submitted.date())

        writer.writerow(parts_list)
    return response


@login_required
def balance(request):
    revenue_updates = RevenueUpdate.objects.all().order_by('date_submitted').reverse()

    if request.method == 'POST':
        if 'export' in request.POST:
            return make_revenue_export_file(revenue_updates, 'balance_history.csv')

    return render(request, 'app/balance.html', {'revenue_updates': revenue_updates})


def process_misc_create(form_data):
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


def bike_inventory(request):
    return render(request, 'app/bike_inventory.html')


def sold_items(request):
    return render(request, 'app/sold_items.html')


def buy_backs(request):
    return render(request, 'app/buy_backs.html')