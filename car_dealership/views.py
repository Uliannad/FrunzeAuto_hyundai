from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
# Імпортуємо моделі напряму, щоб код нижче працював
from car_dealership.models import Car, TestDriveBooking, ServiceBooking, SparePart
from .forms import ServiceBookingForm, TestDriveForm
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class HomeView(TemplateView):
    template_name = 'tasks/home.html'

class CarListView(ListView):
    model = Car
    template_name = 'tasks/car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'tasks/car_detail.html'
    context_object_name = 'car'

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")

class RegisterView(CreateView):
    template_name = "tasks/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home") # Виправлено на чисте "home"
def test_drive(request, car_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        car = get_object_or_404(Car, id=car_id)

        TestDriveBooking.objects.create(
            name=name, phone=phone, car=car, date=date
        )
        return render(request, 'success.html', {'message': 'Ви успішно записані на тест-драйв!'})


class TestDriveSelectView(ListView):
    model = Car
    template_name = 'tasks/test_drive_select.html'
    context_object_name = 'cars'

    def get_queryset(self):
        return Car.objects.filter(is_available=True)

class TestDriveBookView(CreateView):
    model = TestDriveBooking
    form_class = TestDriveForm
    template_name = 'tasks/test_drive_book.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_car'] = get_object_or_404(Car, id=self.kwargs['car_id'])
        return context

    def form_valid(self, form):
        car = get_object_or_404(Car, id=self.kwargs['car_id'])
        form.instance.car = car
        return super().form_valid(form)

class ServiceView(CreateView):
    model = ServiceBooking
    form_class = ServiceBookingForm
    template_name = 'tasks/service_booking.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parts'] = SparePart.objects.all()
        return context