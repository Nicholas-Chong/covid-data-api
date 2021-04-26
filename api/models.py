from django.db import models


class Report(models.Model):
    date = models.DateField()
    date_string = models.CharField(max_length=10)

    new_cases = models.IntegerField(default=0)
    new_deaths = models.IntegerField(default=0)
    new_tests = models.IntegerField(default=0)
    total_cases = models.IntegerField(default=0)
    total_deaths = models.IntegerField(default=0)
    total_resolved = models.IntegerField(default=0)
    total_active = models.IntegerField(default=0)

    new_vaccinations = models.IntegerField(default=0)
    num_fully_vaccinated = models.IntegerField(default=0)
    num_part_vaccinated = models.IntegerField(default=0)

    total_variant_p1 = models.IntegerField(default=0)
    total_variant_b1351 = models.IntegerField(default=0)
    total_variant_b117 = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)
