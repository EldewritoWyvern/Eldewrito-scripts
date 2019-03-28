# Basic server queue script
# Python 3.7

import requests, json, winsound, time

# Grab the initial json output from the master server
print('Contacting master server...')
try:
    master = requests.get("http://eldewrito.red-m.net/list", timeout = 0.5).text
except:
    print('\n\nFailed to contact master server! Try again later.')
    print('If script keeps failing try changing the timeout value or the master server could be down.')
    input('Press the enter key to exit.')
    exit()

master = json.loads(master) # Turn the json output into a dictionary
masterServers = master['result']['servers'] # Creates list of all the online servers
serverDict = {}
fullServers = []

print('Reaching out to servers...')
for eachServer in masterServers: # For each online server...
    try: # Try to reach out to it and get its initial json output
        server = requests.get('http://' + eachServer, timeout = 0.5).text # I don't think you need the http://. The timeout can be lowered if you don't want to find high ping servers.
        server = json.loads(server)
        serverDict[eachServer] = server # Add each online servers initial json response to a list
    except:
        pass # If a server doesn't respond in time skip it.

fullServers = serverDict.copy() # To iterate a dictionary and remove values at the same time I had to make a copy to edit instead.

print('Finding full servers...')
for key in serverDict: # Check if a server is full. If it is not then remove it from the fullServers list.
    if serverDict[key]['maxPlayers'] != serverDict[key]['numPlayers']:
        fullServers.pop(key)

ServerKeys = list(fullServers.keys())

# Ask the user what server to join.
# The output will look like the below:
# Which full server do you want to join: 
# 1. [FWKZT] MINI-GAMES on Splatter Snek - 12/12
# You will enter 1 to queue up for that server.

if fullServers:
    print('\nWhich full server do you want to join? ')
    count = 0
    for eachFullServer in fullServers: # Displays the server name, and map in a nice numbered bulleted list. Enter the corresponding number to select that server.
        count += 1
        print(str(count) + '. ' + fullServers[eachFullServer]['name'] + ' on ' + fullServers[eachFullServer]['map'] + ' - ' + str(fullServers[eachFullServer]['numPlayers']) + '/' + str(fullServers[eachFullServer]['maxPlayers']))
    chosenServer = int(input("Please enter the server's corresponding number on the left that you would like to join: ")) # I'm new to python so I wasn't sure of a good way to do this, just what I came up with :)
else: # If there are none then end the script.
    print('\nNo full servers found!\n')
    input('Press the enter key to exit.')
    exit()


# Tell the user what they've selected.
print("\nYou've chosen to join " + fullServers[(ServerKeys[chosenServer-1])]['name'] + ' on ' + fullServers[(ServerKeys[chosenServer-1])]['map'])
print('We will query this server until it is ready to join.\n')
print('Please wait...')

# Check if the server is joinable before starting the queue
queryServer = requests.get('http://' + ServerKeys[chosenServer-1]).text
queryServer = json.loads(queryServer)
if queryServer['maxPlayers'] != queryServer['numPlayers']:
    print('\nJOIN SERVER NOW')
    winsound.PlaySound("*", winsound.SND_ALIAS)
    print('\nJOIN SERVER NOW')
    winsound.PlaySound("*", winsound.SND_ALIAS)
    input('Press the enter key to exit.')
    exit()
else:
    # While the server is full, every 5 seconds grab its json output and see if its not full.
    while queryServer['maxPlayers'] == queryServer['numPlayers']: 
        time.sleep(5)
        print('Refreshing...')
        queryServer = requests.get('http://' + ServerKeys[chosenServer-1]).text
        queryServer = json.loads(queryServer)
    
    # Play some annoying sounds to get your attention so you know when to join.
    print('\nJOIN SERVER NOW')
    winsound.PlaySound("*", winsound.SND_ALIAS)
    print('\nJOIN SERVER NOW')
    winsound.PlaySound("*", winsound.SND_ALIAS)
    print('\nJOIN SERVER NOW')
    winsound.PlaySound("*", winsound.SND_ALIAS)

    # IDEALLY instead of the sounds the script hooks to the games console websocket using the RCON password in dewrito_prefs.cfg that way it joins for you.
    # I will save that for another day.
    