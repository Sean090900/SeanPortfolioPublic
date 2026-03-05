import decimal
import json
import re

import boto3
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse

# Decoding message function
def decode(input_str):
	"""
		The 'decode()' function gets the body message from the 'event' - AKA: the 
		request message
		
		Args:
			input_str (str): Takes in 'event["Body"]'
		
		Returns:
			output_str (str): The decoded request_message
	"""
	# Get message
	output_str = re.compile('%([0-9a-fA-F]{2})',re.M).sub(lambda m: chr(int(m.group(1),16)), input_str)
	output_str = output_str.replace('+', ' ')

	# Return message
	return(output_str)

# Response function
def response(body, number, sid, token):
	"""
		The 'response()' function sends a valid Twilml message back to Twilio, so 
		it can send the message to its appropriate recipient.
		
		Args:
			body (str): The message for the recipient
			number (str): The recipient's phone number 
			sid (str): Sean's Twilio account SID
			token (str): Sean's Twilio account AUTH_TOKEN
			
		Returns:
			NONE - Sends message to Twilio
	"""
	# Show twilio login info
	client = Client(sid, token)

	# Message 
	message = client.messages.create(
		to=number[3:], 
		from_="3419997859",
		body=body)

	# Print ID to confirm
	print(message.sid)

# Organize commands list
def commands(commands_dict):
	"""
		The 'commands()' function organizes the commands list into a readable
		format for a message to be sent back to the recipient.

		Args:
			commands_dict (dict): The COMMANDS dictionary
			
		Returns:
			message (str): The reorganized commands list
	"""
	# Make lists of commands and cooresponding descriptions
	commands = list(commands_dict.keys())
	description = list(commands_dict.values())

	# Develope message 
	message = ''
	for i in range(len(commands_dict)):
		message += "'" + commands[i] + "'" + ":\n" + description[i] + "\n\n" 

	# Return message
	return message

# Give API info 
def hi():
	"""
		The 'hi()' function gives a description of the API service and instructions
		on how to use the service

		Args:
			NONE
		
		Returns:
			message (str): The reorganized commands list
	"""
	# Develope and return message
	message = "Welcome to your Beer Die Stats Collector!\n\nThis system is used to record and visualize individual beer die statistics. You can enter your own stats, visualize your progress, and see your B.D.S.M. (Beer Die Scoring Metric)!\n\nFirst, text in 'New NAME' (with 'NAME' being your first name!). This will set you up with a profile! Once you recieve a confirmation text, you can use other commands to start recording your stats!\n\nYour next step is to take a look at our list of commands. Text in the word 'Commands' to see your options. Using these commands, you can send in your stats, delete mistakes, blank your profile, ask for help, and more!\n\nWhen entering commands, be sure to follow the example perfectly! Include spaces and dashes when they appear in the Commands list. Hashtags (#) mean you have to put in a number - for example, if you are recording a TWO self plunks, follow this format for your text...\n\nAdd 2 self-plunks\n\nGood luck out there! And remember - catch die, not feelings."
	return message

# Deleting a Profile
def remove(number, table):
	"""
		The 'remove()' function deletes a player profile from the Dynamodb table.

		Args:
			number (str): The player's phone number
			table (db): The Dynamodb 'beer_die_stats' table

		Returns:
			NONE - Deletes player profile containing given number
	"""
	# Remove player from table
	response = table.delete_item(
		Key={
			'number': number,
			'id': 0,
		}
	) 
	print("DeleteItem succeeded:")
	print(json.dumps(response, indent=4, cls=DecimalEncoder))

	# Return message
	return "Done! Your profile has been erased"

