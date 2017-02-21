import json
import requests

def find_stations(latitude, longitude, distance):
    '''
    Find and save data about charging station in given radius using NOBIL API
    :param latitude:
    :param longitude:
    :param distance:
    :return:
    '''
    charge_id = []
    address = []
    description = [] # new variable for description of the ch station
    location = []

    url = 'http://nobil.no/api/server/search.php'
    request = {'apikey': '9d74b4c676ecf89e8bc48da4a5628425',
               'apiversion': '3',
               'action': 'search',
               'type': 'near',
               'lat': latitude,
               'long': longitude,
               'distance': str(distance*1000),
               'limit': '20'
               }

    response = requests.post(url, data=request)

    #response = requests.get(url, data=request)# here if needs we can change get by post (find out what's difference)
    if response.status_code == 200:
        # message that there is no charging stations takes less than 30 characters
        if len(response.text) > 30:
            try:
                data = json.loads(response.text)
                for i in range(len(data['chargerstations'])):
                    charge_id.append(data['chargerstations'][i]['csmd']['id'])
                    address_temp = [data['chargerstations'][i]['csmd']['Street'],
                                    data['chargerstations'][i]['csmd']['House_number'],
                                    #data['chargerstations'][i]['csmd']['Description_of_location'] # was delited temporarly
                                    ]
                    address.append(', '.join(address_temp)) # just to check i will change ', ' with '\'
                    description.append(data['chargerstations'][i]['csmd']['Description_of_location'])
                   # "Number_charging_points", "Available_charging_points",
                    location.append(data['chargerstations'][i]['csmd']['Position'])
            except(ValueError, KeyError, TypeError):
                print(ValueError, KeyError, TypeError)
                pass
            if charge_id and location:
                # here we have to call another script which will delete all points in db in certain rectangle. We'll do it to
                # renew information.
                latitude_list = []
                longitude_list = []
                for index in range(len(charge_id)):
                    lat, lon = location[index].strip('()').split(',')
                    latitude_list.append(lat)
                    longitude_list.append(lon)
                    #charge_point = ChargePoints(charge_id=charge_id[index], address=address[index],
                    #                            location=GEOSGeometry("POINT(%s %s)" % (lon, lat)), description='description',
                    #                            payment='no')
                    #charge_point.save()
                #lat_lon = zip(latitude_list, longitude_list)
                # let's zip lattitude, longitude and address
                lat_lon = zip(latitude_list, longitude_list, address, description)
                return lat_lon
                #return lat_lon, address
            print('smthing went wrong')
#    return lat_lon, address
