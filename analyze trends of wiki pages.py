import requests


# Set username and password for bot
USERNAME = 'INSERT BOT USERNAME'
PASSWORD = 'INSERT BOT PASSWORD'

# Establish a header
headers = {
    "INSERT HEADER"
}

# First step: retrive a token
S = requests.Session()

URL = "https://www.mediawiki.org/w/api.php"

PARAMS = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS, headers=headers)
DATA = R.json()
if "query" not in DATA or "tokens" not in DATA['query']:
    raise Exception(f"Failed to fetch login token: {DATA}")
LOGIN_TOKEN = DATA["query"]["tokens"]["logintoken"]

# Second step: Login
PARAMS_0 = {
    "action": "clientlogin",
    "username": USERNAME,  # Use bot password username 
    "password": PASSWORD,  # Use bot password
    "logintoken": LOGIN_TOKEN,
    "loginreturnurl": "https://en.wikipedia.org",
    "format": "json"
}
R = S.post(url=URL, data=PARAMS_0, headers=headers)
print(f"HTTP Status: {R.status_code}")
print(f"Response: {R.text}")
DATA = R.json()

if "clientlogin" not in DATA:
    raise Exception(f"Clientlogin key missing in response: {DATA}")
if DATA["clientlogin"]["status"] != "PASS":
    raise Exception(f"Login failed: {DATA['clientlogin']['message']}")
print("Login successful.")

# Step 3: Fetch the trends

PARAMS_1 = {
    "action": "query",
    "titles": "MediaWiki",
    "prop": "pageviews",
    "pvipdays": 60,
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_1, headers=headers)
DATA = R.json()

# Process the responsee
try:
    pages = DATA.get("query", {}).get("pages", {})
    # The get() will recieve the key query and pages while returning both values of both keys. If query or pages doesn't exist, it would return an empty {}

    # Check if pages dictionary is not empty
    # If pages return a value: None, False, 0, empty list, empty dict (in this case empty dict), or empty string; python would treat the if statement as false, skipping to the else statement.
    # If pages return a value other than one of the above values, python would return as true and if statement code would be executed.
    if pages:
     
        # Get the first page (MediaWiki API returns one page per title)
        # The iter() function creates an iterator from an iterable object like a list, tuple, or dictionary. An iterator allows you to go through the items one at a time. The next() function retrieves the next item from the iterator. Each call to next() moves forward in the sequence until all items are exhausted.
        page = next(iter(pages.values())) # Get the first (and only) page

        # Extract the title
        page_title = page.get("title", "Unknown Title") # If title doesn't exist it would then return an unknown title string.

        # Extract pageviews and calculate total
        pageviews = page.get("pageviews", {})
        total_views = sum(view_count for view_count in pageviews.values() if view_count is not None)

        # Prepare the result
        result = {
            "title": page_title,
            "total_pageviews": total_views
        }

        # Output the result
        print(result)
    else:
        print({"error": "No page found for the given title"})
except Exception as e:
    print({"error": f"An error occurred: {str(e)}"})


#Quick note: JSON response is a dictionary















