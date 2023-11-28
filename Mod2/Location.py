import requests
import urllib.parse
import datetime
from twilio.rest import Client

def Location():

    #Get Info
    response = requests.get("https://ipinfo.io")
    
    if response.status_code == 200:
        data = response.json()
       
        city = data.get("city")
        region = data.get("region")
        country = data.get("country")
        location = data.get("loc")
        y = location,[city,region,country]
    else:
        print("Failed to retrieve geolocation information.")

    x = (y[0]).split(',')
    lat = x[0]
    lon = x[1]

    lat_lon = f"{lat},{lon}"
    base_url = "https://www.google.com/maps/search/"
    params = {"api": 1, "query": lat_lon}
    url = base_url + "?" + urllib.parse.urlencode(params)

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    return(url, y[0], y[1], current_time)

def Send_Text():
    content = Location()
    text = (f"""
          EMERGENCY at {content[1]} \n ({content[2][0]}, {content[2][1]}, {content[2][2]})
          \nCar accident on highway with injuries. Need ambulance and police assistance immediately. 
          
          Time of Accident: {content[3]}
          Link To The Location: 
          {content[0]}
          """)
    #Auth And SID
    sid = "AC32d193612554c3838e66a0d927c7b9fb"
    auth = "9ec3883047408abef629fe6d0b362cac"
    client = Client(sid,auth)

    #Messaging Number
    from_no = "+15637702700"
    to_no = "+918618856297"
    
    #Sending Text
    message = client.messages.create(
        body = text,
        from_=from_no,
        to=to_no
    )

if __name__=="__main__":
    Send_Text()