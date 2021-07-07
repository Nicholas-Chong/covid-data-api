import pandas as pd
from datetime import datetime
from api.models import Report, RegionalReport


def update_report():
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
    remove_comma_to_int = lambda x: int(str(x).replace('.0', ''))

    case_data = pd.read_csv(link1).fillna(0).tail(5).reset_index(drop=True)
    vaxx_data = pd.read_csv(link3).fillna('0').tail(5).reset_index(drop=True)

    # vaxx_data['previous_day_doses_administered'] = (
    #     vaxx_data['previous_day_doses_administered'].apply(remove_comma_to_int)
    # )
    vaxx_data['total_doses_administered'] = (
        vaxx_data['total_doses_administered'].apply(remove_comma_to_int)
    )
    vaxx_data['total_doses_in_fully_vaccinated_individuals'] = (
        vaxx_data['total_doses_in_fully_vaccinated_individuals'].apply(remove_comma_to_int)
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
        daily_report['total_doses_in_fully_vaccinated_individuals']
    )
    daily_report['positivity'] = list((
            daily_report['new_cases'] / 
            daily_report['Total tests completed in the last day'] * 100
        ).round(2)
    )

    latest_record_db = Report.objects.latest('date').date
    new_records = daily_report.loc[latest_record_db < daily_report['Date']]
    print(new_records)

    for i in new_records.iterrows():
        row = i[1].to_dict()
        report = Report.objects.create(
            date = row['Date'],
            date_string = row['Reported Date'],
            new_cases = row['new_cases'],
            new_deaths = row['new_deaths'],
            new_tests = row['Total tests completed in the last day'],
            test_positivity = row['positivity'],
            total_cases = row['Total Cases'],
            total_deaths = row['Deaths'],
            total_resolved = row['Resolved'],
            total_active = row['total_active'],
            new_vaccinations = row['previous_day_total_doses_administered'],
            num_fully_vaccinated = row['total_individuals_fully_vaccinated'],
            num_part_vaccinated = row['num_part_vaccinated'],            
            total_variant_p1 = row['Total_Lineage_P.1_Gamma'],
            total_variant_b1351 = row['Total_Lineage_B.1.351_Beta'],
            total_variant_b117 = row['Total_Lineage_B.1.1.7_Alpha'],
        )
        print(report)
    

def update_regional_report():
    link2 = (
        'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/'
        'resource/8a88fe6d-d8fb-41a3-9d04-f0550a44999f/download/daily_change_i'
        'n_cases_by_phu.csv'
    )
    str_to_date = lambda x: datetime.strptime(x, '%Y-%m-%d').date()

    daily_change_phu = pd.read_csv(link2).tail(5).reset_index(drop=True)
    daily_change_phu = daily_change_phu.drop(columns=['Total'])
    daily_change_phu = daily_change_phu.fillna(0)
    daily_change_phu['Date Obj'] = daily_change_phu['Date'].apply(str_to_date)

    latest_record_db = RegionalReport.objects.latest('date').date
    new_records = daily_change_phu.loc[latest_record_db < daily_change_phu['Date Obj']]
    print(new_records)

    records = new_records.to_dict(orient='records')

    for i in records:
        RegionalReport.objects.create(
            date = datetime.strptime(i['Date'], '%Y-%m-%d').date(),
            date_string = i['Date'],
            Algoma_Public_Health_Unit =  i['Algoma_District'],
            Brant_County_Health_Unit =  i['Brant_County'],
            Chatham_Kent_Health_Unit =  i['Chatham_Kent'],
            Durham_Region_Health_Department =  i['Durham_Region'],
            Eastern_Ontario_Health_Unit =  i['Eastern_Ontario'],
            Grey_Bruce_Health_Unit =  i['Grey_Bruce'],
            Haldimand_Norfolk_Health_Unit =  i['Haldimand_Norfolk'],
            Haliburton_Kawartha_Pine_Ridge_District_Health_Unit =  i['Haliburton_Kawartha_Pine_Ridge'],
            Halton_Region_Health_Department =  i['Halton_Region'],
            Hamilton_Public_Health_Services =  i['City_of_Hamilton'],
            Hastings_and_Prince_Edward_Counties_Health_Unit =  i['Hastings_Prince_Edward'],
            Huron_Perth_District_Health_Unit =  i['Huron_Perth'],
            Kingston_Frontenac_and_Lennox_and_Addington_Public_Health =  i['KFLA'],
            Lambton_Public_Health =  i['Lambton_County'],
            Leeds_Grenville_and_Lanark_District_Health_Unit =  i['Leeds_Grenville_Lanark'],
            Middlesex_London_Health_Unit =  i['Middlesex_London'],
            Niagara_Region_Public_Health_Department =  i['Niagara_Region'],
            North_Bay_Parry_Sound_District_Health_Unit =  i['North_Bay_Parry_Sound_District'],
            Northwestern_Health_Unit =  i['Northwestern'],
            Ottawa_Public_Health =  i['City_of_Ottawa'],
            Peel_Public_Health =  i['Peel_Region'],
            Peterborough_Public_Health =  i['Peterborough_County_City'],
            Porcupine_Health_Unit =  i['Porcupine'],
            Region_of_WaterlooPublic_Health =  i['Waterloo_Region'],
            Renfrew_County_and_District_Health_Unit =  i['Renfrew_County_and_District'],
            Simcoe_Muskoka_District_Health_Unit =  i['Simcoe_Muskoka_District'],
            Southwestern_Public_Health =  i['Southwestern'],
            Sudbury_and_District_Health_Unit =  i['Sudbury_and_District'],
            Thunder_Bay_District_Health_Unit =  i['Thunder_Bay_District'],
            Timiskaming_Health_Unit =  i['Timiskaming'],
            Toronto_Public_Health =  i['Toronto'],
            Wellington_Dufferin_Guelph_Public_Health =  i['Wellington_Dufferin_Guelph'],
            Windsor_Essex_County_Health_Unit =  i['Windsor_Essex_County'],
            York_Region_Public_Health_Services =  i['York_Region'],
        )
        print(i['Date'])


def run():
    print('Starting Provincial Report Update:')
    update_report()
    print('\nStarting Regional Report Update:')
    update_regional_report()