from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from library.models import Borrower, Borrow
from django.contrib.auth.models import User

from library.Forms import MyUserCreationForm

from django.core.mail import send_mail
from django.db.models import Q


class BorrowerListView(ListView):
    model = Borrower
    template_name = 'borrower/borrower-list.html'
    context_object_name = 'users'
    ordering = 'id'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        print(search)


        queryset = super().get_queryset().filter(
            Q(user__first_name__icontains=search)
        )

        # for borrower in queryset:
        #     borrower.can_borrow_book()
        #     print(borrower.has_exemplar())

        for borrow in Borrow.objects.filter(status=1):
            borrow.calculate_fine()

        return queryset


class BorrowerDetailView(DetailView):
    model = Borrower
    template_name = 'borrower/borrower-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exemplar'] = self.object.has_exemplar()

        return context


class BorrowerCreateView(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'crud/form.html'
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


class BorrowerUpdateView(UpdateView):
    model = Borrower
    form_class = MyUserCreationForm
    template_name = 'crud/form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('borrower-detail', kwargs={'pk': self.object.borrower.id})