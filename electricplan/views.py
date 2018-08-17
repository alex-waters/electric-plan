from django.shortcuts import render
from .models import CarbonData

def page_list(request):
    pages = CarbonData.objects.filter()
    fcast_display = CarbonData.fcast_display
    return render(request, 'electricplan/page_list.html', {'pages': pages, 'fcast': fcast_display})