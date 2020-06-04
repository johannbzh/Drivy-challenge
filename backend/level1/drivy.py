import json
import datetime

with open("data/input.json","r") as file:
    data=json.load(file)
    cars=data["cars"]
    rentals=data["rentals"]
    prices=[]
    
    for rental in rentals: #For each rental
        car_id=rental["car_id"]
        dico={}
        for car_model in cars: #We look for the information of the corresponding vehicle
            if(car_model["id"]==car_id): #We calculate the price
                rent_price=car_model["price_per_day"]*((datetime.datetime.strptime(rental["end_date"],'%Y-%m-%d')-datetime.datetime.strptime(rental["start_date"],'%Y-%m-%d')).days+1)+car_model["price_per_km"]*rental["distance"] 
        dico["id"]=rental["id"]
        dico["price"]=int(rent_price)
        prices.append(dico)
    
    with open("output.json", "w") as write_file:
        output={}
        output["rentals"]=prices
        json.dump(output, write_file,indent=4)
