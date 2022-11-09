from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


class CostumUserAdmin(UserAdmin):
    list_display = ['username', 'last_name', 'first_name', 'email', 'age', 'is_staff', 'male']
    add_fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('age',)}),                                    )
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ['age', ]}),
                                       )
admin.site.register(CustomUser, CostumUserAdmin)