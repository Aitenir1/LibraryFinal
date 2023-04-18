# from django.views.generic import ListView, DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.contrib.auth.views import LoginView, LogoutView
# from django.urls import reverse_lazy, reverse
# from django.contrib.auth.models import User
# from .Forms import MyUserCreationForm
#
# from .models import Book, Exemplar, Borrower, Borrow
# from django.db.models import Count
# from django.core.mail import send_mail
#
# from django.utils import timezone
#
# from django.shortcuts import redirect
#
#
# class MyLoginView(LoginView):
#     redirect_authenticated_user = True
#     template_name = 'login.html'
#
#     def get_success_url(self):
#         return reverse_lazy('home')
#
#
# class MyLogoutView(LogoutView):
#     redirect_field_name = True
#
#
# class BooksListView(ListView):
#     model = Book
#     template_name = 'home.html'
#     context_object_name = 'books'
#
#     def get_queryset(self):
#
#         queryset = super().get_queryset()
#         queryset = queryset.annotate(instance_count=Count('exemplar'))
#         return queryset
#
#
# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'crud/book-detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(BookDetailView, self).get_context_data(**kwargs)
#         context['instances'] = len(Exemplar.objects.filter(book=context['book'].id))
#
#         return context
#
#
# class BookCreateView(CreateView):
#     model = Book
#     template_name = 'crud/form.html'
#     fields = '__all__'
#     success_url = reverse_lazy('home')
#
#
# class BookUpdateView(UpdateView):
#     model = Book
#     template_name = 'crud/form.html'
#     fields = '__all__'
#
#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         return reverse('book-detail', kwargs={"pk": pk})
#
#
# class BookDeleteView(DeleteView):
#     model = Book
#     template_name = 'crud/confirm-delete.html'
#     success_url = reverse_lazy('home')
#
#
# class CreateUserView(CreateView):
#     model = User
#     form_class = MyUserCreationForm
#     template_name = 'crud/form.html'
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         password = User.objects.make_random_password()
#
#         user = form.save(commit=False)
#         user.set_password(password)
#         user.save()
#
#         borrower = Borrower(user=user)
#         borrower.save()
#
#         send_mail(
#             'Creating an account in Library application',
#             f'Your passwords for {user.username} account: {password}',
#             'noreply@tenirbook.com',
#             [user.email],
#         )
#
#         response = super().form_valid(form)
#         return response
#
#
# class UserListView(ListView):
#     model = Borrower
#     template_name = 'borrower-list.html'
#     context_object_name = 'users'
#     ordering = 'id'
#
#     def get_queryset(self):
#         users = Borrower.objects.all()
#
#         for borrow in Borrow.objects.filter(status=1):
#             borrow.calculate_fine()
#
#         return users
#
#
# class BookExemplarListView(ListView):
#     template_name = 'exemplar-list.html'
#     context_object_name = 'exemplars'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context['book'] = self.kwargs['book']
#         return context
#
#     def get_queryset(self):
#         exemplars = Exemplar.objects.filter(book=self.kwargs['book'])
#
#         for exemplar in exemplars:
#
#             borrows = Borrow.objects.filter(exemplar=exemplar)
#
#             if not (borrows and borrows.latest('end').status):
#                 exemplar.status = 1
#                 exemplar.save()
#
#             else:
#                 exemplar.status = 0
#                 exemplar.save()
#
#                 borrows.latest('end').exemplar = exemplar
#                 borrows.latest('end').save()
#
#         return exemplars
#
#
# class BookExemplarCreateView(CreateView):
#     model = Exemplar
#     fields = ['publisher', 'code']
#     success_url = reverse_lazy('home')
#     template_name = 'crud/form.html'
#
#     def form_valid(self, form):
#         form.instance.book = Book.objects.get(id=self.kwargs['book'])
#         response = super().form_valid(form)
#         return response
#
#     def get_success_url(self, **kwargs):
#         return reverse_lazy('book-exemplars-list', kwargs={"book": self.object.book.id})
#
#
# class ExemplarDetailView(DetailView):
#     model = Exemplar
#     template_name = 'exemplar-detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         borrow = Borrow.objects.filter(exemplar=kwargs.get('object'))
#
#         if borrow and borrow.latest('end').status:
#             borrower = borrow.latest('end').borrower
#         else:
#             borrower = 'none'
#
#         context['borrower'] = borrower
#
#         return context
#
#
# class BorrowCreateView(CreateView):
#     model = Borrow
#     fields = ['borrower']
#     success_url = reverse_lazy('home')
#     template_name = 'crud/form.html'
#
#     def form_valid(self, form):
#         last_borrow = Borrow.objects.filter(borrower=form.instance.borrower).last()
#
#         if form.instance.borrower.debt:
#             form.add_error('borrower', 'The user has\'t paid the fine')
#
#             return self.form_invalid(form)
#
#         if last_borrow is not None and timezone.now() < last_borrow.end:
#             form.add_error('borrower', 'The user has already borrowed a book')
#
#             return self.form_invalid(form)
#
#         exemplar = Exemplar.objects.get(id=self.kwargs['exemplar'])
#         exemplar.status = 0
#         exemplar.save()
#
#         form.instance.exemplar = exemplar
#
#         response = super().form_valid(form)
#         return response
#
#     def get_success_url(self):
#         return reverse_lazy('exemplar-detail', kwargs={'pk': self.object.exemplar.id})
#
#
# class BorrowerDetailView(DetailView):
#     model = Borrower
#     template_name = 'borrower-detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         borrows = Borrow.objects.filter(borrower=self.object)
#         if borrows.exists():
#             context['has_book'] = borrows.latest('end').status
#         else:
#             context['has_book'] = 0
#
#         return context
#
#
# class BorrowerUpdateView(UpdateView):
#     model = Borrower
#     form_class = MyUserCreationForm
#     template_name = 'crud/form.html'
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def get_success_url(self):
#         return reverse_lazy('borrower-detail', kwargs={'pk': self.object.borrower.id})
#
#
# def clear_fine(request, pk):
#     borrower = Borrower.objects.get(id=pk)
#     borrower.debt = 0
#     borrower.save()
#
#     return redirect('borrower-detail', pk=borrower.id)
#
#
# def end_borrow(request, pk):
#     borrower = Borrower.objects.get(id=pk)
#
#     last_borrow = Borrow.objects.filter(borrower=borrower).latest('end')
#     last_borrow.status = 0
#     last_borrow.save()
#
#     return redirect('borrower-detail', pk=pk)
