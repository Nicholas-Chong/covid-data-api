import pandas as pd
from datetime import datetime
from api.models import Report


def import_data():
    link1 = (
        'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/'
        'resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'
    )
    link2 = (
        'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/'
        'resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_i'
        'n_cases_by_phu.csv'
    )
    link3 = (
        'https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/'
        'resource/8a89caa9-511c-4568-af89-7f2174b4378c/download/vaccine_doses.csv'
    )

    str_to_date = lambda x: datetime.strptime(x, '%Y-%m-%d').date()
    net_new = lambda x: [x[0]] + [x[i] - x[i-1] for i in range(1, len(x))]
    remove_comma_to_int = lambda x: int(x.replace(',', ''))

    case_data = pd.read_csv(link1).fillna(0)
    vaxx_data = pd.read_csv(link3).fillna('0')

    vaxx_data['previous_day_doses_administered'] = (
        vaxx_data['previous_day_doses_administered'].apply(remove_comma_to_int)
    )
    vaxx_data['total_doses_administered'] = (
        vaxx_data['total_doses_administered'].apply(remove_comma_to_int)
    )
    vaxx_data['total_doses_in_fully_vaccinated_individuals '] = (
        vaxx_data['total_doses_in_fully_vaccinated_individuals '].apply(remove_comma_to_int)
    )
    vaxx_data['total_individuals_fully_vaccinated'] = (
        vaxx_data['total_individuals_fully_vaccinated'].apply(remove_comma_to_int)
    )

    daily_report = case_data.join(vaxx_data.set_index('report_date'), on='Reported Date')
    daily_report = daily_report.drop(columns=[
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
        'Number of patients hospitalized with COVID-19',
        'Total Positive LTC Resident Cases', 
        'Total LTC Resident Deaths',
    ])
    daily_report = daily_report.fillna(0)
    
    daily_report['Date'] = daily_report['Reported Date'].apply(str_to_date)
    daily_report['new_cases'] = net_new(daily_report['Total Cases'])
    daily_report['new_deaths'] = net_new(daily_report['Deaths'])
    daily_report['total_active'] = (
        daily_report['Total Cases'] - 
        daily_report['Deaths'] - 
        daily_report['Resolved']
    )
    daily_report['num_part_vaccinated'] = (
        daily_report['total_doses_administered'] - 
        daily_report['total_doses_in_fully_vaccinated_individuals ']
    )

    print(daily_report.columns)
    print(daily_report)

    for i in daily_report.iterrows():
        row = i[1].to_dict()
        report = Report.objects.create(
            date = row['Date'],
            date_string = row['Reported Date'],
            new_cases = row['new_cases'],
            new_deaths = row['new_deaths'],
            new_tests = row['Total tests completed in the last day'],
            total_cases = row['Total Cases'],
            total_deaths = row['Deaths'],
            total_resolved = row['Resolved'],
            total_active = row['total_active'],
            new_vaccinations = row['previous_day_doses_administered'],
            num_fully_vaccinated = row['total_individuals_fully_vaccinated'],
            num_part_vaccinated = row['num_part_vaccinated'],            
            variant_p1 = row['Total_Lineage_P.1'],
            variant_b1351 = row['Total_Lineage_B.1.351'],
            variant_b117 = row['Total_Lineage_B.1.1.7'],
        )
        print(report)


def run():
    import_data()

    








