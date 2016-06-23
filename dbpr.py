from collections import OrderedDict
import datetime
import sys
import os

from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
	content = TextField()
	timestamp = DateTimeField(default= datetime.datetime.now)
	
	class Meta:
		database = db


def clearScreen():
	os.system('cls' if os.name=='nt' else 'clear')


def initialize():
#Creates tables and database if they dont exist
	db.connect()
	db.create_tables([Entry], safe= True)


def menu_loop():
	"""show the menu"""
	choice = None
	
	while choice != 'q':
		clearScreen()
		print 'Enter "q" to quit'
		for key, value in menu.items():
			print '{}) {}'.format(key, value.__doc__)
		choice = raw_input("Action:   ").lower().strip()
		if choice in menu:
			clearScreen()
			menu[choice]()


def add_entry():
	"""adds entry"""
	print 'Enter your entry.  Press ctrl+d when finished'
	data = sys.stdin.read().strip()
	if data:
		if raw_input("Save Entry? (Y/n)    ").lower() != 'n':
			Entry.create(content= data)
			print "Saved successfully"


def view_entries(search_query= None):
	"""view entries"""
	entries = Entry.select().order_by(Entry.timestamp.desc())
	if search_query:
		entries = entries.where(Entry.content.contains(search_query))
	for entry in entries:
		timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
		print timestamp
		print ('='* len(timestamp))
		print entry.content
		print '\n\n' + '='*len(timestamp)
		print "'n' for next entry"
		print "'d' for delete entry"
		print "'q' to quit"
		next_action = raw_input("Enter n/q     ").lower().strip()
		if next_action == 'q':
			break
		elif next_action == 'd':
			delete_entries(entry)
		else:
			clearScreen() 
			continue
			

def delete_entries(entry):
	"""deletes entries"""
	if raw_input('Remove Y/n   ').lower() == 'y':
		entry.delete_instance()
	

def search_entries():
	"""searches Entries"""
	view_entries(raw_input('Enter search term   '))	
	

menu = OrderedDict([
		('a', add_entry),
		('v', view_entries),
		('s', search_entries)
])

if __name__ == '__main__':
	initialize()
	menu_loop()


	