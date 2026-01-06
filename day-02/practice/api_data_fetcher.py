# Import requests 
import requests

# Import json module to work with JSON data (read/write)
import json

# Public API URL 
API_URL = "https://jsonplaceholder.typicode.com/users"

# Output file name where processed data will be saved
OUTPUT_FILE = "output.json"


def fetch_api_data():
    """
    Fetch data from the public API
    Returns parsed JSON data (Python list of dictionaries)
    """
    # Send GET request to API
    response = requests.get(API_URL)

    # Raise an exception if API call fails (status code != 200)
    response.raise_for_status()

    # Convert JSON response into Python object
    return response.json()


def process_data(users):
    """
    Extract meaningful fields from API response
    Input: full user data
    Output: cleaned and structured user data
    """
    # List to store processed user data
    processed_users = []

    # Loop through each user in API response
    for user in users:
        # Extract required fields and store in dictionary
        processed_users.append({
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "city": user["address"]["city"],
            "company": user["company"]["name"]
        })

    # Return cleaned data
    return processed_users


def save_to_json(data):
    """
    Save processed data into a JSON file
    """
    # Open file in write mode
    with open(OUTPUT_FILE, "w") as file:
        # Write data into file in JSON format with indentation
        json.dump(data, file, indent=4)


def main():
    """
    Main function to control the program flow
    """
    print(" Fetching data from API...")
    
    # Fetch raw API data
    users = fetch_api_data()

    print(" Processing data...")
    
    # Process and clean the API data
    processed_data = process_data(users)

    print("\n Processed User Data:\n")
    
    # Print processed data to terminal
    for user in processed_data:
        print(
            f"ID: {user['id']} | "
            f"Name: {user['name']} | "
            f"Email: {user['email']} | "
            f"City: {user['city']} | "
            f"Company: {user['company']}"
        )

    # Save processed data to JSON file
    save_to_json(processed_data)

    print(f"\n Data successfully saved to '{OUTPUT_FILE}'")


# Run main() only if this script is executed directly
if __name__ == "__main__":
    main()
print("################################")
