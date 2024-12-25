# dictionary with object types and their corresponding schema versions
object_types = {
    # Väg - Trafikinformation
    'Camera': 1,
    'FerryAnnouncement': 1.2, 
    'FerryRoute': 1.2,
    'FrostDepthMeasurepoint': 1,
    'FrostDepthObservation': 1,
    'Icon': 1.1,
    'Parking': 1.4,
    'RoadCondition': 1.2,
    'Situation': 1.5, 
    'TrafficFlow': 1.5, 
    'TravelTimeRoute': 1.6,
    'WeatherMeasurepoint': 2.1,
    'WeatherObservation': 2.1,   
    # Järnväg - Trafikinformation
    'RailCrossing': 1.5, 
    'ReasonCode': 1, 
    'TrainAnnouncement': 1.9,
    'TrainMessage': 1.7,
    'TrainPosition': 1.1,
    'TrainStation': 1.5,
    'TrainStationMessage': 1}

def xml_query(API_key, filter, object_type, limit = None):
  
    if limit != None:
        query = f'''<QUERY objecttype="{object_type}" schemaversion="{object_types[object_type]}" limit="{limit}">'''

    else:
      query = f'''<QUERY objecttype="{object_type}" schemaversion="{object_types[object_type]}">'''

    if object_type in ['TrafficFlow', 'TrainMessage']: # object types that can filter on CountyNo
        filter += f'''<EQ name = "CountyNo" value = "1"/>''' # CountyNo for Stockholm
    if object_type == 'Situation':
        filter += f'''<EQ name = "Deviation.CountyNo" value = "1"/>'''
    
    xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
      <REQUEST>
        <LOGIN authenticationkey="{API_key}"/>
        {query}
          <FILTER>{filter}</FILTER>
        </QUERY>
      </REQUEST>'''
    
    return xml_data