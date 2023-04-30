from django.contrib.auth.mixins import UserPassesTestMixin

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from library.models import Exemplar, Borrow, Book


class ExemplarListView(UserPassesTestMixin, ListView):
    template_name = 'exemplar/exemplar-list.html'
    context_object_name = 'exemplars'

    def test_func(self):
        return self.request.user.has_perm('library.list_view_exemplar')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['book'] = self.kwargs['book']
        return context

    def get_queryset(self):
        exemplars = Exemplar.objects.filter(book=self.kwargs['book'])

        for exemplar in exemplars:

            borrows = Borrow.objects.filter(exemplar=exemplar)

            if not (borrows and borrows.latest('end').status):
                exemplar.status = 1
                exemplar.save()

            else:
                exemplar.status = 0
                exemplar.save()

                borrows.latest('end').exemplar = exemplar
                borrows.latest('end').save()

        return exemplars


class ExemplarDetailView(UserPassesTestMixin, DetailView):
    model = Exemplar
    template_name = 'exemplar/exemplar-detail.html'

    def test_func(self):
        return self.request.user.has_perm('library.view_exemplar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        borrows = Borrow.objects.filter(exemplar=self.object)

        if borrows and borrows.latest('end').status:
            borrower = borrows.latest('end').borrower
        else:
            borrower = 'none'

        context['borrows'] = borrows.order_by('start').reverse()
        context['borrower'] = borrower

        return context


class ExemplarCreateView(UserPassesTestMixin, CreateView):
    model = Exemplar
    fields = ['publisher', 'code']
    # success_url = reverse_lazy('home')
    template_name = 'crud/form.html'

    def test_func(self):
        return self.request.user.has_perm('library.create_exemplar')

    def form_valid(self, form):
        form.instance.book = Book.objects.get(id=self.kwargs['book'])
        response = super().form_valid(form)
        print(response)
        return response

    def get_success_url(self, **kwargs):
        return reverse_lazy('exemplar-list', kwargs={"book": self.object.book.id})
