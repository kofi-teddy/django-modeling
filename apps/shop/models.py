from random import choices

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.posgtres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models

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

# class Book(models.Model):
#     TYPE_PHYSICAL = "physical"
#     TYPE_VIRTUAL = "virtual"
#     TYPE_CHOICES = (
#         (TYPE_PHYSICAL, "Physical"),
#         (TYPE_VIRTUAL, "virtual"),
#     )
#     type = models.CharField(
#         max_length=20,
#         choices=TYPE_CHOICES,
#     )

#     # Common attributes
#     name = models.CharField(max_length=100)
#     price = models.PositiveIntegerField(
#         help_text="in cedis",
#     )

#     # Specific attributes
#     weight = models.PositiveIntegerField(
#         help_text="in grams",
#     )
#     download_link = models.URLField(null=True, blank=True)

#     def __str__(self) -> str:
#         return f"[{self.get_type_display()}] {self.name}"

#     def clean(self) -> None:
#         if self.type == Book.TYPE_VIRTUAL:
#             if self.weight != 0:
#                 raise ValidationError(
#                     'A virtual product weight cannot exceed zero.'
#                 )

#             if self.download_link is None:
#                 raise ValidationError(
#                     'A virtual product must have a download link.'
#                 )
#         elif self.type == Book.TYPE_PHYSICAL:
#             if self.weight == 0:
#                 raise ValidationError(
#                     'A physical product weight must exceed zero.'
#                 )
#             if self.download_link is not None:
#                 raise ValidationError(
#                     'A phsical product cannont have a download link.'
#                 )
#         else:
#             assert False, f'Unknown product type {self.type}'

# class Cart(models.Model):
#     user = models.OneToOneField(
#         get_user_model(), primary_key=True, on_delete=models.CASCADE
#     )
#     books = models.ManyToManyField(Book, related_name="products")


# Semi-Strutured Model
"""
In the sparse model approach, fields for every new type of 
product were added. The model now has a lot of nullable fields, 
and new developers and employees are having trouble keeping up.

To address the clutter, keep only the common fields 
(name and price) on the model. Store the rest of the fields in a 
single JSONField:
"""

# class Book(models.Model):
#     TYPE_PHYSICAL = 'physical'
#     TYPE_VIRTUAL = 'virtual'
#     TYPE_CHOICES = (
#         (TYPE_PHYSICAL, 'physical'),
#         (TYPE_VIRTUAL, 'virtual'),
#     )
#     type = models.CharField(
#         max_length=20,
#         choices=TYPE_CHOICES,
#     )

#     # Common attributes
#     name = models.CharField(max_length=100)
#     price = models.PositiveIntegerField(
#         help_text='in cedis',
#     )
#     extra = JSONField()

#     def __str__(self) -> str:
#         return f'[{self.get_type_display()}] {self.name}'

#     def clean(self) -> None:

#         if self.type == Book.TYPE_VIRTUAL:

#             try:
#                 weight = int(self.extra['weight'])
#             except ValueError:
#                 raise ValidationError(
#                     'Weight must be a number'
#                 )
#             except KeyError:
#                 pass
#             else:
#                 if weight != 0:
#                     raise ValidationError(
#                         'A virtual product weight cannot exceed zero.'
#                     )
#             try:
#                 download_link = self.extra['download_link']
#             except KeyError:
#                 pass
#             else:
#                 # will raise a validation error
#                 URLValidator()(download_link)

#         elif self.type == Book.TYPE_PHYSICAL:

#             try:
#                 weight = int(self.extra['weight'])
#             except ValueError:
#                 raise ValidationError('Weight must be a number')
#             except KeyError:
#                 pass
#             else:
#                 if weight == 0:
#                     raise VAlidationError(
#                         'A physical product weight must exceed zero.'
#                     )

#             try:
#                 download_link = self.extra['download_link']
#             except KeyError:
#                 pass
#             else:
#                 if download_link is not None:
#                     raise ValidationError('A physical product cannot have a download link.')
#         else:
#             raise ValidationError(f'Unknon product type "{self.type}" ')


