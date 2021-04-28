from django.shortcuts import render
from django.http import HttpResponse
from .models import Report, RegionalReport
from django.db.models import Prefetch
from django.forms.models import model_to_dict
from pprint import pprint
import json
import time


def index(request):
    start = time.process_time()

    # Retrieve all records
    fields = [i.name for i in Report._meta.get_fields()][2:]
    ret_field_names = [
        'Date String', 'New Cases', 'New Deaths', 'New Tests', 'Positivity', 
        'Total Cases', 'Total Deaths', 'Total Resolved', 'Total Active', 
        'New Vaccinations', 'Num Fully Vaccinated', 'Num Part Vaccinated', 
        'P1 (Brazil)', 'B1351 (South Africa)', 'B117 (UK)',
    ]
    res = {}
    res['data'] = [ret_field_names] + list(Report.objects.values_list(*fields))

    regional_data_today = model_to_dict(RegionalReport.objects.latest('date'))
    del regional_data_today['date']
    del regional_data_today['date_string']
    del regional_data_today['id']

    formatted_rdt = [
        {'region': i.replace('_', ' '), 'new cases': regional_data_today[i]} 
        for i in regional_data_today
    ]
    
    res['regional_data'] = formatted_rdt
    
    end = time.process_time() - start
    print(end)

    response = HttpResponse(json.dumps(res), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    # response['Cache-Control'] = 'max-age=1800'
    response['Server-Timing'] = f'db;desc="Database";dur={end}'
    return response