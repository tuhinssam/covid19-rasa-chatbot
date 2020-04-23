# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset
import smtplib
import pandas
import requests
import json

'''
API to access COVID related information
'''
cases_by_dist= requests.get('https://api.covid19india.org/state_district_wise.json')
covid_facilities = requests.get('https://api.covid19india.org/resources/resources.json')
df_conf = pandas.read_csv('http://api.covid19india.org/states_daily_csv/confirmed.csv')
df_death = pandas.read_csv('https://api.covid19india.org/states_daily_csv/deceased.csv')
df_recovered = pandas.read_csv('https://api.covid19india.org/states_daily_csv/recovered.csv')

#state vs state code mapping
statecode_to_state = {"state_mappings":{'tt':'Total','kl':'Kerala', 'dl':'Delhi','tg':'Telangana','rj':'Rajasthan','hr':'Haryana','up':'Uttar Pradesh','la':'Ladakh','tn':'Tamil Nadu','jk':'Jammu and Kashmir','ka':'Karnataka','mh':'Maharashtra','pb':'Punjab','ap':'Andhra Pradesh','ut':'Uttarakhand','or':'Odisha','py':'Puducherry','wb':'West Bengal','ch':'Chandigarh','ct':'Chhattisgarh','gj':'Gujarat','hp':'Himachal Pradesh','mp':'Madhya Pradesh','br':'Bihar','mn':'Manipur','mz':'Mizoram','ga':'Goa','an':'Andaman and Nicobar Islands','jh':'Jharkhand','as':'Assam','ar':'Arunachal Pradesh','tr':'Tripura','ml':'Meghalaya'}}
state_to_statecode = {"state_mappings":{'Total':'tt','Kerala':'kl', 'Delhi':'dl','Telangana':'tg','Rajasthan':'rj','Haryana':'hr','Uttar Pradesh':'up','Ladakh':'la','Tamil Nadu':'tn','Jammu and Kashmir':'jk','Karnataka':'ka','Maharashtra':'mh','Punjab':'pb','Andhra Pradesh':'ap','Uttarakhand':'ut','Odisha':'or','Puducherry':'py','West Bengal':'wb','Chandigarh':'ch','Chhattisgarh':'ct','Gujarat':'gj','Himachal Pradesh':'hp','Madhya Pradesh':'mp','Bihar':'br','Manipur':'mn','Mizoram':'mz','Goa':'ga','Andaman and Nicobar Islands':'an','Jharkhand':'jh','Assam':'as','Arunachal Pradesh':'ar','Tripura':'tr','Meghalaya':'ml'}}

facilities_json= covid_facilities.json()

def get_dist_based_stat():
    case_dict = {}
    for state in cases_by_dist.json().keys():
        for place, val in zip(cases_by_dist.json()[state]['districtData'].keys(), cases_by_dist.json()[state]['districtData'].values()):
            case_dict[place] = {'confirmed':val['confirmed'], 'deceased':val['deceased'], 'recovered':val['recovered']}
    return case_dict

#***************************STATISTICS***********************************
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


#***************************FACILITIES***********************************
def get_testcenters_by_state(state):
    facilities = []
    for res in facilities_json['resources']:
        if res['category'].lower() == 'CoVID-19 Testing Lab'.lower() and res['state'].lower() == state.lower():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities

def get_hospitals_by_state(state):
    facilities = []
    for res in facilities_json['resources']:
        if res['category'].lower() == 'hospitals and centers' and res['state'].lower()== state.lower():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+res['phonenumber'])
    return facilities

def get_testcenters_by_city(city):
    facilities = []
    for res in facilities_json['resources']:
        if res['category'].lower() == 'CoVID-19 Testing Lab'.lower() and res['city'].lower() == city.lower():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities

def get_hospitals_by_city(city):
    facilities = []
    for res in facilities_json['resources']:
        if res['category'].lower() == 'hospitals and centers' and res['city']== city.lower():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+res['phonenumber'])
    return facilities

def get_shelterhomes_by_city(city):
    facilities = []
    for res in facilities_json['resources']:
        if res['category'].lower()== 'accommodation and shelter homes' and res['city'].lower()== city.lower():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities 

def get_shelterhomes_by_state(state):
    facilities = []
    for res in facilities_json['resources']:
        if res['category'].lower()== 'accommodation and shelter homes' and res['state'].lower()== state.lower():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities 

def get_freefoods_by_city(city):
    facilities = []
    for res in facilities_json['resources']:
        if (res['category'].lower() == 'free food' or res['category'].lower()== 'community Kitchen') and res['city'].lower()== city.lower():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities 

def get_freefoods_by_state(state):
    facilities = []
    for res in facilities_json['resources']:
        if (res['category'].lower() == 'free food' or res['category'].lower() == 'community kitchen') and res['state']== state.title():
            facilities.append(res['nameoftheorganisation']+", "+res['city']+", "+res['state']+", "+"Phone: "+res['phonenumber'])
    return facilities 

