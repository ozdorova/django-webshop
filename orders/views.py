from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created_task
from yookassa import Payment, Configuration
from django.urls import reverse
import uuid

order_id = None

def order_create(request):
    """Создание заказа"""
    
    #текущая корзина
    cart = Cart(request)
    global order_id
    
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                
            price = cart.get_total_price()
            cart.clear()
            order_id = order.id
            
            # тестовые данные Юкасса
            Configuration.account_id = '372530'
            Configuration.secret_key = 'test_f0RImG50ZazCZyiulHMXMDnT5mLmmsqEs6qGI0WZbRA'
            
            # данные для передачи по api
            payment_data = {
                "amount": {
                    "value": f"{price}",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": 'http://localhost:8000'+reverse('orders:created'),
                },
                "capture": True,
                "description": f"Заказ {order.id}"
            }
            
            #создание платежа юкасса
            payment = Payment.create(payment_data, uuid.uuid4())
            
            # запись номера операции
            order.payment_id = payment.id
            
            order.save()
            
            #перенаправление на подтверждение юкассы
            return HttpResponseRedirect(payment.confirmation.confirmation_url)
        
    else: # GET
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form},
    )


def order_created_view(request):
    """Вызывается в случае успешной оплаты"""
    #запуск асинхронного задания celery
    order = Order.objects.get(id=order_id)
    order.paid = True
    order.save()
    order_created_task.delay(order_id)
    return render(request, 'orders/order/created.html')