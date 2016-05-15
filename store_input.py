from flask import Flask, request, url_for, make_response, current_app
import sqlite3
import datetime
import json
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to SQLite database if it does not yet exists
db_conn = sqlite3.connect('data/entries.sqlite')
db_cursor = db_conn.cursor()
# Initialize table
db_cursor.execute('''CREATE TABLE IF NOT EXISTS entries(
		name TEXT,
		email TEXT,
		partner_name TEXT,
		partner_email TEXT,
		address TEXT,
		answer_question_1 TEXT,
		answer_question_2 TEXT,
		answer_question_3 TEXT,
		answer_question_4 TEXT,
		suggestions TEXT,
		time_of_entry TEXT
	)''')
db_conn.close()

# @app.after_request
# def after_request(response):
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#    return response


@app.route('/store_results', methods=['POST'])
#@cross_origin()
def store_results():

	print('Beginning of store results function')
	print('Request method %s' %request.method)

	# Convert form entries
	entry = dict((key, request.form.getlist(key)[0]) for key in request.form.keys())
	print('%s is filling in the questionaire' %str(entry['name']))
	time_of_entry = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
	entry = [(entry['name'], entry['email'], entry['partner_name'], entry['partner_email'], entry['address'], entry['question_veggie'], entry['question_statistics'],\
				entry['question_drinks'],entry['question_music'], entry['suggestions'], time_of_entry)]	
	

	# Write in db
	try:
		
	 	db_conn = sqlite3.connect('data/entries.sqlite')
	 	db_cursor = db_conn.cursor()
	 	#db_cursor.execute('''INSERT INTO entries VALUES (?,?,?,?,?,?,?,?,?,?,?)''', );
	 	db_cursor.executemany('INSERT INTO entries VALUES (?,?,?,?,?,?,?,?,?,?,?)', entry)
	 	print('Is he trying')
	 	db_conn.commit()
	 	db_conn.close()
	 	return('success')

	except sqlite3.Error as e:
	 	print('Exception occured')
	 	if db_conn:
	 		db_conn.rollback()
	 		print("Error %s:" % e.args[0])
	 		return('error')


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug = True)