# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

# TODO : add def validate_xxx for each entity in form

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import isabel


# Form to gather slots from the customer to get a diagnostic.
class DiagnosticForm(FormAction):
    # name (built-in function) : specifies the name of the function that is referenced in the
    # domain file and called by the stories.
    def name(self) -> Text:
        return "DiagnosticForm"

    # required_slots (built-in function) : specifies the list of qui required slots
    # (is triggered each time a new slot is populated).
    @staticmethod
    def required_slots(tracker) -> List[Text]:
        returnList = ["symptoms", "symptoms2", "symptoms3"]

        if tracker.get_slot('sex') == 'm':
            return returnList + ["sex", "birthdate", "country"]
        else:
            return returnList + ["sex", "pregnant", "birthdate", "country"]

    # submit (built-in function) : is triggered when the form is completed.
    # dispatcher.utter_message(text=...) specifies the text to play to the user.
    # the return value can be used to set slots.
    def submit(self, dispatcher, tracker, domain) -> List[Dict]:
        responseText = isabel.getDiagnostic(tracker.slots["birthdate"],
                                            tracker.slots["sex"],
                                            tracker.slots["pregnant"],
                                            tracker.slots["country"],
                                            tracker.slots['symptoms1'] + ","
                                            + tracker.slots['symptoms2'] + ","
                                            + tracker.slots['symptoms3'] + ",")

        dispatcher.utter_message(text=responseText)

        return []

    @staticmethod
    def validate_symptoms(value, dispatcher, tracker, domain) -> Dict[Text, Any]:
        print("symptoms = ")
        print(value)
        if tracker.get_slot("symptoms1") is None:
            if type(value) is list:
                if len(value) == 1:
                    return {"symptoms1": value[0]}
                elif len(value) == 2:
                    return {"symptoms1": value[0], "symptoms2": value[1]}
                else:
                    return {"symptoms1": value[0], "symptoms2": value[1], "symptoms3": ",".join(value[2:])}
            return {"symptoms1": value}
        elif tracker.get_slot("symptoms2") is None:
            if type(value) is list:
                if len(value) == 1:
                    return {"symptoms2": value[0]}
                else:
                    return {"symptoms2": value[0], "symptoms3": ",".join(value[1:])}
            return {"symptoms2": value}
        else:
            if type(value) is list:
                return {"symptoms3": ",".join(value)}
            else:
                return {"symptoms3": value}
