import csv
from flask import Flask, render_template, request

DATA_FILE = 'data.csv'
FIELDNAMES = ['id', 'name', 'price', 'summary']

app = Flask(__name__)

apartments = []

def load_data_file():
  with open(DATA_FILE) as data_file:
    reader = csv.DictReader(data_file)
    for row in reader:
      apartments.append(row)

def append_data_file(new_row):
  with open(DATA_FILE, 'a', newline='') as data_file:
    writer = csv.DictWriter(data_file, FIELDNAMES)
    writer.writerow(new_row)

@app.route('/apartments')
def apartments_index():
  return render_template('index.html', apartments=apartments)

@app.route('/apartments/<apartment_id>')
def apartments_show(apartment_id):
  for apartment in apartments:
    if apartment['id'] == apartment_id:
      return render_template('show.html', apartment=apartment)
  
  return { 'error': 'Not Found' }, 404

@app.route('/apartments', methods=['POST'])
def apartments_create():
  new_apartment = request.get_json()
  new_apartment['id'] = str(len(apartments) + 1)
  apartments.append(new_apartment)
  append_data_file(new_apartment)
  return { 'message': 'Apartment created successfully' }, 201

@app.route('/apartments/<apartment_id>', methods=['PATCH'])
def apartments_update(apartment_id):
  updated_apartment = request.get_json()

  for apartment in apartments:
    if apartment['id'] == apartment_id:
      apartment.update(updated_apartment)
      return { 'message': 'Apartment updated successfully' }, 201

  return { 'error': 'Not Found' }, 404

@app.route('/apartments/<apartment_id>', methods=['DELETE'])
def apartments_delete(apartment_id):
  found_apartment_idx = None

  for i in range(len(apartments)):
    if apartments[i]['id'] == apartment_id:
      found_apartment_idx = i
      break

  if found_apartment_idx != None:
    apartments.pop(found_apartment_idx)
    return { 'message': 'Apartment deleted successfully' }, 201
  
  return { 'error': 'Not Found' }, 404

load_data_file()
app.run()




