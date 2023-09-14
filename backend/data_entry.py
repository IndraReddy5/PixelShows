import requests as req

admin_user = {"username": "admin", "password": "pixel123"}

new_users = [
    {"username": "chris", "email": "chris@pixelshows.in", "password": "pixel123"},
    {"username": "rogers", "email": "rogers@pixelshows.in", "password": "pixel123"},
    {"username": "monk", "email": "monk@pixelshows.in", "password": "pixel123"},
]

new_venue_types = [
    {"type": "Multiplex", "venue_charges": 70},
    {"type": "Imax", "venue_charges": 100},
    {"type": "PVR", "venue_charges": 150},
    {"type": "Show_Theatre", "venue_charges": 50},
]

new_tags = [
    {"tag_name": "RomCom"},
    {"tag_name": "Action"},
    {"tag_name": "Thriller"},
    {"tag_name": "Drama"},
    {"tag_name": "Documentary"},
    {"tag_name": "Comedy"},
]

new_venues = [
    {
        "venue_name": "V Mega Anand Cine Complex",
        "seating_capacity": 100,
        "venue_image": "V_Mega_Anand_Cine_Complex_1.jpg",
        "venue_address": "National Highway 18,  Kurnool,  Andhra Pradesh 518004,  India",
        "venue_city": "kurnool",
        "venue_type": 1,
    },
    {
        "venue_name": "The Habitat",
        "seating_capacity": 50,
        "venue_image": "The_Habitat_1.jpg",
        "venue_address": "1st Floor, Hotel Unicontinental, 3rd Road, Station, next to Khar, Khar West, Mumbai, Maharashtra 400052",
        "venue_city": "Mumbai",
        "venue_type": 4,
    },
    {
        "venue_name": "Prasads Multiplex",
        "seating_capacity": 150,
        "venue_image": "Prasads_Multiplex_1.jpg",
        "venue_address": "IMAX Road, NTR Marg, behind of, Khairtabad, Hyderabad, Telangana 500063",
        "venue_city": "Hyderabad",
        "venue_type": 2,
    },
    {
        "venue_name": "Inox_Nexus_Whitefield",
        "seating_capacity": 70,
        "venue_image": "V_Mega_Anand_Cine_Complex_1.jpg",
        "venue_address": "PVR INOX Limited., 2nd Floor, Nexus Whitefield, Whitefield Main Road, Bengaluru - 560066, Karnataka",
        "venue_city": "Banglore",
        "venue_type": 3,
    },
]

new_shows = [
    {
        "show_name": "Miss Shetty Mr Polishetty",
        "ticket_price": 120.00,
        "show_description": "Miss Shetty is a feminist living in London and wants to be single forever. Mr. Polishetty from Hyderabad in Telangana, India, wants to be in a committed relationship. The two appear to be in different stages of life but somehow connect.",
        "show_poster": "09/13/2023_16:37.jpg",
        "show_timing": "09/13/2023 16:00:00",
        "show_venues": [1],
        "show_tags": [1,6],
    },
    {
        "show_name": "Jawan",
        "ticket_price": 150.00,
        "show_description": "A high-octane action thriller which outlines the emotional journey of a man who is set to rectify the wrongs in the society.",
        "show_poster": "09/24/2023_16:37.jpg",
        "show_timing": "09/13/2023 16:00:00",
        "show_venues": [1,3,4],
        "show_tags": [2,3],
    },
    {
        "show_name": "Oppenheimer",
        "ticket_price": 100.00,
        "show_description": "The story of American scientist, J. Robert Oppenheimer, and his role in the development of the atomic bomb.",
        "show_poster": "07/10/2023_16:37.jpg",
        "show_timing": "09/13/2023 16:00:00",
        "show_venues": [3,4],
        "show_tags": [2,3,4],
    },
    {
        "show_name": "Jailer",
        "ticket_price": 150.00,
        "show_description": "A retired jailer goes on a manhunt to find his son's killers. But the road leads him to a familiar, albeit a bit darker place. Can he emerge from this complex situation successfully?",
        "show_poster": "09/28/2023_16:37.jpg",
        "show_timing": "09/13/2023 16:00:00",
        "show_venues": [1,4],
        "show_tags": [2,6],
    },
    {
        "show_name": "All Star Standup Comedy",
        "ticket_price": 500.00,
        "show_description": "Start the week with the best in Standup Comedy performing fresh material - May or may not include surprise acts. May or may not include any/all acts as shown in the poster.",
        "show_poster": "10/04/2023_16:37.jpg",
        "show_timing": "10/04/2023 22:00:00",
        "show_venues": [2],
        "show_tags": [6],
    },
]


auth_token = req.post("http://localhost:8000/api/login?include_auth_token", json = admin_user).json()['response']['user']['authentication_token']

headers = {"Content-Type":"application/json", "Auth-Token": auth_token}

for user in new_users:
    req.post("http://localhost:8000/api/createuserprofile", json = user, headers=headers)

for venue_type in new_venue_types:
    req.post("http://localhost:8000/api/venuetype", json = venue_type, headers=headers)

for tag in new_tags:
    req.post("http://localhost:8000/api/tag", json = tag, headers=headers)

for venue in new_venues:
    req.post("http://localhost:8000/api/venue", json = venue, headers=headers)

for show in new_shows:
    req.post("http://localhost:8000/api/shows", json = show, headers=headers)

print("data entry done")