from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="weather_app")

def get_coordinates(city_name):

    location = geolocator.geocode(city_name)

    if not location:
        return None

    return {
        "latitude": location.latitude,
        "longitude": location.longitude
    }