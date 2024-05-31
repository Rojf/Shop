from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.views.decorators.http import require_GET
from django.views import View
from django.urls import reverse

import weasyprint

from .Repository import OrderItemRepository, OrderRepository
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


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(OrderRepository.model, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))])

    return response


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(OrderRepository.model, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@require_GET
def order_created(request, pk):
    if pk:
        return render(request, 'orders/order/created.html', {'order_id': pk})

    return HttpResponseNotFound("Not Found")
