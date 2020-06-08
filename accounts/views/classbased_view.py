from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, DetailView, \
    CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin

from django.shortcuts import render, redirect
from accounts.models import Product, Customer, Order, Tag
from accounts.form import CustomerForm
from accounts.filters import OrderFilter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decorators import allowed_users, admin_only


class HomeView(TemplateView):
    template_name = 'accounts/dashboard.html'

    @method_decorator(login_required(login_url='login'))
    @method_decorator(admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.all()[:5]
        context['customers'] = Customer.objects.all()
        context['total_customer'] = Customer.objects.count()
        context['total_orders'] = Order.objects.count()
        context['delivered'] = Order.objects.filter(status='Delivered').count()
        context['pending'] = Order.objects.filter(status='Pending').count()

        return context


class UserPageView(TemplateView):
    template_name = 'accounts/user.html'

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['customer']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserPageView, self).get_context_data(**kwargs)
        orders = self.request.user.customer.orders.all()
        context['orders'] = orders
        context['total_orders'] = orders.count()
        context['delivered'] = orders.filter(status='Delivered').count()
        context['pending'] = orders.filter(status='Pending').count()
        return context


class AccountSettingView(TemplateView):
    template_name = 'accounts/account_settings.html'
    form_class = CustomerForm

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['customer']))
    def dispatch(self, *args, **kwargs):
        self.instance = self.request.user.customer
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.instance)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'form': form})


class ProductsView(ListView):
    model = Product
    template_name = 'accounts/products.html'
    context_object_name = 'products'

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomerView(DetailView):
    model = Customer
    template_name = 'accounts/customers.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(id=self.kwargs.get('pk'))
        myFilter = OrderFilter(self.request.GET, queryset=customer.orders.all())
        orders = myFilter.qs
        context['myFilter'] = myFilter
        context['orders'] = orders
        return context

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderCreateView(CreateView):
    model = Order
    fields = ['product', 'status', 'note']
    template_name = 'accounts/order_form.html'

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):  # for_set_not_NULL_value
        form.instance.customer = self.request.user.customer
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('customers', kwargs={'pk': self.object.customer.pk})


class OrderUpdateView(UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['product', 'status', 'note']
    template_name = 'accounts/order_form.html'

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def test_func(self):
        order = self.get_object()
        if order.customer.id == self.request.user.id:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse_lazy('customers', kwargs={'pk': self.object.customer.pk})


class OrderDeleteView(UserPassesTestMixin, DeleteView):
    model = Order
    template_name = 'accounts/delete.html'

    def test_func(self):
        order = self.get_object()
        if order.customer.id == self.request.user.id:
            return True
        else:
            return False

    def get_success_url(self):
        return redirect('customers', kwargs={'pk': self.object.customer.pk})