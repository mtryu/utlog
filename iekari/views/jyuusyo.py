import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from iekari.models import Todoufuken, Shikucyouson, Station, RentRoom
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime
def todoufuken(request):
    todoufukens = Todoufuken.objects.all()
    return render(request, 'iekari/todoufuken.html', {'todoufukens': todoufukens})

def shikucyouson(request,prefid):
    shikucyousons = Shikucyouson.objects.filter(prefid=prefid)
    return render(request, 'iekari/shikucyouson.html', {'shikucyousons': shikucyousons})

def station(request,cityid):
    stations = Station.objects.filter(cityid=cityid)
    return render(request, 'iekari/station.html', {'stations': stations})


def search_result(request,stationid): 
    results = RentRoom.objects.filter(nearest_station_id=stationid)
    nowyear = datetime.now().year
    return render(request, 'iekari/search_result.html', {'results':results,'nowyear':nowyear})

