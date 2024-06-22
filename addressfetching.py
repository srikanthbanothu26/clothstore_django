import requests

# Input from user
colonyname = input("Enter colony name: ")
village = input("Enter village name: ")
cityname = input("Enter city name: ")
apikey = "pk.ed10c7b21526a2babc266be91ccebef9"
state=input("Enter state name: ")

# Construct URL based on whether colonyname is provided
if colonyname:
    url = f"https://api.locationiq.com/v1/autocomplete.php?key={apikey}&q={colonyname}%20{village}%20{cityname}%20{state}&limit=5&dedupe=1"
else:
    url = f"https://api.locationiq.com/v1/autocomplete.php?key={apikey}&q={village}%20{cityname}%20{state}&limit=5&dedupe=1"

# Make the API request
response = requests.get(url)

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    try:
        resp = response.json()
        
        # Loop through each place in the response and print the required details
        for place in resp:
            display_place = place.get('display_place', 'N/A')
            address = place.get('address', {})
            city = address.get('city', 'N/A')
            postcode = address.get('postcode', 'N/A')
            district = address.get('county', 'N/A')
            state = address.get('state', 'N/A')
            country_code = address.get('country_code', 'N/A')
            county = address.get('county', 'N/A')
            full_address = place.get('display_address', 'N/A')
            
            # Print details
            print(f"Display Place: {display_place}")
            print(f"City: {city}")
            print(f"Postcode: {postcode}")
            print(f"District: {district}")
            print(f"State: {state}")
            print(f"Country Code: {country_code}")
            print(f"County: {county}")
            print(f"Full Address: {full_address}")
            print('-' * 40)
    except ValueError:
        print("Error parsing the JSON response.")
else:
    print(f"Error: Received status code {response.status_code}")
