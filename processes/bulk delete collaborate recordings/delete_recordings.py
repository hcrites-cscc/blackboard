import requests, json, datetime, jwt
from urllib.parse import urlencode

def main():
    oAuth = get_token()

    recording_list = open('delete_recordings.txt', 'r')

    for recording in recording_list:
        recording_uuid = recording.strip()
        delete_recordings(recording_uuid, oAuth)

    recording_list.close()

def delete_recordings(recording_uuid, oAuth):
        
    delete = requests.delete(oAuth["endpoint"]+"/recordings/"+recording_uuid,
        headers={"Authorization":"Bearer "+oAuth["token"],
                 "Content-Type":"application/json"
                 }
        )
   
    if delete.status_code != 200:
        if delete.status_code == 404:
           print("Not Found: "+recording_uuid) 
        elif delete.status_code == 401:
           oAuth = get_token()
           delete_recordings(recording_uuid, oAuth)
        else:
           response = json.loads(delete.text)
           print("Error: "+delete.status_code+" "+json.dumps(response,indent=4, separators=(',', ': ')))
    else:
        print("Success: "+recording_uuid)
        


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

