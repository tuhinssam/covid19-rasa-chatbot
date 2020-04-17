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
