from decimal import Decimal
from django.conf import settings
from django.http import HttpRequest
from shop.models import Product


class Cart:
    """Класс описывающий корзину и методы взаимодествия с ней"""
    
    def __init__(self, request: HttpRequest):
        """Инициализация корзины"""
        
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # создается пустая корзина
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product: Product, quantity=1, override_quantity=False):
        """Добавить товар в корзину либо обновить количество"""
        
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def save(self):
        """Пометить сеанс как измененный"""
        #это сообщает фреймворку что сеанс изменился и его нужно сохранить
        self.session.modified = True
    
    def remove(self, product: Product):
        """Удалить товар из корзины"""
        
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Позволяет перебирать товары в корзине с помощью цикла и получение товара из БД"""
        
        product_ids = self.cart.keys()
        
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """Подсчет количества всех товаров в корзине"""
        
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """Расчет общей стоимости товарой"""
        
        return sum(Decimal(item['price']) * item['quantity']
                    for item in self.cart.values())
    
    def clear(self):
        """Очистка корзину путем удаления сеанса корзины"""
        
        del self.session[settings.CART_SESSION_ID]
        self.save()