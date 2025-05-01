import httpx, requests
from pydantic import BaseModel
from typing import List
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url1 = "http://api.nobelprize.org/v1/laureate.json"
response = requests.get(url1)
# response.raise_for_status()
winners = response.json()["laureates"]
# print(type(winners))
# print(winners["laureates"][0])


url2 = "http://api.nobelprize.org/v1/country.json"
response = requests.get(url2)
# response.raise_for_status()
countries = response.json()["countries"]
# print(countries)
# print(data["countries"][0])
# {'name': 'Algeria', 'code': 'DZ'}

class Output(BaseModel):
    id: int
    name: str
    dob: str
    unique_prize_years: str
    unique_prize_categories: str
    gender: str
    bornCountryCode: str

def create_data(winners, countries) -> List[Output]:
    final = []

    for winner in winners:
        try:
            id = winner["id"]
        except KeyError as e:
            # logger.error("Key Error")
            continue

        try:
            firstname = winner["firstname"]
            surname = winner["surname"]
            if surname == '':
                name = firstname
            else:
                name = f"{firstname} {surname}"
        except KeyError as e:
            # logger.error("Key Error")
            firstname = ''
            surname = ''
            
        try:
            dob = winner["born"]
        except KeyError as e:
            # logger.error("Key Error")
            dob = ''

        unique_prize_years = ""
        years = []
        for i in winner["prizes"]:
            try: 
                year = int(i["year"])
                if year not in years:
                    unique_prize_years += str(year) + " ; "
                    years.append(year)
            except KeyError as e:
                # logger.error("Key Error")
                years = ''
            
        if len(years) > 1:
            print(id, years, unique_prize_years)

        unique_prize_categories = ""
        prizes = []
        for i in winner["prizes"]:
            try:
                prize = i["category"]
                if prize not in prizes:
                    unique_prize_categories += prize + " ; "
                    prizes.append(prize)
            except:
                # logger.error("Key Error")
                prize = ''
        
        if len(prizes) > 1:
            print(id, prizes)

        # print(len(winner["prizes"]))


        try:
            gender = winner["gender"]
        except KeyError as e:
            # logger.error("Key Error")
            gender = ''

        bornCountryCode = ""
        for country in countries:
            try:
                if country["code"] == winner["bornCountryCode"]:
                    bornCountryCode = country["name"]
                    break
            except KeyError as e:
                # logger.error("Key Error")
                bornCountryCode = 'Empty'
        

            
        final.append(Output(
            id=id,
            name=name,
            dob=dob,
            unique_prize_years=unique_prize_years[:len(unique_prize_years)-3],
            unique_prize_categories=unique_prize_categories[:len(unique_prize_categories)-3],
            gender=gender,
            bornCountryCode=bornCountryCode
        ))

    return final

result = create_data(countries=countries, winners=winners)
# print(result)

# print([item.model_dump() for item in result][0])
df = pd.DataFrame([item.model_dump() for item in result])
df.to_csv("noble_winners.csv", index=False)

# Some keys are missing in the data, I handled them properly. This code can be more organized in classes and functions. And more proper handling could be done. And I could have store this on CSV from Internet, but due to time constraint I didn't. 
# And I will explore pandas options very soon. Thank you sir. :)