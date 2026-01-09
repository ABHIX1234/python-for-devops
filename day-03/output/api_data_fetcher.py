"""
Stock Market Data Fetcher - Enhanced Version (Day 03)

This script fetches daily stock market data from Alpha Vantage API
and saves it to a JSON file with proper error handling and validation.

Features:
- Interactive user input with validation
- Comprehensive error handling
- Automatic directory creation
- Timestamped output files
- Metadata tracking

Author: DevOps Learning Path
Date: Day 03 - Error Handling & Code Structure
"""

import requests  # HTTP library for API calls
import json      # JSON parsing and creation
import os        # Operating system interactions (file/directory operations)
import sys       # System-specific parameters and functions
from datetime import datetime  # Date and time handling


def validate_api_key(api_key):

    # Check if API key is missing or still set to placeholder value
    if not api_key or api_key == "YOUR_API_KEY":
        return False
    return True

def validate_stock_symbol(symbol):
    # Check if symbol exists and is a string
    if not symbol or not isinstance(symbol, str):
        return False
    
    # Basic validation: 1-5 uppercase letters only
    # Examples of valid symbols: IBM, AAPL, MSFT, GOOGL
    if not (1 <= len(symbol) <= 5 and symbol.isalpha() and symbol.isupper()):
        return False
    
    return True


def fetch_stock_data(api_url, api_key, symbol):
    try:
        # Build the query string with API parameters
        # function: Type of data to fetch (TIME_SERIES_DAILY)
        # symbol: Which stock to look up
        # apikey: Authentication credential
        query = (
            f"function=TIME_SERIES_DAILY"
            f"&symbol={symbol}"
            f"&apikey={api_key}"
        )

        print(f" Requesting data for {symbol}...")
        
        # Send GET request with 10-second timeout to prevent hanging
        response = requests.get(api_url + query, timeout=10)
        
        # Raise exception if HTTP status code indicates error (4xx or 5xx)
        response.raise_for_status()

        # Parse JSON response into Python dictionary
        data = response.json()

        # Check for API-specific error messages
        # Alpha Vantage returns different keys for different error types
        if "Error Message" in data:
            print(f" API Error: Invalid stock symbol '{symbol}'")
            return None
        
        # Check if we've hit the API rate limit
        # Free tier allows 25 requests per day
        if "Note" in data:
            print(f"  API Rate Limit: {data['Note']}")
            return None

        # Verify the response has the expected data structure
        # "Time Series (Daily)" contains the actual stock price data
        if "Time Series (Daily)" not in data:
            print(" Unexpected API response format")
            return None

        print(f" Successfully fetched data for {symbol}")
        return data

    # Handle specific exception types for better error messages
    except requests.exceptions.Timeout:
        # Request took longer than specified timeout
        print(" Error: Request timed out after 10 seconds")
    except requests.exceptions.ConnectionError:
        # No internet connection or server unreachable
        print(" Error: Unable to connect to API (check internet connection)")
    except requests.exceptions.HTTPError as error:
        # Server returned error status code (4xx or 5xx)
        print(f" HTTP Error: {error}")
    except requests.exceptions.RequestException as error:
        # Catch-all for other requests-related errors
        print(f" Network error: {error}")
    except json.JSONDecodeError:
        # Response body is not valid JSON
        print(" Error: Invalid JSON response from API")
    except Exception as error:
        # Catch any other unexpected errors
        print(f" Unexpected error: {error}")

    # Return None if any error occurred
    return None


def save_data_to_file(data, filename, symbol):

    try:
        # Create a structured output with metadata
        # This helps track when data was fetched and what version of script was used
        output_data = {
            "metadata": {
                "symbol": symbol,
                "fetched_at": datetime.now().isoformat(),  # ISO format timestamp
                "script_version": "1.1"
            },
            "stock_data": data  # The actual API response
        }
        
        # Extract directory path from filename (if any)
        directory = os.path.dirname(filename)
        
        # Create directory structure if it doesn't exist
        # This prevents "directory not found" errors
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f" Created directory: {directory}")

        # Open file in write mode with UTF-8 encoding
        # UTF-8 ensures proper handling of special characters
        with open(filename, "w", encoding="utf-8") as file:
            # Write data as formatted JSON
            # indent=4 makes the file human-readable
            json.dump(output_data, file, indent=4)

        # Get file size and display to user
        # Provides feedback on how much data was saved
        file_size = os.path.getsize(filename)
        print(f" Data saved successfully to '{filename}' ({file_size:,} bytes)")
        return True

    # Handle file-related errors gracefully
    except FileNotFoundError:
        # Parent directory doesn't exist or invalid path
        print(f" Error: Invalid file path '{filename}'")
    except PermissionError:
        # No write permission for the target location
        print(f" Error: Permission denied writing to '{filename}'")
    except OSError as error:
        # Other OS-level errors (disk full, etc.)
        print(f" OS Error: {error}")
    except Exception as error:
        # Catch-all for unexpected file errors
        print(f" File error: {error}")
    
    return False


