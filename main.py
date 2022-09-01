import requests
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient


OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = "ACeec9f9ab642e6df2ac8d2c7a8131065c"

api_key = "4856d05830439e769a7291914a8c2206"
auth_token = "4a17a2824bb945692f5bd4716eda5b7d"

weather_params = {
    "lat": -1.189310,
    "lon": 37.11,
    "appid": api_key,
    "exclude":"current,minutely,daily"
}


response = requests.get(OWM_Endpoint,params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data['hourly'][:12]
#print(weather_slice)
will_rain = False
for hour_data in weather_slice:
    condition_code = int(hour_data["weather"][0]['id'])
    if condition_code < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token,http_client=proxy_client)
    message = client.messages \
    .create(body="It's going to rain today bring an umbrella ☂️ ",
            from_="+18593506477",
            to="+254715522758"
            )
    print(message.status)
        #print("Bring an umbrella")
#print(weather_data["hourly"][0]["weather"][0]['id'])


