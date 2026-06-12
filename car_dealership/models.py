from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    BODY_STYLE_CHOICES = [
        ('sedan', 'Седан'),
        ('suv', 'Кросовер'),
        ('electric', 'Електромобіль'),
        ('hatchback', 'Хетчбек'),
    ]

    model_name = models.CharField(max_length=100, verbose_name="Модель (напр. Tucson)")
    body_style = models.CharField(max_length=20, choices=BODY_STYLE_CHOICES, verbose_name="Тип кузова")
    year = models.PositiveIntegerField(verbose_name="Рік випуску")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна (грн)")

    engine_info = models.CharField(max_length=100, verbose_name="Двигун", help_text="Напр. 2.0 Multi Point Injection")
    power = models.IntegerField(verbose_name="Потужність (к.с.)")
    transmission = models.CharField(max_length=50, verbose_name="Трансмісія", default="6MT / 6AT")

    image = models.ImageField(upload_to='hyundai_cars/', verbose_name="Фото авто")
    description = models.TextField(verbose_name="Опис моделі та переваг", blank=True)
    is_available = models.BooleanField(default=True, verbose_name="Доступно в салоні")

    def __str__(self):
        return f"Hyundai {self.model_name} {self.year}"


class SparePart(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва запчастини")
    part_number = models.CharField(max_length=50, verbose_name="Артикул (OEM)", blank=True)
    category = models.CharField(max_length=100, verbose_name="Категорія (Фільтри, Гальма тощо)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='parts/', blank=True, null=True)

    def __str__(self):
        return self.name


class ServiceBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='service_bookings',
                             verbose_name="Користувач")
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    email = models.CharField(max_length=100, verbose_name="email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    vin_code = models.CharField(max_length=17, verbose_name="VIN-код авто", blank=True)
    service_type = models.CharField(max_length=100, verbose_name="Тип робіт (ТО, діагностика)")
    date = models.DateTimeField(verbose_name="Дата запису")

    def __str__(self):
        return f"Сервіс {self.service_type} — {self.name} ({self.date.strftime('%d.%m.%Y')})"


class TestDriveBooking(models.Model):
    # Зв'язуємо запис на тест-драйв із користувачем
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='test_drives',
                             verbose_name="Користувач")
    name = models.CharField(max_length=100, verbose_name="Клієнт")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Обрана модель")
    date = models.DateTimeField(verbose_name="Час тест-драйву")

    def __str__(self):
        return f"Тест-драйв {self.car.model_name} — {self.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефону")

    def __str__(self):
        return f"Профіль користувача: {self.user.username}"