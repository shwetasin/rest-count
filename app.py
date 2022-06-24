from locale import currency
import os
from sqlite3 import register_converter
from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import socket
import requests
import json

from sqlalchemy.sql import func

URL ="https://restcountries.com/v3.1/all"


location = "Countries"

PARAMS = {'address':location}

r = requests.get(url = URL, params = PARAMS)

data = r.json()

latitude = data[0]['latlng'][0]
longitude = data[0]['latlng'][1]
# formatted_address = data['results'][0]['formatted_address']

print("Latitude:%s\nLongitude:%s"
      %(latitude, longitude))


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://:postgres@localhost/Countries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)




class Country(db.Model):
    __tablename__ = 'Country'
    id = db.Column(db.Integer, primary_key=True)
    country=db.Column (db.JSON)
    capital= db.Column(db.String(100))
    currency=db.Column(db.JSON)
    region = db.Column(db.String(100))
    language = db.Column(db.String(150))
    area = db.Column(db.Float(50))
    flag = db.Column(db.String(100))
    population = db.Column(db.Integer())
    timezone = db.Column(db.String(10))


    def __repr__(self):
        return f'<Country {self.capital}>'

@app.route('/country/<int:page_num>')
def country (page_num):
    paginated_obj= Country.query.paginate(per_page=5, page=page_num, error_out=True)
    country=paginated_obj.items
    return {"has_next":paginated_obj.has_next,"total_pages":paginated_obj.pages,"total_items":paginated_obj.total,'countries':[]}


@app.route('/country', methods=['GET'])

def get_all_countries():
    # country = Country.query.filter_by(country=request.data['country']).first()

    # countries =Country.query.all()
    URL ="https://restcountries.com/v3.1/all"

    r = requests.get(url = URL, params = PARAMS)

    countries = r.json()
    obj=[]

    countries_list= []
    for country in countries:
        print('---------------1---------->')
        country_obj = Country (
    
            country=country['name'] ['common'],
            capital=country['capital'][0] if 'capital' in country else None,
            currency=country['currencies'] if 'currencies' in country else None,
            region=country['region'] if 'region' in country else None,
            language=country['languages'] if 'languages' in country else None,
            area=country['area'] if 'area' in country else None,
            flag=country['flags'] if 'flags' in country else None,
            population=country['population'] if 'population' in country else None,
            timezone=country['timezones'] if 'timezones' in country else None,
        )
        countries_list.append(country_obj)


        print('---------------2---------->')


        country_data ={}
        country_data ['country'] =country['name']['common']
        country_data ['capital'] =country['capital'][0] if 'capital' in country else None
        country_data ['currency'] =country['currencies'] if 'currencies' in country else None
        country_data ['region'] =country['region'] if 'region' in country else None
        country_data['language '] = country['languages'] if 'languages' in country else None
        country_data['area '] = country['area'] if 'area' in country else None
        country_data['flag '] = country['flags'] if 'flags' in country else None
        country_data['population'] = country['population'] if 'population' in country else None
        country_data['timezone'] = country['timezones'] if 'timezones' in country else None


        obj.append(country_data)

    print(obj)
    db.session.add_all(countries_list)
    db.session.commit()
    return {'countries':obj}
    
if __name__ == '__main__':
    app.run(debug= True)