# Give seeds
def seedings(table):
	"""
		The 'seedings()' function uses BDSM scores to develope seedings for tournaments and 
		returns an organized message relaying the information
		
		Args:
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			message (str): The organized seeding message
	"""
	# Get names and BDSMs
	scan = table.scan()
	names =[]
	bdsms = []
	for profile in scan["Items"]:
		info = profile["info"]
		name = info["name"]
		if info["wins"] + info["losses"] < 10:
			bdsm = '---'
		else:
			bdsm = calc_bdsm(profile, table)
		names.append(name)
		bdsms.append(bdsm)
	
	# Re-organize by BDSM score
	org_names = []
	org_bdsms = []
	for name in range(len(names)):
		biggest = 0
		index = 0
		for j in range(len(bdsms)):
			if type(bdsms[j]) == str:
				continue
			if bdsms[j] > biggest:
				biggest = bdsms[j]
				index = j
		org_names.append(names[index])
		names.remove(names[index])
		org_bdsms.append(bdsms[index])
		bdsms.remove(bdsms[index])
	if names:
		for name in range(len(names)):
			org_names.append(names[name])
			names.remove(names[name])
			org_bdsms.append(bdsms[name])
			bdsms.remove(bdsms[name])
	
	# Develope message
	message = 'SEEDINGS:\n'
	for i in range(len(org_names)):
		message += str(i + 1) + ") " + str(org_names[i]) + " - BDSM: " + str(org_bdsms[i]) + "\n"
	
	# Return message
	return message

# Getting/Displaying stats
def stats(profile, table):
	"""
		The 'stats()' function organizes a player's stats from the table and 
		organizes a message to be sent back.
		
		Args:
			profile (json object): 
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			message (str): The organized message to be sent to the player
	"""
	# Assign values to cooresponding stat
	print(profile)
	info = profile["info"]
	wins, losses, drops, plunks, self_plunks, skunks, fifas = info["wins"], info["losses"], info['drops'], info['plunks'], info['self_plunks'], info["skunks"], info['fifas']
	
	# Deveope message
	message = '' + profile["info"]["name"] + '\n'
	message += "Games Played: {}\n".format(wins + losses)
	message += "Wins: {}\n".format(wins)
	message += "Easy Drops: {}\n".format(drops)
	message += "Plunks: {}\n".format(plunks)
	message += "Self-Plunks: {}\n".format(self_plunks)
	message += "Skunks: {}\n".format(skunks)
	message += "FIFAs: {}\n".format(fifas)
	if int(wins + losses) == 0:
		message += "Win Percentage: 0%\n"
		message += "BDSM Score: ---"
	else:
		win_loss = wins / (wins + losses)
		message += "Win Percentage: {}%\n".format(int(win_loss * 100))
		message += "BDSM Score: {}".format(calc_bdsm(profile, table))

	# Return message
	return message

# Insert new item (person)
def new(number, name, table):
	"""
		The 'new()' function creates a new player profile within the Dynamodb
		table.
		
		Args:
			number (str): The player's phone number
			name (str): The name of the player
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			NONE - Creates new Dynamodb item
	"""
	# Blank existing profile
	scan = table.scan()
	table.put_item(
		Item={
			'number': number, 
			'id': 0,
			'info': {
				"losses": 0,
				"wins": 0,
				"drops": 0,
				"plunks": 0,
				"self_plunks": 0,
				"name": name,
				"skunks": 0,
				"fifas": 0,
			}
		}
	)
	message = "Done! {}'s profile has been created".format(name)
		
	# Return message
	return message

