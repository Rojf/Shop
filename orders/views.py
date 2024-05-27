from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_GET
from django.http import HttpResponseNotFound
from django.urls import reverse

from .Repository import OrderItemRepository
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_creared as celery_order_created


class OrderCreateView(View):
    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()

        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)

        if not cart.cart:
            return redirect('/')

        if form.is_valid():
            order = form.save()

            for item in cart:
                if not item['product']:
                    return
                OrderItemRepository.create(order=order, product=item['product'], price=item['price'],
                                           quantity=item['quantity'])

            cart.clear()
            celery_order_created.delay(order.id)
            request.session['order_id'] = order.id

            return redirect(reverse('payment:process'))

        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@require_GET
def order_created(request, pk):
    if pk:
        return render(request, 'orders/order/created.html', {'order_id': pk})

    return HttpResponseNotFound("Not Found")