#======================ACTION CLASSES============================
class ActionFacilitySearch(Action):

    def name(self) -> Text:
        return "action_facility_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            facility = tracker.get_slot("facility_type")
            location = tracker.get_slot("location")
            name = tracker.get_slot("username")
            emailid = tracker.get_slot("emailid")

            #location = 'bangalore'
            #name = 'tuhin'
            #emailid = 'tuhinssam@gmail.com'

            print("Tracked Facility: "+facility)
            print("Tracked Location: "+location)

            if facility == "free food":
                facilities_city = get_freefoods_by_city(location.title())
                facilities_state = get_freefoods_by_state(location.title())
                if len(facilities_city) != 0:
                    allfacilities = "\n".join(facilities_city)
                    dispatcher.utter_message("Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities))
                elif len(facilities_state) != 0:
                    allfacilities = "\n".join(facilities_state)
                    dispatcher.utter_message("Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities))
                else:
                    dispatcher.utter_message("No {} found in {}".format(facility,location))
            
            if facility == "hospital":
                facilities_state = get_hospitals_by_state(location.title())
                facilities_city = get_hospitals_by_city(location.title())
                if len(facilities_city) != 0:
                    allfacilities = "\n".join(facilities_city)
                    dispatcher.utter_message("Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities))
                elif len(facilities_state) != 0:
                    allfacilities = "\n".join(facilities_state)
                    dispatcher.utter_message("Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities))
                else:
                    dispatcher.utter_message("No {} found in {}".format(facility,location))
            
            if facility == "test center":
                facilities_city = get_testcenters_by_city(location.title())
                facilities_state = get_testcenters_by_state(location.title())

                if len(facilities_city) != 0:
                    allfacilities = "\n".join(facilities_city)
                    dispatcher.utter_message("Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities))
                elif len(facilities_state) != 0:
                    allfacilities = "\n".join(facilities_state)
                    dispatcher.utter_message("Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities))
                else:
                    dispatcher.utter_message("No {} found in {}".format(facility,location))
            
            if facility == "shelter home":
                facilities_city = get_shelterhomes_by_city(location.title())
                facilities_state = get_shelterhomes_by_state(location.title())
                if len(facilities_city) != 0:
                    allfacilities = "\n".join(facilities_city)
                    dispatcher.utter_message("Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities))
                elif len(facilities_state) != 0:
                    allfacilities = "\n".join(facilities_state)
                    dispatcher.utter_message("Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities))
                else:
                    dispatcher.utter_message("No {} found in {}".format(facility,location))
            if facility == "corona cases":
                cases_dict = get_dist_based_stat()
                if location.title() in cases_dict.keys():
                    cases = cases_dict[location.title()]
                    dispatcher.utter_message("Here is the statistics for {}: \n Confirmed Cases: {} Deceased: {} Recovered: {}".format(location, cases['confirmed'], cases['deceased'], cases['recovered']))
                else:
                    dispatcher.utter_message("Sorry! Location not found")
            if facility == "email": 
                facilities_city = get_testcenters_by_city(location.title())
                facilities_state = get_testcenters_by_state(location.title())
                bodystr1 = ""
                bodystr2 = ""
                body = ""
                if len(facilities_city) != 0:
                    allfacilities = "\n".join(facilities_city)
                    bodystr1 = "Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities)
                elif len(facilities_state) != 0:
                    allfacilities = "\n".join(facilities_state)
                    bodystr1 = "Here is the address of the {} facilities in {}: {}".format(facility, location, allfacilities)

                cases_dict = get_dist_based_stat()
                if location.title() in cases_dict.keys():
                    cases = cases_dict[location.title()]
                    bodystr2 = "Here is the statistics for {}: \n Confirmed Cases: {} Deceased: {} Recovered: {}".format(location, cases['confirmed'], cases['deceased'], cases['recovered'])
                else:
                    bodystr2 = "Sorry! Location not found"
                
                body = bodystr1 +"\n\n"+bodystr2
                sendMail(emailid, name, body)
                dispatcher.utter_message("email sent")

        except:
            dispatcher.utter_message("Sorry: Could not get information dute to internal error")
            
        return []

class UserForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "user_form"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["username","emailid","mobilenumber","location"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {
             "username": [self.from_text(intent=None), self.from_text()],
             "emailid": [self.from_text(intent=None), self.from_text()],
             "mobilenumber": [self.from_text(intent=None), self.from_text()],
             "location": [self.from_entity(entity="location", intent="inform"), self.from_text()]
              }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],) -> List[Dict]:
        try:
                """Define what the form has to do
            after all required slots are filled"""
            print("username:"+ tracker.get_slot('username'))
            print("emailid:"+ tracker.get_slot('emailid'))
            print("mobilenumber:"+ tracker.get_slot('mobilenumber'))
            print("location:"+ tracker.get_slot('location'))
            dispatcher.utter_message("Thank you for providing all the details! How may I help you?")
        except:
            dispatcher.utter_message("Sorry! some internal error has occoured!")
        
        return []


def sendMail(emailid, name, body):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    # start TLS for security 
    s.starttls() 
  
    # Authentication password needs to be added to run the code
    s.login("tuhinssamanta@gmail.com", "######") 

    # message to be sent 
    text = "Dear "+name+",\n\n"+"Please find the required details:\n"+ body + "\n\n"+"Thanks and Regards\n -Covid-19 Assistant\nStay Home, Stay Safe"
    subject = "Covid19 assistant summary"
    message = 'Subject: {}\n\n{}'.format(subject, text) 
    # sending the mail 
    s.sendmail("tuhinssamanta@gmail.com", emailid, message)
    # terminating the session 
    s.quit()  
