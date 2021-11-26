from django.contrib import admin

from .models import Member, Group, Membership

admin.site.register(Member)
admin.site.register(Group)
admin.site.register(Membership)
