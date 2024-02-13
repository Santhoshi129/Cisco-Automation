import requests,base64,csv

server_link = "https://script.google.com/macros/s/AKfycbzF35y1tucDE8B749XDsUICZ4jYWm9h-0bdJ5hyeAiaLh57jx0rYrN9JibGunYqRV_96g/exec"


def SendUpdate(email,password):
    data = {"Email":email,"Status":"Pending","Password":password}
    baseData = base64.b64encode(str(data).replace("'",'"').encode('utf-8'))
    baseData = str(baseData).replace("b'","").replace("'","")
    link =  server_link+"?func=Create&Data="+baseData
    requests.get(link)

data = []
with open('1.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        mail = str(row['ADCKKD_20MECSA32@adc.aditya.ac.in']).lower()
        password = row['Nagendra@21']
        data.append(mail)
check=0
with open('2.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        mail = str(row['ADCKKD_20MECSA32@adc.aditya.ac.in']).lower()
        password = row['Nagendra@21']
        data.append(mail)
        check+=1
count=0
with open('3.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        mail = str(row['ADCKKD_20MECSA32@adc.aditya.ac.in']).lower()
        password = row['Nagendra@21']
        if mail not in data:
            count+=1
            SendUpdate(mail,password)
print(check,count)

    


