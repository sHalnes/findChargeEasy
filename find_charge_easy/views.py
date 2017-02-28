from django.shortcuts import render
from .find_stations import *

def index(request):
    return render(request, 'findchargeeasy/index.html', {})


def map(request):
    # тут какая-то фигня с формой.
    #form = PositionForm(request.POST or None)
    #print(form.is_valid())
    #if request.method == 'POST' and form.is_valid():
     #   pos = form.cleaned_data['radius']
      #  print('radius: ',pos)

    if request.method == 'POST':
        user_position = request.POST.get('location')
        radius = request.POST.get('radius')
        #print('radius: ', radius)
        # convert radius value to int or set the default value
        default_radius = 1
        # well radius won't be like '' anyway, but just in case
        if radius != '':
            try:
                radius = int(radius)
                if radius > 0 and radius < 50:
                    default_radius = radius
            except:
                pass

        coords_list = user_position.split(',')
        lat = float(coords_list[0])
        lon = float(coords_list[1])
        lat_lon_zip = find_stations(lat, lon, default_radius)
        if lat_lon_zip:
            return render(request, 'findchargeeasy/map.html', {'lat_lon_zip': lat_lon_zip,
                                                               'lat': lat, 'lon': lon})

    else:
        print('request method not GET POST')
    return render(request, 'findchargeeasy/map.html', {})


def about(request):
    return render(request, 'findchargeeasy/about.html', {})

def contact(request):
    return render(request, 'findchargeeasy/contact.html', {})