from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from library.models import Book, Exemplar

from django.db.models import Count
from django.db.models import Q


class BooksListView(ListView):
    model = Book
    template_name = 'home.html'
    context_object_name = 'books'
    paginate_by = 1

    def get_queryset(self):
        search = self.request.GET.get('search', '')

        queryset = super().get_queryset().filter(
            Q(title__icontains=search) |
            Q(author__name__icontains=search)
        )

        return queryset


class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book-detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['instances'] = len(Exemplar.objects.filter(book=context['book'].id))

        return context


class BookCreateView(CreateView):
    model = Book
    template_name = 'crud/form.html'
    fields = '__all__'
    success_url = reverse_lazy('home')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'crud/form.html'
    fields = '__all__'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('book-detail', kwargs={"pk": pk})


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'crud/confirm-delete.html'
    success_url = reverse_lazy('home')


# class BookSearchView(ListView):
#