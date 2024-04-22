import redis
from django.conf import settings
from .models import Product


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,)


class Recommender:
    """Класс рекомендаций для хранения покупок и получение предложений по товару"""

    def get_product_key(self, id):
        """Формирование ключа для redis"""
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        """Создание сортированного множества для хранения рекомендаций к товарам"""
        products_ids = [p.id for p in products]
        for product_id in products_ids:
            for with_id in products_ids:
                # получить другие товары, купленные вместе с каждым товаром
                if product_id != with_id:
                    #  увеличить балл товара
                    # балл представляет число раз когда другой товар был куплен вместе с данным товаром
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        """Метод извлечения товаров, которые были куплены вместе"""
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # если только 1 товар
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # елси товаров несколько
            # генерация временного ключа
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'

            # обьединить баллы всех товаров, сохранить полученное сортированное множество во временнном ключе
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)

            # удалить идентификаторы товарый для который дается рекомендация
            r.zrem(tmp_key, *product_ids)

            # получить идентификаторы товаров по их количеству, сортировка по убыванию
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]

            # удалить временный ключ
            r.delete(tmp_key)

        suggested_products_ids = [int(id) for id in suggestions]
        # получить предлагаемые товары и отсортировать их по порядку их появления

        suggested_products = list(
            Product.objects.filter(id__in=suggested_products_ids))

        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id))

        return suggested_products

    def clear_purchases(self):
        """Очистка рекомендаций"""
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
