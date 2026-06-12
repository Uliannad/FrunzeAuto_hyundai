from django import forms
from .models import ServiceBooking, TestDriveBooking, Car
from django.contrib.auth.models import User
from .models import UserProfile

class ServiceBookingForm(forms.ModelForm):
    SERVICE_CHOICES = [
        ('to', 'Планове ТО'),
        ('diagnosis', 'Комп’ютерна діагностика'),
        ('car_wash', 'Автомийка'),
        ('anti_bacterial', 'Антибактеріальна обробка системи кондиціювання'),
        ('ac_check', 'Перевірка та заправка системи кондиціювання'),
        ('maintenance', 'Технічне обслуговування, поточний ремонт'),
        ('body_repair', 'Кузовний ремонт'),
        ('accessories', 'Аксесуари та додаткове обладнання'),
        ('warranty', 'Гарантійне обслуговування'),
        ('parts', 'Запасні частини'),
        ('lpg_install', 'Встановлення ГБО'),
        ('other', 'Інше'),
    ]

    service_type = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        label="Тип робіт",
        widget=forms.Select(attrs={'class': 'form-select rounded-pill'})
    )

    class Meta:
        model = ServiceBooking
        fields = ['name', 'last_name', 'phone', 'vin_code', 'service_type', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': "Ваше ім'я"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': "Ваше прізвище"}),
            'phone': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': '+380...'}),
            'vin_code': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': '17 символів'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control rounded-pill', 'type': 'datetime-local'}),
        }

class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDriveBooking
        fields = ['car', 'name', 'last_name', 'phone', 'date']
        widgets = {
            # Приховуємо поле вибору авто, ми заповнимо його через JS
            'car': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': "Ім'я"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Прізвище'}),
            'phone': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': '+380...'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control rounded-pill', 'type': 'datetime-local'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Електронна пошта")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': "Ім'я",
            'last_name': "Прізвище",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Додаємо класи Bootstrap, щоб поля виглядали красиво
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control border-dark-subtle'
            field.widget.attrs['style'] = 'border-radius: 4px;'

# Форма для редагування телефону (UserProfile)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number']
        labels = {
            'phone_number': 'Номер телефону',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control border-dark-subtle'
            field.widget.attrs['style'] = 'border-radius: 4px;'
            field.widget.attrs['placeholder'] = '+380XXXXXXXXX'