import re
from datetime import date

from django import forms

from .models import (
    CustomCarRequest,
    Review,
)


class CustomCarRequestForm(forms.ModelForm):

    privacy_consent = forms.BooleanField(
        required=True,
        label=(
            'Sunt de acord ca datele furnizate să fie folosite '
            'pentru a fi contactat în legătură cu această cerere.'
        )
    )

    class Meta:

        model = CustomCarRequest

        fields = [
            'full_name',
            'phone',
            'email',
            'brand',
            'model_name',
            'budget_max',
            'year_min',
            'fuel',
            'transmission',
            'max_mileage',
            'notes',
        ]

        widgets = {

            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ex: Alexandru Popescu',
                    'autocomplete': 'name',
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Ex: 07xx xxx xxx',
                    'autocomplete': 'tel',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Ex: nume@email.com',
                    'autocomplete': 'email',
                }
            ),

            'brand': forms.TextInput(
                attrs={
                    'placeholder': 'Ex: BMW, Volkswagen, Audi',
                }
            ),

            'model_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ex: Seria 3, Golf, A4',
                }
            ),

            'budget_max': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex: 15000',
                    'min': '1',
                }
            ),

            'year_min': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex: 2018',
                    'min': '1980',
                }
            ),

            'max_mileage': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex: 150000',
                    'min': '0',
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'placeholder': (
                        'Ex: prefer culoarea neagră, '
                        'navigație, scaune încălzite...'
                    ),
                    'rows': 5,
                }
            ),

        }

    def clean_phone(self):

        phone = self.cleaned_data['phone'].strip()

        digits = re.sub(
            r'\D',
            '',
            phone
        )

        if len(digits) < 8:

            raise forms.ValidationError(
                'Introdu un număr de telefon valid.'
            )

        return phone

    def clean_year_min(self):

        year = self.cleaned_data.get(
            'year_min'
        )

        if year is None:
            return year

        current_year = date.today().year

        if year < 1980 or year > current_year + 1:

            raise forms.ValidationError(
                'Introdu un an valid.'
            )

        return year

    def clean_budget_max(self):

        budget = self.cleaned_data[
            'budget_max'
        ]

        if budget <= 0:

            raise forms.ValidationError(
                'Bugetul trebuie să fie mai mare de 0.'
            )

        return budget


class ReviewForm(forms.ModelForm):

    publish_consent = forms.BooleanField(
        required=True,
        label=(
            'Sunt de acord ca recenzia și numele meu '
            'să fie afișate public pe site.'
        )
    )

    class Meta:

        model = Review

        fields = [
            'customer_name',
            'rating',
            'car_model',
            'comment',
        ]

        widgets = {

            'customer_name': forms.TextInput(
                attrs={
                    'placeholder': 'Numele tău',
                }
            ),

            'rating': forms.Select(),

            'car_model': forms.TextInput(
                attrs={
                    'placeholder': (
                        'Ex: Volkswagen Golf VI'
                    ),
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'placeholder': (
                        'Spune-ne cum a fost experiența ta '
                        'cu Auto Cars GML...'
                    ),
                    'rows': 5,
                }
            ),

        }