from django.shortcuts import redirect

from library.models import Borrower, Borrow


def clear_fine(request, pk):
    borrower = Borrower.objects.get(id=pk)
    borrower.debt = 0
    borrower.save()

    return redirect('borrower-detail', pk=borrower.id)


def end_borrow(request, pk):
    borrower = Borrower.objects.get(id=pk)

    last_borrow = Borrow.objects.filter(borrower=borrower).latest('end')
    last_borrow.status = 0
    last_borrow.save()

    return redirect('borrower-detail', pk=pk)