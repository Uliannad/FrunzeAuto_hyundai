from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from car_dealership.models import Car, TestDriveBooking, ServiceBooking, SparePart, UserProfile
from .forms import ServiceBookingForm, TestDriveForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# ==========================================
# 📑 КОНТЕКСТНИЙ ПРОЦЕСОР ДЛЯ ПРОФІЛЮ КОРИСТУВАЧА (ПОВЕРНУВ НА МІСЦЕ!)
# ==========================================
def profile_context_processor(request):
    if request.user.is_authenticated:
        return {
            'service_bookings': ServiceBooking.objects.filter(user=request.user),
            'test_drives': TestDriveBooking.objects.filter(user=request.user)
        }
    return {}


# ==========================================
# 🏠 ГОЛОВНІ СТОРІНКИ ТА АВТОРИЗАЦІЯ
# ==========================================
class HomeView(TemplateView):
    template_name = 'tasks/home.html'


class CarListView(ListView):
    model = Car
    template_name = 'tasks/car_list.html'
    context_object_name = 'cars'


class CarDetailView(TemplateView):
    template_name = 'tasks/car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_slug = self.kwargs.get('car_name', 'elantra').lower().strip()

        car_descriptions = {
            'elantra': "Hyundai Elantra — це втілення динамічного стилю та сучасних технологій. Седан вражає своїм сміливим гранованим дизайном у стилі 'Parametric Dynamics'...",
            'kona': "Hyundai Kona — яскравий, сміливий та ультрасучасний компактний кросовер, створений для активного міського життя...",
            'ioniq5': "Hyundai Ioniq 5 — повністю електричний кросовер нового покоління, який ламає стереотипи...",
            'venue': "Hyundai Venue — найкомпактніший, маневрений та неймовірно практичний кросовер у лінійці...",
            'tucson': "Hyundai Tucson — світовий бестселер та справжня дизайнерська революція у класі позашляховиків...",
            'inster': "Hyundai Inster — абсолютно новий, повністю електричний міський субкомпактний кросовер...",
            'santa fe': "Hyundai Santa Fe — флагманського повнорозмірний сімейний кросовер, який отримав радикальний брутальний дизайн...",
            'staria': "Hyundai Staria — футуристичний мінівен космічного дизайну, який повністю змінює уявлення про перевезення..."
        }

        context['car_name'] = car_slug.title()
        context['car_img_name'] = car_slug.replace(' ', '_')
        context['car_description'] = car_descriptions.get(car_slug, "Сучасний автомобіль Hyundai.")
        return context


def car_constructor_view(request, car_name):
    return render(request, 'tasks/car_constructor.html', {'car_name': car_name.capitalize()})


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
        return redirect("home")


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_car'] = get_object_or_404(Car, id=self.kwargs['car_id'])
        return context

    def post(self, request, *args, **kwargs):
        car = get_object_or_404(Car, id=self.kwargs['car_id'])
        first_name = request.POST.get('name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        date_str = request.POST.get('date', '').strip()

        if first_name and phone and date_str:
            booking_user = request.user if request.user.is_authenticated else None
            TestDriveBooking.objects.create(
                user=booking_user,
                car=car,
                name=first_name,
                last_name=last_name,
                phone=phone,
                date=date_str
            )

            return render(request, 'tasks/success.html')
        return self.get(request, *args, **kwargs)


class ServiceView(CreateView):
    model = ServiceBooking
    form_class = ServiceBookingForm
    template_name = 'tasks/service_booking.html'
    # Повертаємо твою оригінальну сторінку успіху для сервісу
    success_url = reverse_lazy('service_success_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parts'] = SparePart.objects.all()
        return context

    def form_valid(self, form):
        booking = form.save(commit=False)
        if self.request.user.is_authenticated:
            booking.user = self.request.user
        booking.save()
        return super().form_valid(form)


class ModelsOverviewView(TemplateView):
    template_name = 'tasks/models_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models_list'] = [
            {'slug': 'elantra', 'name': 'ELANTRA', 'price': 'від 923 700 грн', 'category': 'sedan'},
            {'slug': 'kona', 'name': 'KONA Hybrid', 'price': 'від 1 378 100 грн', 'category': 'crossover eco'},
            {'slug': 'ioniq5', 'name': 'IONIQ 5', 'price': 'від 1 950 000 грн', 'category': 'eco'},
            {'slug': 'venue', 'name': 'VENUE', 'price': 'від 890 500 грн', 'category': 'crossover'},
            {'slug': 'tucson', 'name': 'TUCSON', 'price': 'від 1 150 000 грн', 'category': 'crossover'},
            {'slug': 'inster', 'name': 'INSTER', 'price': 'від 1 237 600 грн', 'category': 'crossover eco', 'is_new': True},
            {'slug': 'santa fe', 'name': 'SANTA FE', 'price': 'від 1 750 000 грн', 'category': 'crossover'},
            {'slug': 'staria', 'name': 'STARIA', 'price': 'від 2 100 000 грн', 'category': 'mpv'},
        ]
        return context


class ServiceInfoView(TemplateView):
    template_name = 'tasks/service_info.html'


class SpecialOffersView(TemplateView):
    template_name = 'tasks/special_offers.html'


class TradeInView(TemplateView):
    template_name = 'tasks/trade_in.html'


@login_required
def edit_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'tasks/edit_profile.html', context)

class ContactView(TemplateView):
    template_name = 'tasks/contacts.html'