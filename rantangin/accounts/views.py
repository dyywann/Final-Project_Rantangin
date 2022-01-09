from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import View
from .forms import UserRegistrationForm, CheckoutForm                                         
from django.views.generic import ListView, DetailView
from django.utils import timezone
import uuid
from .models import (               
    Item,
    Order,
    OrderItem,
    CheckoutAddress
)

class HomeView(ListView):
    model = Item
    template_name = "accounts/home.html"

class ProductView(DetailView):
    model = Item
    template_name = "accounts/product.html"

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object' : order
            }
            return render(self.request, 'accounts/keranjang.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'accounts/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                address = form.cleaned_data.get('address')
                zip = form.cleaned_data.get('zip')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                save_info = form.cleaned_data.get('save_info')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    address=address,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.ordered = True
                order.save()
                return redirect('payments')
            messages.warning(self.request, "Failed Chekout")
            return redirect('checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("order-summary")

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=True)
        context = {
            'order': order
        }
        return render(self.request, 'accounts/payments.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your accounts has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form':form}
    return render(request, 'accounts/signup.html', context)

@login_required
def add_to_cart(request, pk) :
    item = get_object_or_404(Item, pk = pk )
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered= False)

    if order_qs.exists() :
        order = order_qs[0]
        
        if order.items.filter(item__pk = item.pk).exists() :
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("keranjang")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("keranjang")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("keranjang")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \""+order_item.item.item_name+"\" remove from your cart")
            return redirect("keranjang")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("keranjang")
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("keranjang")

@login_required
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Item, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists() :
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("keranjang")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("keranjang")
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("keranjang")

