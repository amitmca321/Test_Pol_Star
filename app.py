#Python version used is - Python 3.10.8
import bottle # pip install bottle https://bottlepy.org/docs/dev/tutorial_app.html
import csv
import sqlite3
from bottle import app, get, hook, post, route, run, request, response
from bottle import HTTPResponse

#Read the given CSV file

with open('positions.csv') as file_csv:
    file_csv_read = csv.reader(file_csv, delimiter=',')
    all_value = []
    for row in file_csv_read:
        value = (row[0], row[1], row[2], row[3])
        all_value.append(value)


#Logic to return dict
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Logic to connect SQLite3 database
db = sqlite3.connect(':memory:')
db.row_factory = dict_factory

# Note I have designed below database query only for runtime execution as it is a test project, in real I might have created/designed these tables and inserted the records in real database instead of ':memory:'
db.executescript('''
    BEGIN TRANSACTION;
    CREATE TABLE ships(imo char(7), ship_name varchar(50));
    INSERT INTO ships VALUES('9632179', 'Mathilde Maersk');
    INSERT INTO ships VALUES('9247455', 'Australian Spirit');
    INSERT INTO ships VALUES('9595321', 'MSC Preziosa');
    CREATE TABLE positions(imo char(7), time_stamp text, latitude real, longitude real);
    COMMIT;
''')

#Below logic is to take care of populating the database with all the records received from the CSV file

query = "insert into `positions`(`imo`, `time_stamp`, `latitude`, `longitude`) values (?, ?, ?, ?)"
mycursor = db.cursor()
mycursor.executemany(query, all_value)
db.commit()

#This is the entry point of the welcome page
@bottle.get('/')
def index():
    bottle.response.content_type = 'text/plain'
    return "Pole Star Candidate Exercise for Amit Kumar Dubey :)"

#Create the endpoint: GET/ships to fetch the list of current ships from the database.
@bottle.get('/ships')
def test_get_ships():
    cur = db.cursor()
    cur.execute("""SELECT *FROM ships""")
    rows = cur.fetchall()
    return dict(ships=rows)
    
#Create the endpoint: get/positions/<imo> to query the details for the given imo number
@bottle.get('/positions/<imo>/') 
def test_get_positions(**kwargs):
    inputed_imo = kwargs["imo"]
    cur = db.cursor()
    data = cur.execute("""SELECT a.ship_name, b.imo, b.latitude, b.longitude from ships a inner join positions b on a.imo=b.imo where a.imo = ? order by b.time_stamp desc""",[inputed_imo])
    row1 = cur.fetchall()

    response.status = 200
    bottle.response.content_type = 'application/json'
    return dict(ships=row1)
    




if __name__ == '__main__':
    import sys
    hostname = 'localhost'
    port = '8080'
    if len(sys.argv) >= 2:
        hostname = sys.argv[1]
    if len(sys.argv) >= 3:
        port = sys.argv[2]

    bottle.debug()
    bottle.run(host=hostname, port=int(port), reloader=True)