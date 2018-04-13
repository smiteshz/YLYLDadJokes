import requests as req

print( "       _       _           _____                           _               ___   ___   ___   ___  ")
print( "      | |     | |         / ____|                         | |             |__ \ / _ \ / _ \ / _ \ ")
print( "      | | ___ | | _____  | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __     ) | | | | | | | | | |")
print( "  _   | |/ _ \| |/ / _ \ | | |_ |/ _ \ '_ \ / _ \ '__/ _\`| __/ _ \| '__|   / /| | | | | | | | | |")
print( " | |__| | (_) |   <  __/ | |__| |  __/ | | |  __/ | | (_| | || (_) | |     / /_| |_| | |_| | |_| |")
print( "  \____/ \___/|_|\_\___|  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|    |____|\___/ \___/ \___/ ")
print( "                                                                                                  ")


url = "https://icanhazdadjoke.com/"
choice =  True
search_q = ""
ch = ""
while choice: 
	search_q = input("What do you want to seach for?(Press Enter for any random joke) ")
	res = req.get(
			url,
			headers ={"Accept" : "application/json"}
		).json()
	print(res["joke"])
	ch = input("One more ? (Press Enter for a joke or Type q to quit) ")
	if ch == "q" or ch == "Q":
		break
	elif ch == "":
		continue
	else:
		continue

