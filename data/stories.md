## hospital search happy path
* greet
  - utter_how_can_i_help
* search_provider{"facility_type":"hospital", "location": "San Francisco"}
  - action_facility_search
  - utter_address
* thanks
  - utter_goodbye

## hospital search + location
* greet
  - utter_how_can_i_help
* search_provider{"facility_type":"hospital"}
  - utter_ask_location
* inform{"location":"San Francisco"}
  - action_facility_search
  - utter_address
* thanks
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye
