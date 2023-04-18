from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from library.models import Exemplar, Borrow, Book


class ExemplarListView(ListView):
    template_name = 'exemplar/exemplar-list.html'
    context_object_name = 'exemplars'

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


class ExemplarDetailView(DetailView):
    model = Exemplar
    template_name = 'exemplar/exemplar-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrow = Borrow.objects.filter(exemplar=kwargs.get('object'))

        if borrow and borrow.latest('end').status:
            borrower = borrow.latest('end').borrower
        else:
            borrower = 'none'

        context['borrower'] = borrower

        return context


class ExemplarCreateView(CreateView):
    model = Exemplar
    fields = ['publisher', 'code']
    success_url = reverse_lazy('home')
    template_name = 'crud/form.html'

    def form_valid(self, form):
        form.instance.book = Book.objects.get(id=self.kwargs['book'])
        response = super().form_valid(form)
        return response

    def get_success_url(self, **kwargs):
        return reverse_lazy('book-exemplars-list', kwargs={"book": self.object.book.id})
