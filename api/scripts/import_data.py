import pandas as pd
from datetime import datetime
from api.models import (
    Report, TimeseriesCases, TimeseriesCasesRegional, TimeseriesVaccination,
    PublicHealthUnit
)


def create_phus():
    data_disp = ['Algoma Public Health', 'Brant County Health', 'Chatham-Kent Health', 'Durham Region Health Department', 'Eastern Ontario Health', 'Grey Bruce Health', 'Haldimand-Norfolk Health', 'Haliburton, Kawartha, Pine Ridge District Health', 'Halton Region Health Department', 'Hamilton Public Health Services', 'Hastings and Prince Edward Counties Health', 'Huron Perth District Health', 'Kingston, Frontenac and Lennox & Addington Public Health', 'Lambton Public Health', 'Leeds, Grenville and Lanark District Health', 'Middlesex-London Health', 'Niagara Region Public Health Department', 'North Bay Parry Sound District Health', 'Northwestern Health', 'Ottawa Public Health', 'Peel Public Health', 'Peterborough Public Health', 'Porcupine Health', 'Region of Waterloo, Public Health', 'Renfrew County and District Health', 'Simcoe Muskoka District Health', 'Southwestern Public Health', 'Sudbury & District Health', 'Thunder Bay District Health', 'Timiskaming Health', 'Toronto Public Health', 'Wellington-Dufferin-Guelph Public Health', 'Windsor-Essex County Health', 'York Region Public Health Services']
    data_ont = ['Algoma_Public_Health_Unit', 'Brant_County_Health_Unit', 'Chatham-Kent_Health_Unit', 'Durham_Region_Health_Department', 'Eastern_Ontario_Health_Unit', 'Grey_Bruce_Health_Unit', 'Haldimand-Norfolk_Health_Unit', 'Haliburton,_Kawartha,_Pine_Ridge_District_Health_Unit', 'Halton_Region_Health_Department', 'Hamilton_Public_Health_Services', 'Hastings_and_Prince_Edward_Counties_Health_Unit', 'Huron_Perth_District_Health_Unit', 'Kingston,_Frontenac_and_Lennox_&_Addington_Public_Health', 'Lambton_Public_Health', 'Leeds,_Grenville_and_Lanark_District_Health_Unit', 'Middlesex-London_Health_Unit', 'Niagara_Region_Public_Health_Department', 'North_Bay_Parry_Sound_District_Health_Unit', 'Northwestern_Health_Unit', 'Ottawa_Public_Health', 'Peel_Public_Health', 'Peterborough_Public_Health', 'Porcupine_Health_Unit', 'Region_of_Waterloo,_Public_Health', 'Renfrew_County_and_District_Health_Unit', 'Simcoe_Muskoka_District_Health_Unit', 'Southwestern_Public_Health', 'Sudbury_&_District_Health_Unit', 'Thunder_Bay_District_Health_Unit', 'Timiskaming_Health_Unit', 'Toronto_Public_Health', 'Wellington-Dufferin-Guelph_Public_Health', 'Windsor-Essex_County_Health_Unit', 'York_Region_Public_Health_Services']

    for i in range(len(data_ont)):
        PublicHealthUnit(display_name=data_disp[i], ontario_name=data_ont[i]).save()


def create_timeseries_cases():
    # Status of COVID-19 Cases in Ontario
    link1 = (
        'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/'
        'resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'
    )
    summary_ontario = pd.read_csv(link1)
    summary_ontario =summary_ontario.drop(columns=[
        'Confirmed Negative',
        'Confirmed Positive',
        'Presumptive Negative',
        'Presumptive Positive',
        'Under Investigation',
        'Total patients approved for testing as of Reporting Date',
        'Total Positive LTC HCW Cases',
        'Total LTC HCW Deaths',
        'Number of patients in ICU on a ventilator due to COVID-19',
        'Num. of patients in ICU on a ventilator testing positive',
        'Num. of patients in ICU on a ventilator testing negative',
        'Number of patients in ICU, testing negative for COVID-19',
        'Number of patients in ICU, testing positive for COVID-19',
        'Number of patients in ICU due to COVID-19',
        'Number of patients hospitalized with COVID-19'
    ])

    summary_ontario = summary_ontario.fillna(0)

    net_new = lambda x: [0] + [x[i] - x[i-1] for i in range(1, len(x))]
    summary_ontario['new_cases'] = net_new(summary_ontario['Total Cases'])
    summary_ontario['new_deaths'] = net_new(summary_ontario['Deaths'])

    print(summary_ontario)

    for i in summary_ontario.iterrows():
        row = i[1].to_dict()
        date = datetime.strptime(row['Reported Date'], '%Y-%m-%d').date()

        report = Report.objects.create(date=date)
        TimeseriesCases.objects.create(
            report=report,
            new_cases=row['new_cases'],
            new_deaths=row['new_deaths'],
            new_tests=row['Total tests completed in the last day'],
            total_cases=row['Total Cases'],
            total_deaths=row['Deaths'],
        )


def create_timeseries_cases_regional():
    link2 = (
        'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/'
        'resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_i'
        'n_cases_by_phu.csv'
    )

    daily_change_phu = pd.read_csv(link2)
    daily_change_phu = daily_change_phu.drop(columns=['Total'])
    daily_change_phu = daily_change_phu.fillna(0)

    for i in daily_change_phu.iterrows():
        row = i[1]
        date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
        report = Report.objects.get(date=date)

        for j in daily_change_phu.columns[1:]:
            phu = PublicHealthUnit.objects.get(ontario_name=j)
            TimeseriesCasesRegional.objects.create(
                report=report,
                phu=phu,
                new_cases=row[j]
            )


def create_timeseries_vaccination():
    # COVID-19 Vaccine Data
    link3 = (
        'https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/'
        'resource/8a89caa9-511c-4568-af89-7f2174b4378c/download/vaccine_doses.csv'
    )
    vaccine_data = pd.read_csv(link3)
    vaccine_data = vaccine_data.fillna('0')

    remove_comma = lambda x: x.replace(',', '')

    vaccine_data['previous_day_doses_administered'] = (
        vaccine_data['previous_day_doses_administered'].apply(remove_comma)
    )

    vaccine_data['total_doses_administered'] = (
        vaccine_data['total_doses_administered'].apply(remove_comma)
    )

    vaccine_data['total_doses_in_fully_vaccinated_individuals '] = (
        vaccine_data['total_doses_in_fully_vaccinated_individuals '].apply(remove_comma)
    )

    vaccine_data['total_individuals_fully_vaccinated'] = (
        vaccine_data['total_individuals_fully_vaccinated'].apply(remove_comma)
    )

    print(vaccine_data)

    for i in vaccine_data.iterrows():
        row = i[1]
        date = datetime.strptime(row['report_date'], '%Y-%m-%d').date()
        report = Report.objects.get(date=date)
        TimeseriesVaccination.objects.create(
            report=report,
            new_vaccinations=row['previous_day_doses_administered'],
            num_fully_vaccinated=row['total_individuals_fully_vaccinated'],
            num_part_vaccinated=(
                int(row['total_doses_administered']) - 
                int(row['total_doses_in_fully_vaccinated_individuals '])
            ),
        )


def run():
    create_phus()
    create_timeseries_cases()
    create_timeseries_cases_regional()
    create_timeseries_vaccination()

    








