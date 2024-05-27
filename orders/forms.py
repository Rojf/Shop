from django import forms

from .Repository import OrderRepository


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderRepository.model
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
