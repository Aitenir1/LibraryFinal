from django.contrib.auth.mixins import UserPassesTestMixin

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from library.models import Borrower, Borrow
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from library.Forms import MyUserCreationForm

from django.core.mail import send_mail
from django.db.models import Q


class BorrowerListView(UserPassesTestMixin, ListView):
    model = Borrower
    template_name = 'borrower/borrower-list.html'
    context_object_name = 'users'
    ordering = 'id'

    def test_func(self):
        return self.request.user.has_perm('library.view_borrower')

    def get_queryset(self):
        search = self.request.GET.get('search', '')

        queryset = super().get_queryset().filter(
            Q(user__first_name__icontains=search)
        )



        for borrow in Borrow.objects.filter(status=1):
            borrow.calculate_fine()

        return queryset


class BorrowerDetailView(UserPassesTestMixin, DetailView):
    model = Borrower
    template_name = 'borrower/borrower-detail.html'

    def test_func(self):
        return self.request.user.has_perm('library.detail_view_borrower')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        borrows = Borrow.objects.filter(borrower=self.object)

        if borrows and borrows.latest('end').status:
            borrows.latest('end').calculate_fine()

        context['borrows'] = borrows.order_by('end').reverse()
        context['exemplar'] = self.object.has_exemplar()

        return context


class BorrowerCreateView(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'crud/form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.has_perm('library.create_borrower')

    def form_valid(self, form):
        password = User.objects.make_random_password()

        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        students_group = Group.objects.get(name='students')
        students_group.user_set.add(user)

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


class BorrowerUpdateView(UserPassesTestMixin, UpdateView):
    model = Borrower
    form_class = MyUserCreationForm
    template_name = 'crud/form.html'

    def test_func(self):
        return self.request.user.has_perm('library.change_borrower')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('borrower-detail', kwargs={'pk': self.object.borrower.id})