from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Форма позволяющая выбирать количество товаров в корзине"""

    # выбор количества товаров от 1 до 20
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Количество')

    # поле для указания, нужно ли перезаписывать количество товаров в корзине, скрыто от пользователя
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)
