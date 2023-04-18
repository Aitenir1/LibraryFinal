from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class MyLogoutView(LogoutView):
    redirect_field_name = True
