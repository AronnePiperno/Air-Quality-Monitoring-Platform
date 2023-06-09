from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="MyApp")

city = input("Enter the city name: ")

location = geolocator.geocode(city)

print("The latitude of the location is: ", location.latitude)
print("The longitude of the location is: ", location.longitude)
