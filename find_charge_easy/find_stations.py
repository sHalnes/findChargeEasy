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

    if response.status_code == 200:
        # message that there is no charging stations takes less than 30 characters
        if len(response.text) > 30:
            try:
                data = json.loads(response.text)
                for i in range(len(data['chargerstations'])):
                    charge_id.append(data['chargerstations'][i]['csmd']['id'])
                    address_temp = [str(data['chargerstations'][i]['csmd']['Street']),
                                    str(data['chargerstations'][i]['csmd']['House_number']),
                                    #data['chargerstations'][i]['csmd']['Description_of_location'] # was delited temporarly
                                    ]
                    address.append(', '.join(address_temp))
                    location.append(data['chargerstations'][i]['csmd']['Position'])

                    description_temp = [str(data['chargerstations'][i]['csmd']['Description_of_location']),
                                        "Number of points: " + str(data['chargerstations'][i]['csmd']['Number_charging_points']),
                                        "Number of available: " + str(data['chargerstations'][i]['csmd']['Available_charging_points']),
                                        "Owned by: " + data['chargerstations'][i]['csmd']['Owned_by'],
                                        data['chargerstations'][i]['attr']['st']['24']['attrname'] + ': ' +
                                        data['chargerstations'][i]['attr']['st']['24']['trans'],
                                        #data['chargerstations'][i]['attr']['st']['22']['attrname'] + ': ' + # public funding
                                        #data['chargerstations'][i]['attr']['st']['22']['trans'],
                                        data['chargerstations'][i]['attr']['st']['7']['attrname'] + ': ' +
                                        data['chargerstations'][i]['attr']['st']['7']['trans'],
                                        data['chargerstations'][i]['attr']['st']['6']['attrname'] + ': ' +
                                        data['chargerstations'][i]['attr']['st']['6']['trans'],
                                        data['chargerstations'][i]['attr']['st']['3']['attrname'] + ': ' +
                                        data['chargerstations'][i]['attr']['st']['3']['trans'],
                                        data['chargerstations'][i]['attr']['st']['2']['attrname'] + ': ' +
                                        data['chargerstations'][i]['attr']['st']['2']['trans']
                                        ]
                    description.append(', '.join(description_temp))

            except(ValueError, KeyError, TypeError):
                print(ValueError, KeyError, TypeError)
                pass
            if charge_id and location:
                # make a zip to return all values
                latitude_list = []
                longitude_list = []
                for index in range(len(charge_id)):
                    lat, lon = location[index].strip('()').split(',')
                    latitude_list.append(lat)
                    longitude_list.append(lon)
                lat_lon = zip(latitude_list, longitude_list, address, description)
                return lat_lon
            print('smthing went wrong')
