# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction
import smtplib
import pandas
import requests
import json

conf_cases_by_dist= requests.get('https://api.covid19india.org/state_district_wise.json')
covid_facilities = requests.get('https://api.covid19india.org/resources/resources.json')
df_conf = pandas.read_csv('http://api.covid19india.org/states_daily_csv/confirmed.csv')
df_death = pandas.read_csv('https://api.covid19india.org/states_daily_csv/deceased.csv')
df_recovered = pandas.read_csv('https://api.covid19india.org/states_daily_csv/recovered.csv')

statecode_to_state = {"state_mappings":{'tt':'Total','kl':'Kerala', 'dl':'Delhi','tg':'Telangana','rj':'Rajasthan','hr':'Haryana','up':'Uttar Pradesh','la':'Ladakh','tn':'Tamil Nadu','jk':'Jammu and Kashmir','ka':'Karnataka','mh':'Maharashtra','pb':'Punjab','ap':'Andhra Pradesh','ut':'Uttarakhand','or':'Odisha','py':'Puducherry','wb':'West Bengal','ch':'Chandigarh','ct':'Chhattisgarh','gj':'Gujarat','hp':'Himachal Pradesh','mp':'Madhya Pradesh','br':'Bihar','mn':'Manipur','mz':'Mizoram','ga':'Goa','an':'Andaman and Nicobar Islands','jh':'Jharkhand','as':'Assam','ar':'Arunachal Pradesh','tr':'Tripura','ml':'Meghalaya'}}
state_to_statecode = {"state_mappings":{'Total':'tt','Kerala':'kl', 'Delhi':'dl','Telangana':'tg','Rajasthan':'rj','Haryana':'hr','Uttar Pradesh':'up','Ladakh':'la','Tamil Nadu':'tn','Jammu and Kashmir':'jk','Karnataka':'ka','Maharashtra':'mh','Punjab':'pb','Andhra Pradesh':'ap','Uttarakhand':'ut','Odisha':'or','Puducherry':'py','West Bengal':'wb','Chandigarh':'ch','Chhattisgarh':'ct','Gujarat':'gj','Himachal Pradesh':'hp','Madhya Pradesh':'mp','Bihar':'br','Manipur':'mn','Mizoram':'mz','Goa':'ga','Andaman and Nicobar Islands':'an','Jharkhand':'jh','Assam':'as','Arunachal Pradesh':'ar','Tripura':'tr','Meghalaya':'ml'}}

facilities_json= covid_facilities.json()

def get_death_count_by_state(state):
    stateval = state.title()
    statecode = (state_to_statecode['state_mappings'][stateval]).upper()
    return sum(df_death[statecode])

def get_conf_count_by_state(state):
    stateval = state.title()
    statecode = (state_to_statecode['state_mappings'][stateval]).upper()
    return sum(df_conf[statecode])

def get_recovered_count_by_state(state):
    stateval = state.title()
    statecode = (state_to_statecode['state_mappings'][stateval]).upper()
    return sum(df_recovered[statecode])

def get_testcenters_by_state(state):
    facilities = []
    for res in facilities_json['resources']:
        if res['category']== 'CoVID-19 Testing Lab' and res['state']== state.title():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities

def get_hospitals_by_state(state):
    facilities = []
    for res in facilities_json['resources']:
        if (res['category']== 'Hospitals and Centers' or res['category']== 'Hospitals and Centers') and res['state']== state.title():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+res['phonenumber'])
    return facilities

def get_testcenters_by_city(city):
    facilities = []
    for res in facilities_json['resources']:
        if res['category']== 'CoVID-19 Testing Lab' and res['city']== city.title():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities

def get_shelterhomes_by_city(city):
    facilities = []
    for res in facilities_json['resources']:
        if res['category']== 'Accommodation and Shelter Homes' and res['city']== city.title():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities 

#Community Kitchen
def get_freefoods_by_city(city):
    facilities = []
    for res in facilities_json['resources']:
        if (res['category']== 'Free Food' or res['category']== 'Community Kitchen') and res['city']== city.title():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities 

class ActionFacilitySearch(Action):

    def name(self) -> Text:
        return "action_facility_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        facility = tracker.get_slot("facility_type")
        location = tracker.get_slot("location")

        print("Tracked Facility: "+facility)
        print("Tracked Location: "+location)
        #code when location: location, zipcode: zip, facility_type: hospital
        #code when location: location, zipcode: zip, facility_type: test center
       
        #can write query here to retrieve data from database or APIs
        address = "Bangalore Medical College & Research Institute, Fort, K.R. Road, Bangalore-560002"
        dispatcher.utter_message("Here is the address of the {} in {}: {}".format(facility, location, address))

        return [SlotSet("address", address)]

class FacilityForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "user_form"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["username","location"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {
             "username": [self.from_text(intent=None), self.from_text()],
             "location": [self.from_entity(entity="location", intent="inform"), self.from_text()]
              }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],) -> List[Dict]:
        """Define what the form has to do
        after all required slots are filled"""
        print("username:"+ tracker.get_slot('username'))
        print("location:"+ tracker.get_slot('location'))
        #dispatcher.utter_message(template="utter_submit")
        return []


# class ActionSetUsername(Action):

#     def name(self) -> Text:
#         return "action_set_username"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         name = tracker.latest_message.get('text')
#         print("Tracked Name: "+name)
#        # dispatcher.utter_message("Thank you {} for using our service".format(name))
#         return [SlotSet("intent_message", name)]

def sendMail(body):
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    # start TLS for security 
    s.starttls() 
  
    # Authentication 
    s.login("tuhinssamanta@gmail.com", "#########") 
  
    # message to be sent 
    message = body
  
    # sending the mail 
    s.sendmail("tuhinssamanta@gmail.com", "tuhinssamanta@gmail.com", message) 
  
    # terminating the session 
    s.quit() 
