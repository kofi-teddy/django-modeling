from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Member, through="Membership", related_name="groups")

    def __str__(self):
        return self.name


class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.member} is a member of {self.group}"