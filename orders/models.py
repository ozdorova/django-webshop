
from django.db import models
from shop.models import Product


class Order(models.Model):
    """Модель детальной информации о заказе"""
    
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField()
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    
    class Meta:
        ordering = [
            '-created',
        ]
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return f'Заказ {self.id}'
    
    def get_total_cost(self):
        """Получение общей суммы заказа"""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Модель отвечающая за позицию в заказе"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        """Возвращает общую стоимость позиции в заказе"""
        return self.price * self.quantity