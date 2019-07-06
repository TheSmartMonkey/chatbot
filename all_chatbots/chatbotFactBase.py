# coding: utf8

import pandas as pa
import random
import string
import json
from copy import copy


class FactBase(object):
    def __init__(self):
        self.airport = pa.read_csv("airport.csv", sep = ",", encoding = "utf-8")
        self.flight = pa.read_csv("flight.csv", sep = ",", encoding = "utf-8")

        self.IATA = self.airport.set_index("IATA")
        self.fullFlight = self.flight.join(self.airport.set_index("IATA"), on = "FROM_IATA", rsuffix = "_from") \
        .join(self.airport.set_index("IATA"), on = "TO_IATA", rsuffix = "_to")
        self.days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        self.cities = self.build_dict(self.airport.city.values)
        self.countries = self.build_dict(self.airport.country.values)
        self.iata = self.build_dict(self.airport.IATA.values)

    # Format my facts
    def build_dict(self,values):
        return dict([(value.lower().strip(),value) for value in values if type(value)==str])

    # check if a text contains a element of the dictionnary
    def text_contains(self,text,refdict):
        words = text.lower().split(" ")
        for i in range(0, len(words)):
            for j in range(len(words), i, -1):
                name = " ".join(words[i:j])
                if  name in refdict:
                    return refdict[name]
        return None

    # Facts
    ## Citys
    def checkCity(self,city):
        return city in self.cities

    def listCity(self):
        return self.cities.values()

    def containCity(self,text):
        return self.text_contains(text,self.cities)

    def randomCity(self):
        randomLetter = random.choice(string.ascii_uppercase)
        for city in self.listCity():
            if city.startswith(randomLetter):
                return city

    ## Countries
    def checkCountry(self,country):
        return country in self.countries

    def listCountry(self):
        return self.countries.values()

    def listCityInCountry(self,country):
        return list(set(self.airport[self.airport.country==country].city.values))

    def containCountry(self,text):
        return self.text_contains(text,self.countries)
    
    ## Flights
    def checkFlight(self,flight):
            return True
    
    def listFlight(self,cityFrom,cityTo):
        flight = self.fullFlight[(self.fullFlight.city==cityFrom) & (self.fullFlight.city_to==cityTo)]
        return list(zip(flight.name.values,flight.name_to.values))
    
    ## Airports
    def listField(self):
        return self.airport.columns

    ### Check my Facts
    def checkFact(self,var,val):
        if var == "city":
            return self.checkCity(val)
        elif var == "country":
            return self.checkCountry(val)
        elif var == "day":
            return val in self.days
        elif var == "flight":
            return val in self.checkFlight(val)
        else:
            return True


def testFacts():
    fb = FactBase()

    # print("cities in France:",fb.listCityInCountry("France"))
    # print("Give a City:",fb.checkCity("Paris".lower()))
    # print("all Citys:",",".join([c for c in fb.listCity() if c.startswith("A")]))
    # print("all Countrys:",fb.listCountry())
    # print("flight:",fb.listFlight("Paris","San Francisco"))
    print("Random City: ",fb.randomCity())
    # print(fb.listCity)
