from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .Forms import MyUserCreationForm

from .models import Book, Instance, Borrower
from django.db.models import Count
from django.core.mail import send_mail


def send_email(request):


    return redirect('home')


# class HomeView(TemplateView):
#     template_name = 'home.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class MyLogoutView(LogoutView):
    redirect_field_name = True


class BooksListView(ListView):
    model = Book
    template_name = 'home.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(instance_count=Count('instance'))
        return queryset


class BookDetailView(DetailView):
    model = Book
    template_name = 'crud/book-detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['instances'] = len(Instance.objects.filter(book=context['book'].id))

        return context


class BookCreateView(CreateView):
    model = Book
    template_name = 'crud/book-create.html'
    fields = '__all__'
    success_url = reverse_lazy('home')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'crud/book-create.html'
    fields = '__all__'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('book-detail', kwargs={"pk": pk})


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'crud/book-confirm-delete.html'
    success_url = reverse_lazy('home')


class CreateUser(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'crud/book-create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        password = User.objects.make_random_password()

        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        borrower = Borrower(user=user)
        borrower.save()

        send_mail(
            'Creating an account in Library application',
            f'Your passwords for {user.username} account: {password}',
            'noreply@tenirbook.com',
            [user.email],
        )

        response = super().form_valid(form)
        return response

