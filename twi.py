# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import TwilioRestClient;

# Libraries allowing the user to choose a file from the file dialog
from pathlib import Path;
import tkinter as tk
from tkinter import filedialog

# the Python library containing functions for csv files
import csv

# Google's PhoneNumbers package that can validate phone numbers
import phonenumbers

# functions for quickly displaying time
import time

# Account Sid and Auth Token from twilio.com/user/account
ACCOUNT_SID = "";
AUTH_TOKEN = "";
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN);
# Account phone number
accountNumber = "";

# We want to make sure the phone numbers are in E.164 format that
# Twilio can read/process. All parenthesis, spaces, dashes, and
# other characters will be removed and a single + will be added
# to the beginning of the number. If numbers are 10 digits, we will
# assume that they are US numbers.
def formatNumber(phoneNumber):
	characters = ["(",")"," ","-","+","."]

	for c in characters:
	    while c in phoneNumber:
	        i = phoneNumber.find(c)
	        phoneNumber = phoneNumber[:i] + phoneNumber[i+1:]
	if len(phoneNumber) == 10:
		phoneNumber = "+1" + phoneNumber
	elif len(phoneNumber) > 10:
		phoneNumber = "+" + phoneNumber
	return phoneNumber

# The validate function checks the possibility and validity of a phone
# number. If it is less than 10 digits, it is not a possible phone
# number. The function then uses a Google library to check if a phone
# number is valid.
def validate(phoneNumber):
	if len(phoneNumber) < 10:
		return 2
	try:
		p = phonenumbers.parse(phoneNumber,None)
		if phonenumbers.is_valid_number(p):
			valid = True
			return 1
		else:
			valid = False
			return 3
	except Exception as e:
		print(e)
		log.write(str(e) + "\n")
		pass
	return 4

# This section utilizes a "file explorer" so the user can select
# the file that contains the phone numbers. When a file is
# chosen, its path is saved.
root = tk.Tk();
root.withdraw();
file_path = filedialog.askopenfilename();

# Query the user for the name of the log
logName = input("Enter the name of the log file:\n\n")
print("\n")

# This section utilizes a mini-prompt to allow the user to
# type the body of the text message.
text = input("/* Enter message */" + "\n" + "\n");
print("\n\n")

# Create a text file to log the text
log = open(logName + ".txt","w")
localtime = time.asctime(time.localtime(time.time()))
log.write("Local current time: " + str(localtime) + "\n\n")
log.write("Message text: " + text + "\n\n\n" + "Text Message data:\n\n")

# A file object is created as "f". Line 102 contains a for loop that
# will go through every line and get the phone number. Next,
# a message object is created and sends the message.

# counts the number of requests sent
i = 0
# counts the number of requests attempted
p = 0
# counts the phone numbers that Twilio cannot send to
# this is usually due to blacklisting
b = 0
# counts the number of phone number validation errors
v = 0

with open(file_path, 'r') as f:
	phoneReader = csv.reader(f, delimiter=',')
	for line in f:
		for row in phoneReader:
			p = p + 1
			print("Line " + str(p))
			log.write("Line " + str(p) + "\n")
			pNumber=row[0];
			origNumber = pNumber
			pNumber = formatNumber(pNumber);
			if validate(pNumber) == 1:
				try:
					message = client.messages.create(body=text,
					    to=pNumber,
					    from_=accountNumber);
				except Exception as e:
					print(e)
					log.write(str(e))
					b = b + 1
					pass
				i = i + 1
				print(str(i) + " HTTP request(s) sent. Last phone number: " + pNumber)
				log.write(str(i)+ "  HTTP request(s) sent. Last phone number: " + pNumber + "\n")
			elif validate(pNumber) == 2:
				print("Error: " + pNumber + " is not a possible phone number.")
				log.write("Error: " + pNumber + " is not a possible phone number.\n")
			elif validate(pNumber) == 3:
				print("Error: " + pNumber + " is not a valid phone number.")
				log.write("Error: " + pNumber + " is not a valid phone number.\n")
			elif validate(pNumber) == 4:
				v = v + 1
			print("\n")
			log.write("\n")

# Present a summary of requests
print ("All HTTP requests sent.");
log.write("\nAll HTTP requests sent.\n")

print(str(i) + " out of " + str(p) + " total phone numbers validated.")
log.write(str(i) + " out of " + str(p) + " total phone numbers validated.\n")

print(str(v) + " out of " + str(p) + " total phone numbers could not be interpreted by the phone number parse function.")
log.write(str(v) + " out of " + str(p) + " total phone numbers could not be interpreted by the phone number parse function.\n")

print(str(b) + " out of " + str(i) + " validated phone numbers were not queued due to blacklisting or some other Twilio error.")
log.write(str(b) + " out of " + str(i) + " validated phone numbers were not queued due to blacklisting or some other Twilio error.\n")

print(str(i - b) + " out of " + str(p) + " total phone numbers were queued by Twilio.")
log.write(str(i - b) + " out of " + str(p) + " total phone numbers were queued by Twilio.\n")
