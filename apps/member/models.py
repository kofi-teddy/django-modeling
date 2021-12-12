from django.db import models
from django.utils.translation import ugettext_lazy as _


class Member(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(_("name"), max_length=128)
    members = models.ManyToManyField(
        Member,
        through="Membership",
        related_name="groups",
        through_fields=("group", "member"),
        verbose_name=_("group members"),
    )

    def __str__(self):
        return self.name


class Membership(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name=_("member"),
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name=_("group"),
    )
    inviter = models.ForeignKey(
        Member,
        verbose_name=_("inviter"),
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.member} is a member of {self.group}"