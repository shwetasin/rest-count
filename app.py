import os
from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import socket

from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/Countries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Country(db.Model):
    __tablename__ = 'Country'
    id = db.Column(db.Integer, primary_key=True)
    country=db.Column(db.String(100))
    capital= db.Column(db.String(100))
    currency=db.Column(db.String(100))
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

    countries =Country.query.all()

    obj=[]


    for country in countries:


        country_data ={}
        country_data ['country'] =country.country
        country_data ['capital'] =country.capital
        country_data ['currency'] =country.currency
        country_data ['region'] =country.region
        country_data['language '] = country.language
        country_data['area '] = country.area
        country_data['flag '] = country.flag
        country_data['population'] = country.population
        country_data['timezone'] = country.timezone


        obj.append(country_data)

    print(obj)
    return {'countries':obj}
    
if __name__ == '__main__':
    app.run(debug= True)