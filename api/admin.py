from django.contrib import admin
from .models import (
    Report, TimeseriesCases, TimeseriesCasesRegional, TimeseriesVaccination,
    PublicHealthUnit, TimeseriesVariant,
)

# Register your models here.
admin.site.register(Report)
admin.site.register(TimeseriesCases)
admin.site.register(TimeseriesCasesRegional)
admin.site.register(TimeseriesVaccination)
admin.site.register(PublicHealthUnit)
admin.site.register(TimeseriesVariant)