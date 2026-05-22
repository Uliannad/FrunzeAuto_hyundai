from django import forms
from .models import ServiceBooking, TestDriveBooking, Car

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