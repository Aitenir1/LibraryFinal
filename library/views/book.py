from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from library.models import Book, Exemplar

from django.db.models import Count
from django.db.models import Q

class BooksListView(UserPassesTestMixin, ListView):
    model = Book
    template_name = 'home.html'
    context_object_name = 'books'

    def test_func(self):
        return self.request.user.has_perm('library.add_book')

    def get_queryset(self):
        search = self.request.GET.get('search', '')

        queryset = super().get_queryset().filter(
            Q(title__icontains=search) |
            Q(author__name__icontains=search)
        )

        return queryset


class BookDetailView(UserPassesTestMixin, DetailView):
    model = Book
    template_name = 'book/book-detail.html'

    def test_func(self):
        return self.request.user.has_perm('library.view_book')

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['instances'] = len(Exemplar.objects.filter(book=context['book'].id))

        return context


class BookCreateView(UserPassesTestMixin, CreateView):
    model = Book
    template_name = 'crud/form.html'
    fields = '__all__'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.has_perm('library.add_book')


class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    template_name = 'crud/form.html'
    fields = '__all__'

    def test_func(self):
        return self.request.user.has_perm('library.change_book')

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('book-detail', kwargs={"pk": pk})


class BookDeleteView(UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'crud/confirm-delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.has_perm('library.delete_book')