# Updating info
def update(number, word2, jsn, stat, table):
	"""
		The 'update()' function updates a player's stats within the Dynamodb
		table.
		
		Args:
			number (str): The player's phone number
			word2 (str): The assumed number to be added to existing stat count
			jsn (json object): Player profile in json format
			stat (str): The stat type to be changed
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			NONE - Updates player stats in table
	"""
	# 'is_int()' method to determine if casting will be successful
	def is_int(s):
		try:
			number = int(s)
			return True
		except ValueError: 
			return False

	# Send error message if casting does not work
	if not is_int(word2):
		return "Invalid Message! Make sure the second word is a number!"

	# Update existing stat and send message if result is positive, else return error message
	num = int(word2)
	prev = jsn["info"][stat]
	if (num + prev) >= 0:
		response = table.update_item(
			Key={
				'number': number,
				'id': 0,
			},
			UpdateExpression="set info.{}=:s".format(stat),
			ExpressionAttributeValues={
				':s': num + prev,
			},
			ReturnValues="UPDATED_NEW"
		)
		print("UpdateItem succeeded:")
		print(json.dumps(response, indent=4, cls=DecimalEncoder))

		# Add to tag if stat leader!
		tag = ''
		thisPlayer = read(number, table)
		if stat == 'plunks' or stat == 'skunks' or stat == 'drops' or stat == 'self_plunks' or stat == 'fifas':
			scan = table.scan()
			maxPlunks = 0
			maxSkunks = 0
			maxDrops = 0
			maxSelfPlunks = 0
			maxFifas = 0

			for profile in scan["Items"]:
				info = profile["info"]
				if int(info["plunks"]) > maxPlunks:
					maxPlunks = int(info['plunks'])
				if int(info["skunks"]) > maxSkunks:
					maxSkunks = int(info['skunks'])
				if int(info["drops"]) > maxDrops:
					maxDrops = int(info['drops'])
				if int(info["self_plunks"]) > maxSelfPlunks:
					maxSelfPlunks = int(info['self_plunks'])
				if int(info["fifas"]) > maxFifas:
					maxFifas = int(info['fifas'])
			
			playersWithMaxPlunks = 0
			playersWithMaxSkunks = 0
			playersWithMaxDrops = 0
			playersWithMaxSelfPlunks = 0
			playersWithMaxFifas = 0
			for profile in scan['Items']:
				info = profile['info']
				if int(info["plunks"]) == maxPlunks:
					playersWithMaxPlunks += 1
				if int(info["drops"]) == maxDrops:
					playersWithMaxDrops += 1
				if int(info["skunks"]) == maxSkunks:
					playersWithMaxSkunks += 1
				if int(info["self_plunks"]) == maxSelfPlunks:
					playersWithMaxSelfPlunks += 1
				if int(info["fifas"]) == maxFifas:
					playersWithMaxFifas += 1
			
			if int(thisPlayer['info']['plunks']) == maxPlunks and stat == 'plunks' and playersWithMaxPlunks == 1:
				tag += "\nYou are the current Plunk King! \U0001F451"
			elif int(thisPlayer['info']['plunks']) == maxPlunks and stat == 'plunks' and playersWithMaxPlunks > 1:
				tag += "\nYou are tied for Plunk King!"
			if int(thisPlayer['info']['skunks']) == maxSkunks and stat == 'skunks' and playersWithMaxSkunks == 1:
				tag += "\nYou have the most Skunks! \U0001F9A8"
			elif int(thisPlayer['info']['skunks']) == maxSkunks and stat == 'skunks' and playersWithMaxSkunks > 1:
				tag += "\nYou are tied for the most Skunks!"
			if int(thisPlayer['info']['drops']) == maxDrops and stat == 'drops' and playersWithMaxDrops == 1:
				tag += "\nYou have the most Easy Drops... loser! \U0001F4A9"
			elif int(thisPlayer['info']['drops']) == maxDrops and stat == 'drops' and playersWithMaxDrops > 1:
				tag += "\nYou are tied for the most Drops... loser!"
			if int(thisPlayer['info']['self_plunks']) == maxSelfPlunks and stat == 'self_plunks' and playersWithMaxSelfPlunks == 1:
				tag += "\nYou have the most Self-Plunks... loser! \U0001F4A9"
			elif int(thisPlayer['info']['self_plunks']) == maxSelfPlunks and stat == 'self_plunks' and playersWithMaxSelfPlunks > 1:
				tag += "\nYou are tied for the most Self Plunks... loser!"
			if int(thisPlayer['info']['fifas']) == maxFifas and stat == 'fifas' and playersWithMaxFifas == 1:
				tag += "\nYou have the most FIFAs! \U000026BD"
			elif int(thisPlayer['info']['fifas']) == maxFifas and stat == 'fifas' and playersWithMaxFifas > 1:
				tag += "\nYou are tied for the most FIFAs!"

		return "Done! Your {}: {}{}".format(stat, num + prev, tag)
	else:
		return "You already have 0 {}!".format(stat)

