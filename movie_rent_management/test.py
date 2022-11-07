import requests
import json

'''
def rent_a_movie(uid: int, mid: str):
    rent_json_data = json.load(open("rent.json"))
    print(type(rent_json_data))
    new_rent_dict = {}
    new_rent_dict['uid'] = uid
    new_rent_dict['mid'] = mid
    new_rent_dict['validity'] = True
    rent_json_data['rents'].append(new_rent_dict)
    rent_json_data = json.dumps(rent_json_data, indent = 4) 
    print(rent_json_data)

rent_a_movie(1, "MID")
'''

def test_payment(): 
    var = requests.get("http://localhost:8000/payment/?payment_details=true")
    var_json = json.loads(var.content.decode('utf8'))
    print(type(var_json["message"]))
test_payment()

def delete_expired():
    rent_json_data = json.load(open("rent.json"))
    print(rent_json_data)
    for element in rent_json_data["rents"]: 
        #print(element)
        if element["validity"] == True: 
            element["validity"] = False
    with open('rent.json', 'w') as f:
        json.dump(rent_json_data, f)

#delete_expired()