def get_user_input(prompt, default=None, validator=None):

    # Loop until valid input is received
    while True:
        try:
            # Display prompt with default value if provided
            if default:
                user_input = input(f"{prompt} [{default}]: ").strip()
                # Use default if user just presses Enter
                if not user_input:
                    user_input = default
            else:
                user_input = input(f"{prompt}: ").strip()
            
            # Reject empty input
            if not user_input:
                print(" Input cannot be empty. Please try again.")
                continue
            
            # Run validator function if provided
            # Validator should return True for valid input
            if validator and not validator(user_input):
                print(" Invalid input format. Please try again.")
                continue
            
            # Input is valid, return it
            return user_input
            
        except KeyboardInterrupt:
            # User pressed Ctrl+C - exit gracefully
            print("\n\n  Operation cancelled by user")
            sys.exit(0)
        except EOFError:
            # Unexpected end of input stream
            print("\n Unexpected end of input")
            sys.exit(1)


def main():
    """
    Main function that coordinates the program flow.
    
    This is the entry point of the script. It orchestrates:
    1. User input collection
    2. Input validation
    3. API data fetching
    4. Data saving to file
    5. Success/failure reporting
    """
    # Display welcome banner
    print("=" * 60)
    print(" Stock Market Data Fetcher - Enhanced Version")
    print("=" * 60)
    print()

    # Configuration - API endpoint URL
    api_url = "https://www.alphavantage.co/query?"
    
    # Get API key from user with validation
    # 'demo' is Alpha Vantage's public demo key for testing
    api_key = get_user_input(
        "Enter your Alpha Vantage API key",
        default="demo"  # Allow testing without real API key
    )
    
    # Warn user if API key looks invalid (but allow 'demo')
    if not validate_api_key(api_key) and api_key != "demo":
        print("  Warning: API key looks invalid (using anyway)")
    
    # Get stock symbol from user with format validation
    stock_symbol = get_user_input(
        "Enter stock symbol (e.g., IBM, AAPL, MSFT)",
        default="IBM",
        validator=validate_stock_symbol  # Ensures proper format
    )
    
    # Generate unique filename with timestamp
    # Format: stock_data_IBM_20240103_143022.json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stock_data_{stock_symbol}_{timestamp}.json"
    
    # Visual separator for cleaner output
    print()
    print("-" * 60)

    # Step 1: Fetch data from API
    stock_data = fetch_stock_data(api_url, api_key, stock_symbol)

    # Step 2: Save data if fetch was successful
    if stock_data:
        print()
        success = save_data_to_file(stock_data, filename, stock_symbol)
        
        if success:
            # Display success message
            print()
            print("=" * 60)
            print(" Operation completed successfully!")
            print(f" Stock data for {stock_symbol} saved to {filename}")
            print("=" * 60)
        else:
            # Data fetched but couldn't save - non-zero exit code
            print("\n  Data fetched but could not be saved")
            sys.exit(1)  # Exit with error code 1
    else:
        # Data fetch failed - display helpful troubleshooting tips
        print()
        print("=" * 60)
        print(" Operation failed - no data to save")
        print("=" * 60)
        print("\n Troubleshooting tips:")
        print("   • Check your API key is valid")
        print("   • Verify the stock symbol is correct")
        print("   • Ensure you haven't exceeded API rate limits")
        print("   • Check your internet connection")
        sys.exit(1)  # Exit with error code 1


# Script entry point
# This block only runs when the script is executed directly
# (not when imported as a module)
if __name__ == "__main__":
    main()