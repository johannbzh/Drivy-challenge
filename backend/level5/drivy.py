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

def action(who,amount): #Given the entity and the amount, gives back the dictionnary containing the corresponding information
    dico={}
    dico["who"]=who
    if(who=="driver"):
        dico["type"]="debit"
    else:
        dico["type"]="credit"
    dico["amount"]=amount
    return dico
    
def commission(price_with_option,price_without_option,nb_of_day,option_list): #Given the price(with and without the option price) and the duration of the rental, gives the part that goes to each entity + add the amount corresponding to the option
    repartition=[]
    repartition.append(action("driver",price_with_option))
    commission_price=price_without_option*0.3 #Total price of the commission
    total_price_owner=price_without_option-commission_price #Basic amount for the owner
    if("gps" in option_list):
        print("Option GPS")
        total_price_owner+=option_price("gps",nb_of_day) #If the selected option is a gps
    if("baby_seat" in option_type):
        print("Option Baby_seat")
        total_price_owner+=option_price("baby_seat",nb_of_day) #If the selected option is a baby seat
    repartition.append(action("owner",total_price_owner)) #Part that goes to the owner
    repartition.append(action("insurance_fee",commission_price*0.5)) #Part that goes to the assistance
    commission_price*=0.5
    repartition.append(action("insurance_fee",nb_of_day*100)) #Part that goes to the assistance
    commission_price-=nb_of_day*100 #Basic amount for Drivy
    if("additional_insurance" in option_type):
        print("Additional insurance")
        commission_price+=option_price("additional_insurance",nb_of_day) #If the selected option is an additional insurance
    repartition.append(action("drivy_fee",commission_price)) #Rest goes to Drivy
    return repartition

def option_price(type,nb_of_day): #Returns the additional amount of money corresponding to one option for a number of day
    if(type=="gps"):
        print("Prix =",500*nb_of_day)
        return 500*nb_of_day
    if(type=="baby_seat"):
        print("Prix =",200*nb_of_day)
        return 200*nb_of_day
    if(type=="additional_insurance"):
        print("Prix =",1000*nb_of_day)
        return 1000*nb_of_day
    
with open("data/input.json","r") as file:
    data=json.load(file)
    cars=data["cars"]
    rentals=data["rentals"]
    options=data["options"]
    prices=[]
    for rental in rentals: #For each rental
        car_id=rental["car_id"]
        dico={}
        option_type=""
        for car_model in cars: #We look for the information of the corresponding vehicle
            if(car_model["id"]==car_id):
                period=(datetime.datetime.strptime(rental["end_date"],'%Y-%m-%d')-datetime.datetime.strptime(rental["start_date"],'%Y-%m-%d')).days+1 
                rent_price_without_option=0 #Having both prices with and without the option price allows to calculate the correct amount of money for each entity later in he program
                for day in range(period): #To get the corresponding price, according to the duration of the renting
                    rent_price_without_option+=price(day,car_model["price_per_day"])
                rent_price_without_option+=car_model["price_per_km"]*rental["distance"] #We add the distance multiplied by the price per kilometer
        option_list=[]
        rent_price_with_option=rent_price_without_option
        for option in options: #To get the option(s) corresponding to the rental_id
            if(option["rental_id"]==rental["id"]):
                option_type=option["type"]
                rent_price_with_option+=option_price(option_type,period)
                option_list.append(option["type"])
        print("Id :",rental["id"])
        #Writing of the JSON
        dico["id"]=rental["id"]
        dico["options"]=option_list
        dico["actions"]=commission(rent_price_with_option,rent_price_without_option,period,option_list)
        prices.append(dico)
        
    with open("output.json", "w") as write_file:
        output={}
        output["rentals"]=prices
        json.dump(output, write_file,indent=4)
