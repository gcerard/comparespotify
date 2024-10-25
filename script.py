import requests
import base64

# Spotify API credentials
client_id = 'e5bec664feb84e5fb112177d640153d5'
client_secret = 'f624adcffc83404186ab6994df13e6f1'

# Authenticate and get an access token
def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("ascii")
    headers = {
        "Authorization": f"Basic {auth_header}",
    }
    data = {
        "grant_type": "client_credentials",
    }
    response = requests.post(auth_url, headers=headers, data=data)
    return response.json().get("access_token")

# Get followers list
def get_followers(access_token, user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}/followers"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return [follower["id"] for follower in response.json().get("items", [])]

# Get following list
def get_following(access_token):
    url = "https://api.spotify.com/v1/me/following?type=user"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return [following["id"] for following in response.json().get("items", [])]

# Compare the lists
def compare_followers_and_following(followers, following):
    not_followed_back = set(following) - set(followers)
    not_following_back = set(followers) - set(following)
    print("People you follow but who don't follow you back:", not_followed_back)
    print("People who follow you but you don't follow back:", not_following_back)

# Run the script
access_token = get_access_token(client_id, client_secret)
user_id = 'bu73cgutsyftzrzi8882nrgt3'  # Replace with your Spotify user ID
followers = get_followers(access_token, user_id)
following = get_following(access_token)
compare_followers_and_following(followers, following)
