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
    total_resolved = models.IntegerField(default=0)
    total_active = models.IntegerField(default=0)

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
    Algoma_Public_Health_Unit = models.IntegerField(default=0)
    Brant_County_Health_Unit = models.IntegerField(default=0)
    Chatham_Kent_Health_Unit = models.IntegerField(default=0)
    Durham_Region_Health_Department = models.IntegerField(default=0)
    Eastern_Ontario_Health_Unit = models.IntegerField(default=0)
    Grey_Bruce_Health_Unit = models.IntegerField(default=0)
    Haldimand_Norfolk_Health_Unit = models.IntegerField(default=0)
    Haliburton_Kawartha_Pine_Ridge_District_Health_Unit = models.IntegerField(default=0)
    Halton_Region_Health_Department = models.IntegerField(default=0)
    Hamilton_Public_Health_Services = models.IntegerField(default=0)
    Hastings_and_Prince_Edward_Counties_Health_Unit = models.IntegerField(default=0)
    Huron_Perth_District_Health_Unit = models.IntegerField(default=0)
    Kingston_Frontenac_and_Lennox_and_Addington_Public_Health = models.IntegerField(default=0)
    Lambton_Public_Health = models.IntegerField(default=0)
    Leeds_Grenville_and_Lanark_District_Health_Unit = models.IntegerField(default=0)
    Middlesex_London_Health_Unit = models.IntegerField(default=0)
    Niagara_Region_Public_Health_Department = models.IntegerField(default=0)
    North_Bay_Parry_Sound_District_Health_Unit = models.IntegerField(default=0)
    Northwestern_Health_Unit = models.IntegerField(default=0)
    Ottawa_Public_Health = models.IntegerField(default=0)
    Peel_Public_Health = models.IntegerField(default=0)
    Peterborough_Public_Health = models.IntegerField(default=0)
    Porcupine_Health_Unit = models.IntegerField(default=0)
    Region_of_WaterlooPublic_Health = models.IntegerField(default=0)
    Renfrew_County_and_District_Health_Unit = models.IntegerField(default=0)
    Simcoe_Muskoka_District_Health_Unit = models.IntegerField(default=0)
    Southwestern_Public_Health = models.IntegerField(default=0)
    Sudbury_and_District_Health_Unit = models.IntegerField(default=0)
    Thunder_Bay_District_Health_Unit = models.IntegerField(default=0)
    Timiskaming_Health_Unit = models.IntegerField(default=0)
    Toronto_Public_Health = models.IntegerField(default=0)
    Wellington_Dufferin_Guelph_Public_Health = models.IntegerField(default=0)
    Windsor_Essex_County_Health_Unit = models.IntegerField(default=0)
    York_Region_Public_Health_Services = models.IntegerField(default=0)

    def __str__(self):
        return str(self.report.date)


class TimeseriesVariant(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name='variants'
    )
    p1 = models.IntegerField(default=0)
    b1351 = models.IntegerField(default=0)
    b117 = models.IntegerField(default=0)

    def __str__(self):
        return str(self.report.date)