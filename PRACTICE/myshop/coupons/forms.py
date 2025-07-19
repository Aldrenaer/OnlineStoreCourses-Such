from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label='Код купона',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите код купона'
        })
    )