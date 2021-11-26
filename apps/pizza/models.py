from django.db import models
from django.utils.translation import gettext_lazy as _


class Pizza(models.Model):
    name = models.CharField(_("name of pizza"), max_length=50)
    toppings = models.ManyToManyField(
        "Topping",
        verbose_name=_("toppings"),
        related_name="pizzas",
        through="ToppingAmount",
    )

    def __str__(self) -> str:
        return self.name


class Topping(models.Model):
    name = models.CharField(_("name of toppings"), max_length=50)

    def __str__(self) -> str:
        return self.name


class ToppingAmount(models.Model):
    class AmountChoices(models.IntegerChoices):
        REGULAR = 1, _("Regular")
        DOUBLE = 2, _("Double")
        TRIPPLE = 3, _("Tripple")

    pizza = models.ForeignKey(
        Pizza,
        related_name="topping_amounts",
        verbose_name=_("Pizza"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    topping = models.ForeignKey(
        Topping,
        related_name="topping_amounts",
        verbose_name=_("Topping"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    amount = models.IntegerField(
        _("amount"),
        choices=AmountChoices.choices,
        default=AmountChoices.REGULAR,
    )

    def __str__(self) -> str:
        return f"{self.amount} of {self.topping}"