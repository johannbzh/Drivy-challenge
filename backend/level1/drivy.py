import json
import datetime

with open("data/input.json","r") as file:
    data=json.load(file)
    cars=data.get("cars")
    rentals=data.get("rentals")
    prices=[]
    
    for i in rentals:
        car_id=i.get("car_id")
        dico={}
        for j in cars:
            if(j.get("id")==car_id):
                price=j.get("price_per_day")*((datetime.datetime.strptime(i.get("end_date"),'%Y-%m-%d')-datetime.datetime.strptime(i.get("start_date"),'%Y-%m-%d')).days+1)+j.get("price_per_km")*i.get("distance") 
        dico["id"]=i.get("id")
        dico["price"]=price
        prices.append(dico)
    
    with open("output.json", "w") as write_file:
        output={}
        output["rentals"]=prices
        json.dump(output, write_file)
