from django.contrib import admin
from .models import Car, SparePart, ServiceBooking, TestDriveBooking


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'year', 'price', 'is_available')
    list_filter = ('body_style', 'is_available')
    search_fields = ('model_name',)
admin.site.register(SparePart)
admin.site.register(ServiceBooking)
admin.site.register(TestDriveBooking)

