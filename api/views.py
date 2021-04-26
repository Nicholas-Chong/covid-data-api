from django.shortcuts import render
from django.http import HttpResponse
from .models import Report, TimeseriesCases, TimeseriesVaccination
from django.db.models import Prefetch
from django.forms.models import model_to_dict
from pprint import pprint
import json


def index(request):
    # Retrieve all rows of timeseries_cases and timeseries_vaccination
    report = Report.objects.prefetch_related(
        Prefetch('timeseries_cases', to_attr='ts_cases'),
        Prefetch('timeseries_vaccination', to_attr='ts_vacci'),
        Prefetch('variants', to_attr='ts_variants'),
    )

    res = {}
    res['data'] = []
    res['ts_cases_start'] = -1
    res['ts_vacci_start'] = -1
    res['ts_variant_start'] = -1

    for count, i in enumerate(report):
        to_append = model_to_dict(i, exclude=['date'])
        if i.ts_cases:
            ts_cases_report = model_to_dict(i.ts_cases[0], exclude=['report'])
            to_append['ts_cases'] = ts_cases_report

            if res['ts_cases_start'] == -1:
                res['ts_cases_start'] = count
        
        if i.ts_vacci:
            ts_vacci_report = model_to_dict(i.ts_vacci[0], exclude=['report'])
            to_append['ts_vacci'] = ts_vacci_report

            if res['ts_vacci_start'] == -1:
                res['ts_vacci_start'] = count
        
        if i.ts_variants[0].b117 != 0:
            ts_variant_report = model_to_dict(i.ts_variants[0], exclude=['report'])
            to_append['ts_variant'] = ts_variant_report

            if res['ts_variant_start'] == -1:
                res['ts_variant_start'] = count
        
        res['data'].append(to_append)

    response = HttpResponse(json.dumps(res), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response