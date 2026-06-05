from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
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


class CarDetailView(TemplateView):
    template_name = 'tasks/car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Отримуємо назву машини з URL
        car_slug = self.kwargs.get('car_name')
        if car_slug:
            car_slug = car_slug.lower().strip()
        else:
            car_slug = 'elantra'

        # ПОВНИЙ СЛОВНИК ДЛЯ ВСІХ МОДЕЛЕЙ
        car_descriptions = {
            'elantra': (
                "Hyundai Elantra — це втілення динамічного стилю та сучасних технологій. "
                "Седан вражає своїм сміливим гранованим дизайном у стилі 'Parametric Dynamics', "
                "просторішим технологічним салоном, наднизькою посадкою та цифровим кокпітом. "
                "Він створений для тих, хто цінує драйверський характер, відмінну керованість "
                "на високих швидкостях та виразний силует чотиридверного купе."
            ),
            'kona': (
                "Hyundai Kona — яскравий, сміливий та ультрасучасний компактний кросовер, створений "
                "для активного міського життя. Він миттєво виділяється в потоці завдяки футуристичній "
                "лінії підсвічування 'Seamless Horizon'. Модель пропонує дивовижний простір для свого класу, "
                "величезну кількість інтелектуальних помічників безпеки Smart Sense та високий кліренс "
                "для впевнених подорожей за межі асфальту."
            ),
            'ioniq5': (
                "Hyundai Ioniq 5 — повністю електричний кросовер нового покоління, який ламає стереотипи. "
                "Побудований на революційній електро-платформі E-GMP, він вражає своїм ретро-футуристичним "
                "піксельним дизайном. Салон розроблений за концепцією 'Smart Living Space' з абсолютно плавною "
                "підлогою та сидіннями-шезлонгами. Модель підтримує надшвидку зарядку та здатна живити сторонні "
                "електроприлади прямо від батареї автомобіля."
            ),
            'venue': (
                "Hyundai Venue — найкомпактніший, маневрений та неймовірно практичний кросовер у лінійці. "
                "Він ідеально підходить для вузьких міських вулиць та щоденних поїздок. Попри компактні "
                "зовнішні розміри, продумана ергономіка салону забезпечує максимум простору та затишку для пасажирів. "
                "Двоколірне забарвлення кузова, сучасна мультимедіа та висока посадка роблять його кращим вибором "
                "як для першого автомобіля."
            ),
            'tucson': (
                "Hyundai Tucson — світовий бестселер та справжня дизайнерська运行 революція у класі позашляховиків. "
                "Його головна особливість — унікальна прихована оптика, яка повністю зливається з параметричною "
                "решіткою радіатора у вимкненому стані. Розкішний двозонний інтер'єр преміум-класу, інтелектуальний "
                "повний привід HTRAC та передові гібридні двигуни дарують безкомпромісну впевненість і комфорт у будь-якій подорожі."
            ),
            'inster': (
                "Hyundai Inster — абсолютно новий, повністю електричний міський субкомпактний кросовер. "
                "Він поєднує в собі унікальний кубічний дизайн, фірмову піксельну оптику та дивовижну трансформацію салону: "
                "всі сидіння, включаючи водійське, можуть складатися в абсолютно рівну підлогу. "
                "Inster — це екологічний, маневрений та технологічний гаджет на колесах із солідним запасом ходу для мегаполіса."
            ),
            'santa fe': (
                "Hyundai Santa Fe — флагманського повнорозмірний сімейний кросовер, який отримав радикальний "
                "брутальний дизайн з характерними H-подібними елементами оптики. Головна філософія моделі — "
                "максимальний простір. Величезні двері багажника перетворюють задню частину авто на відкриту терасу "
                "для відпочинку на природі. Доступний у версіях на 5, 6 або 7 місць, цей автомобіль створений для "
                "подорожей першим класом."
            ),
            'staria': (
                "Hyundai Staria — футуристичний мінівен космічного дизайну, який повністю змінює уявлення про "
                "пасажирські перевезення. Силует, що нагадує космічний корабель, панорамні вікна та розкішні VIP-крісла "
                "з підставками для ніг (оттоманками) у другому ряду створюють атмосферу приватного бізнес-джета. "
                "Ідеальний вибір для великих родин, преміального трансферу та комфортного мобільного офісу."
            )
        }

        context['car_name'] = car_slug.title()
        context['car_img_name'] = car_slug.replace(' ', '_')
        context['car_description'] = car_descriptions.get(
            car_slug,
            "Сучасний автомобіль Hyundai, який поєднує в собі максимальний комфорт, надійність та передові технології."
        )

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


def test_drive(request, car_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        car = get_object_or_404(Car, id=car_id)

        TestDriveBooking.objects.create(
            name=name, phone=phone, car=car, date=date
        )
        return render(request, 'tasks/success.html')


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
        date = request.POST.get('date', '').strip()
        full_name = f"{first_name} {last_name}".strip()

        if first_name and phone:
            TestDriveBooking.objects.create(
                car=car,
                name=full_name,
                phone=phone,
                date=date
            )
            return redirect('success_page')
        return super().post(request, *args, **kwargs)


class ServiceView(CreateView):
    model = ServiceBooking
    form_class = ServiceBookingForm
    template_name = 'tasks/service_booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parts'] = SparePart.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect('service_success_page')
        return self.form_invalid(form)

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
            {'slug': 'staria', 'name': 'STARIA', 'price': 'від 2 100 000 грн', 'category': 'mpv'}, # Багатоцільові
        ]
        return context

class ServiceInfoView(TemplateView):
    template_name = 'tasks/service_info.html'