# Reading info
def read(number, table):
	"""
		The 'read()' function outputs a player profile within the Dynamodb
		table (in json format).
		
		Args:
			number (str): The player's phone number
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			item (json object): Specific player profile in json format
	"""
	# Check if profile exists for this number
	scan = table.scan()
	# print(scan)
	check = False
	for profile in scan["Items"]:
		if profile["number"] == number:
			check = True
	if not check:
		return False

	# Read specified player profile
	read = table.get_item(
		Key={
			'number': number,
			'id': 0,
		}
	)
	print(read)
	item = read['Item']
	print("GetItem succeeded:")
	print(json.dumps(item, indent=4, cls=DecimalEncoder))
		
	# Return profile
	return item

# Skunk info
def skunks(table):
	"""
		The 'skunks()' function lists all players' skunks
		
		Args:
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			message (str): The organized message to be sent to the player
	"""
	# Scan table
	scan = table.scan()
	
	# Get names and skunks
	names =[]
	skunks = []
	for profile in scan["Items"]:
		info = profile["info"]
		names.append(info['name'])
		skunks.append(info['skunks'])

	# Re-organize by BDSM score
	org_names = []
	org_skunks = []
	for name in range(len(names)):
		biggest = 0
		index = 0
		for j in range(len(skunks)):
			if skunks[j] > biggest:
				biggest = skunks[j]
				index = j
		org_names.append(names[index])
		names.remove(names[index])
		org_skunks.append(skunks[index])
		skunks.remove(skunks[index])
	
	# Develope message
	message = "SKUNKS:\n"
	for i in range(len(org_names)):
		message += str(i + 1) + ") " + str(org_names[i]) + " - Skunks: " + str(org_skunks[i]) + "\n"

	# Return message
	return message

# Plunk info
def plunks(table):
	"""
		The 'plunks()' function lists all players' plunks
		
		Args:
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			message (str): The organized message to be sent to the player
	"""
	# Scan table
	scan = table.scan()
	
	# Get names and plunks
	names =[]
	plunks = []
	for profile in scan["Items"]:
		info = profile["info"]
		names.append(info['name'])
		plunks.append(info['plunks'])

	# Re-organize by BDSM score
	org_names = []
	org_plunks = []
	for name in range(len(names)):
		biggest = 0
		index = 0
		for j in range(len(plunks)):
			if plunks[j] > biggest:
				biggest = plunks[j]
				index = j
		org_names.append(names[index])
		names.remove(names[index])
		org_plunks.append(plunks[index])
		plunks.remove(plunks[index])
	
	# Develope message
	message = "PLUNKS:\n"
	for i in range(len(org_names)):
		message += str(i + 1) + ") " + str(org_names[i]) + " - Plunks: " + str(org_plunks[i]) + "\n"

	# Return message
	return message

# Drop info
def drops(table):
	"""
		The 'drops()' function lists all players' drops
		
		Args:
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			message (str): The organized message to be sent to the player
	"""
	# Scan table
	scan = table.scan()
	
	# Get names and drops
	names =[]
	drops = []
	for profile in scan["Items"]:
		info = profile["info"]
		names.append(info['name'])
		drops.append(info['drops'])

	# Re-organize by BDSM score
	org_names = []
	org_drops = []
	for name in range(len(names)):
		biggest = 0
		index = 0
		for j in range(len(drops)):
			if drops[j] > biggest:
				biggest = drops[j]
				index = j
		org_names.append(names[index])
		names.remove(names[index])
		org_drops.append(drops[index])
		drops.remove(drops[index])
	
	# Develope message
	message = "DROPS:\n"
	for i in range(len(org_names)):
		message += str(i + 1) + ") " + str(org_names[i]) + " - Drops: " + str(org_drops[i]) + "\n"

	# Return message
	return message

