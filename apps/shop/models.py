from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError


# use case
"""
You sell only one type of product: books. In your online store, 
you want to show details about the books, like name and price. 
You want your users to browse around the website and collect many 
books, so you also need a cart. You eventually need to ship the 
books to the user, so you need to know the weight of each book to 
calculate the delivery fee.
"""


# Naive Implementation
"""
Pro

Easy to understand and maintain: It’s sufficient for a single 
type of product.

Con
Restricted to homogeneous products: It only supports products 
with the same set of attributes. Polymorphism is not captured 
or permitted at all.
"""


# class Book(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.PositiveIntegerField(help_text="in cedis",)
#     weight = models.PositiveIntegerField(help_text="in grams",)

#     def __str__(self):
#         return self.name


# class Cart(models.Model):
#     user = models.OneToOneField(get_user_model(), primary_key=True, on_delete=models.CASCADE)
#     books = models.ManyToManyField(Book, related_name="products")


# Sparse Model
"""
With the success of the online bookstore, users started to ask if 
the shop sell e-books. E-books are a great product for the online 
store.
A physical book is different from an e-book:
An e-book has no weight. It’s a virtual product.
An e-book does not require shipment. Users download it from the website.
"""

class Book(models.Model):
    TYPE_PHYSICAL = "physical"
    TYPE_VIRTUAL = "virtual"
    TYPE_CHOICES = (
        (TYPE_PHYSICAL, "Physical"),
        (TYPE_VIRTUAL, "virtual"),
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )

    # Common attributes
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(
        help_text="in cedis",
    )

    # Specific attributes
    weight = models.PositiveIntegerField(
        help_text="in grams",
    )
    download_link = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return f"[{self.get_type_display()}] {self.name}"

    def clean(self) -> None:
        if self.type == Book.TYPE_VIRTUAL:
            if self.weight != 0:
                raise ValidationError(
                    'A virtual product weight cannot exceed zero.'
                )

            if self.download_link is None:
                raise ValidationError(
                    'A virtual product must have a download link.'
                )
        elif self.type == Book.TYPE_PHYSICAL:
            if self.weight == 0:
                raise ValidationError(
                    'A physical product weight must exceed zero.'
                )
            if self.download_link is not None:
                raise ValidationError(
                    'A phsical product cannont have a download link.'
                )
        else:
            assert False, f'Unknown product type {self.type}'

class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(), primary_key=True, on_delete=models.CASCADE
    )
    books = models.ManyToManyField(Book, related_name="products")


