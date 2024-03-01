# Import required libraries
import requests
import json

# Replace 'YOUR_APP_ID' with your actual Open Exchange Rates API app ID
app_id = "327ec886643c9b239a5054d0d73218da"

# URL to fetch currency conversion rates
url = f"http://api.exchangeratesapi.io/v1/latest?access_key=327ec886643c9b239a5054d0d73218da"

try:
    # Send an HTTP GET request to the specified URL
    response = requests.get(url)
    
    # Check for HTTP errors and raise an exception if encountered
    response.raise_for_status()

    # Parse the JSON response from the API
    rates_data = response.json()

    # Save the fetched currency rates as JSON data in a file
    with open("currency_rates.json", "w") as json_file:
        json.dump(rates_data, json_file)
    
    # Print a success message
    print("Currency rates successfully fetched and saved.")

except requests.exceptions.RequestException as e:
    # Handle exceptions related to HTTP requests, such as network errors
    print(f"Failed to fetch currency rates: {e}")

except json.JSONDecodeError as e:
    # Handle exceptions related to JSON parsing errors
    print(f"Failed to parse JSON response: {e}")

except Exception as e:
    # Handle unexpected exceptions
    print(f"An unexpected error occurred: {e}")
