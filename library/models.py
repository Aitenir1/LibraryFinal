from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone


class Borrower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    debt = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        # self.bor
        return f"{self.user.first_name} {self.user.last_name}"

    def has_exemplar(self):
        book = self.borrow_set.filter(status=1)

        if book:
            return book.first().exemplar

        return False

    def can_borrow_book(self):
        can_borrow = not (self.debt or self.borrow_set.filter(status=1))
        print('===================================')
        print(f"Borrower: {self}")
        print(f"Debt: {self.debt}")
        print(f"Borrows: {self.borrow_set.filter(end__lt=timezone.now())}")
        print(f"Active Borrows: {self.borrow_set.all().filter(status=1)}")
        print(f"Can borrow: {can_borrow}")

        return can_borrow


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.ManyToManyField('Author')
    description = models.TextField(blank=True, null=True, default='It is a new book')
    category = models.ManyToManyField('Category')
    pub_date = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(null=True, blank=True, default='image1.jpeg')

    def __str__(self) -> str:
        return self.title


class Exemplar(models.Model):
    STATUS_CHOICES = (
        (0, 'False'),
        (1, 'True'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    print_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{Book.objects.get(id=self.book.id).title} - {self.code}"


def get_time():
    return datetime.now() + timedelta(minutes=3)


class Borrow(models.Model):
    STATUS_CHOICES = (
        (0, 'False'),
        (1, 'True'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    exemplar = models.ForeignKey('Exemplar', on_delete=models.CASCADE)
    borrower = models.ForeignKey('Borrower', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    start = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True, default=get_time)

    def __str__(self):
        instance = Exemplar.objects.get(id=self.exemplar.id)
        # book = Book.objects.get(id=instance.book.id)

        borrower = Borrower.objects.get(id=self.borrower.id)

        return f"{borrower.user.first_name} {borrower.user.last_name} - {instance}"

    def calculate_fine(self):
        time_now = timezone.now()
        delta = (time_now - self.end)

        # print("====================================")
        # print(f"Borrower: {self.borrower}")
        # print(f"Delta: {time_now - self.end}")
        # print(f"Time now: {time_now}")
        # print(f"End date: {self.end}")
        # print(f"Delta date {delta}")

        if self.status and delta > timedelta(0):
            self.borrower.debt = delta.total_seconds()
            self.borrower.save()


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class Publisher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
