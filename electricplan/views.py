from django.shortcuts import render
from .models import CarbonData
from carbondata.api_call import GridData



def page_list(request):
    pages = CarbonData.objects.filter()
    data_refresh = GridData(intervals=30)
    now = data_refresh.now()
    fcast_display = data_refresh.future()

    return render(
        request,
        'electricplan/page_list.html',
        {
            'pages': pages,
            'time': now[0],
            'intensity': now[1],
            'fuel': now[2],
            'fuel_pc': now[3],
            'fcast': fcast_display
        }
    )
