from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from my_site.forms import RegistrationForm, LoginForm, ComputerForm
from django.views import View
from django import forms
from my_site.models import UserProfile, Computer, Order, BelongTO
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, CreateView
from django.views.generic import DetailView
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.core.urlresolvers import reverse
from django.core.files import File
from django.core.files.storage import FileSystemStorage


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        return render(request, 'registration.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def log(request):
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    if request.is_ajax():
        form_l = LoginForm(request.GET).save(commit=False)

        if form_l.is_valid():
            user = authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if not request.GET.get('remember'):
                    request.session.set_expiry(0)
                return HttpResponseRedirect('/main')
        return HttpResponse('error')
    else:
        form_l = LoginForm(request.POST)
        return HttpResponse('oi')


class SingIn(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        if self.request.method == 'POST':
            form = LoginForm(self.request.POST)
            if form.is_valid():
                auth.login(self.request, form.cleaned_data['user'])
                if not self.request.POST.get('remember'):
                    self.request.session.set_expiry(0)
                return HttpResponseRedirect('/main')
        else:
            form = LoginForm()
        return render(self.request, 'login.html', {'form': form})


def logout_view(request):
    user = request.user
    client_orders = Order.objects.filter(customer_id=user.id).all()
    for order in client_orders:
        flag = 1
        relation = BelongTO.objects.filter(order_id=order.code).all()
        for rel in relation:
            if rel.quantity != 0:
                flag = 0
            else:
                flag = 1
        if flag:
            order.delete()
    logout(request)
    return render(request, 'logout.html')


class ItemsView(View):
    items_on_page = 5

    def get(self, request, page_id):
        page_id = int(page_id)
        client = None
        count = len(Computer.objects.all())
        last = count - ItemsView.items_on_page * (page_id-1)  # осталось
        start = page_id * ItemsView.items_on_page - ItemsView.items_on_page
        if start < count:
            if last >= ItemsView.items_on_page:
                end = start + ItemsView.items_on_page
            else:
                end = start + last
        elif start == len(Computer.objects.all()):
            end = start
        else:
            data = []
            context = {'search': data, 'user': client}
            return render_to_response('list_object.html', context)
        dict_customers = {}  # код компа - массив покупателей
        data = Computer.objects.all()[start: end]
        orders = Order.objects.all()
        for c in data:  # по компам
            customers = []  # купили
            for o in orders:  # по заказам
                cur_cust = o.customer  # покупатель, сделавший заказ
                for item in o.items.all():  # по элементам заказа
                    if item.name == c.name:  # если текущий комп
                        if cur_cust not in customers:
                            customers.append(cur_cust)  # покупателя в купили
            dict_customers[c.name] = customers  # список покупателей для компа
        client_orders = []
        if self.request.user.id is not None:
            client = request.user
            client_orders = Order.objects.filter(customer_id=client.id)
            client_orders_number = client_orders.count()
            client_profile = UserProfile.objects.get(id=client.id)
            if client_orders_number == 0:
                order = Order(customer=client_profile)
                order.save()

        form = ComputerForm()
        if page_id == 1:
            return render(request, 'list.html',
                          context={'search': data,
                                   'customers': dict_customers,
                                   'client_orders': client_orders,
                                   'form': form,
                                   'user': client})
        else:
            context = {'search': data,
                       'customers': dict_customers,
                       'client_orders': client_orders,
                       'form': form, 'user': client}
            return render_to_response('list_object.html', context)


class OrdersView(View):
    def get(self, request):
        empty_orders = []
        computers_in_order = BelongTO.objects.all()  # код заказа - компы
        prices = {}  # цены
        data = Order.objects.filter(
            customer_id=request.user.id).all()  # заказы пользователя
        for o in data:
            computers = BelongTO.objects.filter(
                order_id=o.code).all()  # компьютеры заказа
            if len(computers) == 0:
                empty_orders.append(o.code)
            total = 0
            for c in computers:
                cur_comp = Computer.objects.get(name=c.item_id)
                if c.item_id not in prices.keys():
                    prices[c.item_id] = cur_comp.price
                total = total + cur_comp.price*c.quantity
            o.total = total
            o.save()

        return render(request, 'orders.html',
                      context={"data": data,
                               "computers": computers_in_order,
                               "prices": prices,
                               'empty_orders': empty_orders})


@ensure_csrf_cookie
def change_status(request):
    if request.is_ajax():
        c = request.POST['ordercode']
        o = Order.objects.get(code=c)
        o.is_open = False
        o.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('bad')


@ensure_csrf_cookie
def add(request):
    if request.is_ajax():
        code = request.POST.get('ord_id')
        item = request.POST.get('i_name')
        o = Order.objects.get(code=code)  # заказ
        i = Computer.objects.get(name=item)  # комп
        relation = BelongTO.objects.filter(
            order_id=code).all()  # все компьютеры заказа
        flag = 0
        for el in relation:
            if i.name == el.item_id:
                el.quantity += 1
                el.save()
                flag = 1
                break
        if not flag:
            id = code+item
            b = BelongTO(id=id, order_id=code, item_id=item, quantity=1)
            b.save()
        i.quantity -= 1
        i.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('bad')


@ensure_csrf_cookie
def delete_item(request):
    if request.is_ajax():
        code = request.POST.get('ordercode')  # код заказа
        item = request.POST.get('item')  # код компа
        relation = BelongTO.objects.get(
            order_id=code, item_id=item)  # все данные компьютеры заказа
        if relation.quantity > 1:
            relation.quantity -= 1
            relation.save()
        else:
            relation.delete()

        return HttpResponse('ok')
    else:
        return HttpResponse('bad')


@ensure_csrf_cookie
def delete_order(request):
    if request.is_ajax():
        c = request.POST['ordercode']
        o = Order.objects.get(code=c)
        o.delete()
        return HttpResponse('ok')
    else:
        return HttpResponse('bad')


class OneItem(DetailView):
    model = Computer
    context_object_name = 'computer'
    template_name = 'object.html'

    def get_object(self):
        code_url = self.kwargs['pk']
        return Computer.objects.get(name=code_url)

    def get_context_data(self, **kwargs):
        context = super(OneItem, self).get_context_data(**kwargs)
        relation = BelongTO.objects.filter(item_id=self.kwargs['pk'])
        customers_list = []
        for rel in relation:
            order = Order.objects.get(code=rel.order_id)
            customer = order.customer
            if customer not in customers_list:
                customers_list.append(customer)
        context['customers_list'] = customers_list
        context['client_orders'] = Order.objects.filter(
            customer_id=self.request.user.id)
        return context


def addnew(request):
    if request.method == "POST":
        form = ComputerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('item_view', args=(form.cleaned_data['name'],)))


def list_computers(request):
    if request.is_ajax():
        computers = Computer.objects.all()
        data = []
        for c in computers:
            data.append(c.name)
    jsond = json.dumps(data)
    return HttpResponse(jsond, content_type='application/json')
