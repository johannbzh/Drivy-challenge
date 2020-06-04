import json
import datetime

def price(day,price_per_day): #Giving the day and the price_per_day, returns the adjusted price_per_day
    if(day>=1):
        if(day>=4):
            if(day>=10):
                return price_per_day*0.5
            else:
                return price_per_day*0.7
        else:
            return price_per_day*0.9
    else:
        return price_per_day
    
with open("data/input.json","r") as file:
    data=json.load(file)
    cars=data["cars"]
    rentals=data["rentals"]
    prices=[]
    for rental in rentals: #For each rental
        car_id=rental["car_id"]
        dico={}
        for car_model in cars: #We look for the information of the corresponding vehicle
            if(car_model["id"]==car_id):
                period=(datetime.datetime.strptime(rental["end_date"],'%Y-%m-%d')-datetime.datetime.strptime(rental["start_date"],'%Y-%m-%d')).days+1
                rent_price=0
                for day in range(period): #To get the corresponding price, according to the duration of the renting
                    rent_price+=price(day,car_model["price_per_day"])
                rent_price+=car_model["price_per_km"]*rental["distance"] #We add the distance multiplied by the price per kilometer
        #Writing of the JSON
        dico["id"]=rental["id"]
        dico["price"]=rent_price

        prices.append(dico)
        
    with open("output.json", "w") as write_file:
        output={}
        output["rentals"]=prices
        json.dump(output, write_file,indent=4)