# Abstract Base Model
"""
Adding additonal or different types of product such as e-readers, 
pens and notebooks.

A book and an e-book are both products. A product is defined 
using common attributes such as name and price. In an object-oriented 
environment, create a Product as a base class or an interface.

Define a Product abstract base class and add two models 
for Book and EBook.

An abstract base model is a good choice when there are very few 
types of objects that required very distinct logic.

An intuitive example is modeling a payment process for an online 
shop. There is the need to accept payments with credit cards, PayPal, and 
store credit. Each payment method goes through a very different 
process that requires very distinct logic. Adding a new type of 
payment is not very common, and theres no need in adding new payment 
methods in the future.

Create a payment process base class with derived classes for credit card 
payment process, PayPal payment process, and store credit payment 
process. For each of the derived classes, implement the payment process 
in a very different way that cannot be easily shared. In this case, 
it might make sense to handle each payment process specifically.
"""
# class Product(models.Model):
#     class Meta:
#         abstract = True

#     name = models.CharField(max_length=255)
#     price = models.PositiveIntegerField(
#         help_text='in cedis'
#     )

#     def __str__(self):
#         return self.name


# class Book(Product):
#     weight = models.PositiveIntegerField(
#         help_text='in cedis'
#     )


# class EBook(Product):
#     download_link = models.URLField()


# Concrete Base Model
"""
Django offers another way to implement inheritance in models. 
Instead of using an abstract base class that only exists in the code, 
make the base class concrete. “Concrete” means that the base class 
exists in the database as a table, unlike in the abstract base 
class solution, where the base class only exists in the code.

Using the abstract base model, it was impossible to reference 
multiple type of products. forcefully created a many-to-many 
relation for each type of product. This made it harder to 
perform tasks on the common fields such as getting the total price 
of all the items in the cart.

Using a concrete base class, Django will create a table in the database 
for the Product model. The Product model will have all the common 
fields you defined in the base model. Derived models such as Book and 
EBook will reference the Product table using a one-to-one field. 
To reference a product, you create a foreign key to the base model.

The concrete base model approach is useful when common fields in the 
base class are sufficient to satisfy most common queries.

For example, if there is the need to query for the cart total price, 
show a list of items in the cart, or run ad hoc analytic queries 
on the cart model, there is a possibility to benefit from having 
all the common attributes in a single database table.
"""


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(help_text="in cedis")

    def __str__(self) -> str:
        return self.name


class Book(Product):
    weight = models.PositiveIntegerField()


class EBook(Product):
    download_link = models.URLField()


# Generic Foreign Key
"""
Django offers a special way of referencing any model in the project 
called GenericForeignKey. Generic foreign keys are part of the 
Content Types framework built into Django. The content type framework 
is used by Django itself to keep track of models. This is necessary 
for some core capabilities such as migrations and permissions.
"""


class Cart(models.Model):
    user = model.OneToOneField(
        get_user_model(),
        primary_key=True,
        on_delete=models.CASCADE,
    )


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_object_id = models.IntegerField()
    product_content_type = models.IntegerField()
    product_content_type = models.ForeignKey(
       ContentType,
       on_delete=models.PROTECT, 
    )
    product = GenericForeignKey(
        'product_content_type',
        'product_object_id',
    )
    

# class Cart(models.Model):
#     user = models.OneToOneField(
#         get_user_model(),
#         primary_key = True,
#         on_delete=models.CASCADE,
#     )
#     items = models.ManyToManyField(
#         Book,
#         related_name='+',
#     )


# class Cart(models.Model):
#     user = models.OneToOneField(
#         get_user_model(),
#         primary_key = True,
#         on_delete=models.CASCADE,
#     )
#     books = models.ManyToManyField(
#         Book,
#         related_name='+',
#     )
#     ebooks = models.ManyToManyField(EBook, related_name='+',)
