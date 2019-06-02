from django.shortcuts import render
from .models import CarbonData


def page_list(request):
    cd = CarbonData()
    cd.update_chart()
    return render(request, 'electricplan/carbonchart.html')