# Self-plunk info
def selfPlunks(table):
	"""
		The 'selfPlunks()' function lists all players' self-plunks
		
		Args:
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			message (str): The organized message to be sent to the player
	"""
	# Scan table
	scan = table.scan()
	
	# Get names and self-plunks
	names =[]
	selfPlunks = []
	for profile in scan["Items"]:
		info = profile["info"]
		names.append(info['name'])
		selfPlunks.append(info['self_plunks'])

	# Re-organize by BDSM score
	org_names = []
	org_selfPlunks = []
	for name in range(len(names)):
		biggest = 0
		index = 0
		for j in range(len(selfPlunks)):
			if selfPlunks[j] > biggest:
				biggest = selfPlunks[j]
				index = j
		org_names.append(names[index])
		names.remove(names[index])
		org_selfPlunks.append(selfPlunks[index])
		selfPlunks.remove(selfPlunks[index])
	
	# Develope message
	message = "SELF PLUNKS:\n"
	for i in range(len(org_names)):
		message += str(i + 1) + ") " + str(org_names[i]) + " - SPs: " + str(org_selfPlunks[i]) + "\n"

	# Return message
	return message

# Fifa info
def fifas(table):
	"""
		The 'fifas()' function lists all players' FIFAs
		
		Args:
			table (db): The Dynamodb 'beer_die_stats' table
		
		Returns:
			message (str): The organized message to be sent to the player
	"""
	# Scan table
	scan = table.scan()

	# Get names and FIFAs
	names =[]
	fifas = []
	for profile in scan["Items"]:
		info = profile["info"]
		names.append(info['name'])
		fifas.append(info['fifas'])

	# Re-organize by BDSM score
	org_names = []
	org_fifas = []
	for name in range(len(names)):
		biggest = 0
		index = 0
		for j in range(len(fifas)):
			if fifas[j] > biggest:
				biggest = fifas[j]
				index = j
		org_names.append(names[index])
		names.remove(names[index])
		org_fifas.append(fifas[index])
		fifas.remove(fifas[index])

	# Develope message
	message = "FIFAS:\n"
	for i in range(len(org_names)):
		message += str(i + 1) + ") " + str(org_names[i]) + " - FIFAs: " + str(org_fifas[i]) + "\n"

	# Return message
	return message

# Calculate Beer Die Statistical Metric (BDSM) score
def calc_bdsm(profile, table):
	
	# Get all the maxStats from the table
	statsDict = {
		"plunks": 1,
		"self_plunks": 1,
		"drops": 1,
		"skunks": 1,
		"fifas": 1,
	}
	scan = table.scan()
	for entry in statsDict:
		for player in scan["Items"]:
			maxStat = int(statsDict[entry])
			stat = int(player["info"][entry])
			if stat > maxStat:
				statsDict[entry] = stat
	
	# Calculate statScores
	info = profile["info"]
	wins, losses, drops, plunks, selfPlunks, skunks, fifas = int(info["wins"]), int(info["losses"]), int(info['drops']), int(info['plunks']), int(info['self_plunks']), int(info["skunks"]), int(info["fifas"])
	if wins + losses < 10:
		return "---"
	winLossRatio = (wins / (wins + losses))
	plunksScore = (plunks / statsDict['plunks'])
	skunksScore = (skunks / statsDict['skunks']) 
	fifasScore = (fifas / statsDict['fifas'])
	if selfPlunks == 0:
		selfPlunksScore = 1
	else:
		selfPlunksScore = 1 - (selfPlunks / statsDict["self_plunks"])
	if drops == 0:
		dropsScore = 1
	else:
		dropsScore = 1 - (drops / statsDict['drops'])
	
	# print("Win/Loss ratio: {}".format(winLossRatio))
	# print("Plunks Score: {}".format(plunksScore))
	# print("Skunks Score: {}".format(skunksScore))
	# print("Self-Plunks Score: {}".format(selfPlunksScore))
	# print("Drops Score: {}".format(dropsScore))
	# print("FIFAs Score: {}".format(fifasScore))
	
	# Calculate and return bdsm
	bdsm = round(((5 * winLossRatio) + plunksScore + dropsScore + selfPlunksScore + skunksScore + fifasScore) / 10, 2)
	return bdsm

# Helper class for 'read()'
class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if o % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)