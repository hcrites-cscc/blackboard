import requests, json, datetime, jwt
from urllib.parse import urlencode

def main():
    oAuth = get_token()

    start_date = datetime.datetime(2021, 5, 4)
    end_date = datetime.datetime(2021, 5, 11)

    while start_date <= end_date:
        date_range = start_date+datetime.timedelta(hours = 24)  
        get_recordings(start_date.isoformat(), date_range.isoformat(), 1000, oAuth)
        start_date += datetime.timedelta(hours = 24)


def get_recordings(start_time, end_time, limit, oAuth):
    recordings_data = {
        "startTime": start_time,
        "endTime": end_time,
        "limit": 1000
        }
    
    rest = requests.get(oAuth["endpoint"]+"/recordings?"+urlencode(recordings_data),
        headers={"Authorization":"Bearer "+oAuth["token"],
                 "Content-Type":"application/json"
                 }
        )
   
    if rest.text:
        response = json.loads(rest.text)
        recording_list = response["results"]
        for recording in recording_list:
            try:
                start_date = datetime.datetime.strptime(recording["startTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
                start_date_text = start_date.strftime("%m/%d/%Y %H:%M:%S")
            except KeyError:
                start_date_text = start_time+" (not found)"
            print(recording["id"]+"\t"+recording["name"].encode('unicode-escape').decode('utf-8')+"\t"+start_date_text, end="")
            if recording["publicLinkAllowed"] == False:
                print("\tnot public")
            else:
                print("\tpublic")

def get_token():
    oAuth = {
        "key" : "[your_lti_key]",
        "secret" : "[your_lti_secret]",
        "endpoint" : "https://us.bbcollab.com/collab/api/csa"
    }

    grant_type = "urn:ietf:params:oauth:grant-type:jwt-bearer"

    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes = 5)

    claims = {
        "iss" : oAuth["key"] ,
        "sub" : oAuth["key"] ,
        "exp" : exp 
    }
        
    assertion = jwt.encode(claims, oAuth["secret"], "HS256")
    
    payload = {
        "grant_type": grant_type,
        "assertion" : assertion
    }

    rest = requests.post(
        oAuth["endpoint"]+"/token",
        data = payload,
        auth = (oAuth["key"], oAuth["secret"])
        )

    #print("[auth:setToken()] STATUS CODE: " + str(rest.status_code) )

    res = json.loads(rest.text)
    #print("[auth:setToken()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(",", ": ")))

    if rest.status_code == 200:
        parsed_json = json.loads(rest.text)
        oAuth["token"] = parsed_json['access_token']
        oAuth["token_expires"] = parsed_json['expires_in']

    else:
        print("[auth:setToken()] ERROR: " + str(rest))
        
  
    return oAuth

main()

