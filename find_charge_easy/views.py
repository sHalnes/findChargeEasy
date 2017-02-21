from django.shortcuts import render, redirect, render_to_response
from .find_stations import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.template import RequestContext
from django.http import JsonResponse
#from .forms import PositionForm

def index(request):
    print('in index')
# later we can change this part
    return render(request, 'findchargeeasy/index.html', {})


def map(request):
    print('in map')
    #form = PositionForm(request.POST or None)
    #print(form.is_valid())
    #if request.method == 'POST' and form.is_valid():
     #   pos = form.cleaned_data['radius']
      #  print('radius: ',pos)

    if request.method == 'POST':
        user_position = request.POST.get('location')
        radius = request.POST.get('radius')
        # convert radius value to int or set the default value
        default_radius = 1
        if radius != '':
            try:
                radius = int(radius)
                if radius > 0 and radius < 50:
                    default_radius = radius
            except:
                print('NAN')

        coords_list = user_position.split(',')
        lat = float(coords_list[0])
        lon = float(coords_list[1])
        #print('lat: ', lat, ' lon: ', lon)
#        lat_lon_zip, address = find_stations(lat, lon, default_radius)
        lat_lon_zip = find_stations(lat, lon, default_radius)
        if lat_lon_zip:
            # map(lat_lon_zip, address, lat, lon)
            #print('in map again')
            # t = loader.get_template('findchargeeasy/map.html')
            # c = {'lat_lon_zip': lat_lon_zip, 'address': address, 'latitude': lat, 'longitude': lon}
            # return HttpResponse({'lat':lat,'lon':lon})

            # json = simplejson.dumps(str(lat) + ',' + str(lon))
            # return HttpResponse(json, mimetype='application/json')

            # return JsonResponse({'lat': 'lat', 'lon':'lon'})
            # return HttpResponse(lat)

            return render(request, 'findchargeeasy/map.html', {'lat_lon_zip': lat_lon_zip,
                                                               'lat': lat, 'lon': lon})#

        #print(pos)

                #, context_instance=RequestContent(request))
    else:
        print('request method not GET POST')
    #return HttpResponseRedirect('map')
    return render(request, 'findchargeeasy/map.html', {})


