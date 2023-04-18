from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from library.models import Borrow, Exemplar

from django.utils import timezone


class BorrowCreateView(CreateView):
    model = Borrow
    fields = ['borrower']
    success_url = reverse_lazy('home')
    template_name = 'crud/form.html'

    def form_valid(self, form):
        last_borrow = Borrow.objects.filter(borrower=form.instance.borrower).last()

        if form.instance.borrower.debt:
            form.add_error('borrower', 'The user has\'t paid the fine')

            return self.form_invalid(form)

        if last_borrow is not None and timezone.now() < last_borrow.end:
            form.add_error('borrower', 'The user has already borrowed a book')

            return self.form_invalid(form)

        exemplar = Exemplar.objects.get(id=self.kwargs['exemplar'])
        exemplar.status = 0
        exemplar.save()

        form.instance.exemplar = exemplar

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('exemplar-detail', kwargs={'pk': self.object.exemplar.id})