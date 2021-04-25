from django.db import models


class Report(models.Model):
    date = models.DateField()
    date_string = models.CharField(max_length=10)

    def __str__(self):
        return str(self.date)


class TimeseriesCases(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name='timeseries_cases'
    )
    new_cases = models.IntegerField(default=0)
    new_deaths = models.IntegerField(default=0)
    new_tests = models.IntegerField(default=0)
    total_cases = models.IntegerField(default=0)
    total_deaths = models.IntegerField(default=0)

    def __str__(self):
        return str(self.report.date)


class TimeseriesVaccination(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name='timeseries_vaccination'
    )
    new_vaccinations = models.IntegerField(default=0)
    num_fully_vaccinated = models.IntegerField(default=0)
    num_part_vaccinated = models.IntegerField(default=0)

    def __str__(self):
        return str(self.report.date)


class PublicHealthUnit(models.Model):
    display_name = models.CharField(max_length=200)
    ontario_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.ontario_name)


class TimeseriesCasesRegional(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name='timeseries_regional'
    )
    

    def __str__(self):
        return str(self.report.date)
