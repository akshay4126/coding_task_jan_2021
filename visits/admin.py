from django.contrib import admin

# Register your models here.

from visits.models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
