# This module interfaces with Isabel's API

import urllib.request
import urllib.parse
import json
import datetime

isabelauth = '3awn4q66XJ5OFhTV9Z8O4fCE06hmMuV8'


def getSymptomsList():
    with urllib.request.urlopen("https://apiscsandbox.isabelhealthcare.com/predictive-text") as url:
        data = json.loads(url.read().decode())
        return data['predictive_text']


def getCountry_id(country):
    with urllib.request.urlopen(f"https://apiscsandbox.isabelhealthcare.com/v2/countries?"
                                f"language=english&web_service=json&callback=countries&"
                                f"authorization={isabelauth}") as url:
        dataString = url.read().decode()
        dataSubstring = dataString[dataString.find("(") + 1:-2]
        data = json.loads(dataSubstring)

        return list(filter(lambda x:x['country_name'].lower() == country.lower(), data['countries']['country']))[0]['country_id']


def getDiagnostic(birthdate, sex, pregnancy, country, symptoms):
    with urllib.request.urlopen(f"https://apiscsandbox.isabelhealthcare.com/v2/ranked_differential_diagnoses?"
                                f"specialties=28&"
                                f"dob={(birthdate[0:10].replace('-',''))}&"
                                f"sex={sex}&"
                                f"pregnant={pregnancy}&"
                                f"country_id={getCountry_id(country)}&"
                                f"querytext={(symptoms.replace(' ','%20'))}&"
                                f"suggest=Suggest+Differential+Diagnosis&"
                                f"flag=sortbyRW_advanced&searchType=0&"
                                f"web_service=json&"
                                f"callback=diagnosisCallback&"
                                f"authorization={isabelauth}") as url:
        dataString = url.read().decode()
        dataSubstring = dataString[dataString.find("(")+1:-2]
        data = json.loads(dataSubstring)
        # print(data)
        returnvalue = 'The first diagnoses is ' + data['diagnoses_checklist']['diagnoses'][0]['diagnosis_name']
        returnvalue += '.  \nLearn more here ' + data['diagnoses_checklist']['diagnoses'][0]['knowledge_window_url'].replace(' ','%20')
        returnvalue += '.  \n\nThe second diagnoses is ' + data['diagnoses_checklist']['diagnoses'][1]['diagnosis_name']
        returnvalue += '.  \nLearn more here ' + data['diagnoses_checklist']['diagnoses'][1]['knowledge_window_url'].replace(' ','%20')

        return returnvalue
