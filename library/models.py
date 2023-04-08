from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import datetime, timedelta


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


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(null=True)
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author)
    description = models.TextField(blank=True, null=True, default='It is a new book')
    category = models.ManyToManyField(Category)
    pub_date = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(null=True, blank=True, default='image1.jpeg')

    def __str__(self) -> str:
        return self.title


class Instance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    photo = models.ImageField(blank=True, null=True, default='default-image.png')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{Book.objects.get(id=self.book.id).title} - {self.code}"


class Borrower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # email = models.EmailField()
    debt = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


def get_time():
    return datetime.now() + timedelta(weeks=2)


class InstanceBorrower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    instance = models.ForeignKey('Instance', on_delete=models.CASCADE)
    borrower = models.ForeignKey('Borrower', on_delete=models.CASCADE)
    start = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True, default=get_time)

    def __str__(self):
        instance = Instance.objects.get(id=self.instance.id)
        # book = Book.objects.get(id=instance.book.id)

        borrower = Borrower.objects.get(id=self.borrower.id)

        return f"{borrower.first_name} {borrower.last_name} - {instance}"