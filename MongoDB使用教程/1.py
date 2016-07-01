#!/usr/bin/env python
#coding=utf-8

from pymongo import MongoClient
from datetime import datetime


client = MongoClient()
db = client.test

data = {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    }

def my_inset(data):
	result = db.restaurants_1.insert_one(data)
	result.inserted_id

def get_data():
	cursor = db.restaurants.find()
	for document in cursor:
		print(document)
        print "\n"

if __name__ == '__main__':
	get_data()
