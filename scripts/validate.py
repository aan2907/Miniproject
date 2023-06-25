import re

#Rules for Indian Vehicles
def rules(reading):
    regcodes=['AP', 'AR', 'AS', 'BR', 'CG', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OD', 'PB', 'RJ', 'SK', 'TN', 'TR', 'UP', 'UK', 'WB', 'TS', 'AN', 'CH', 'DN', 'DD', 'LD', 'DL', 'PY']
    for i in regcodes:
        plate = i + r'\s*\d{1,2}\s*[A-Z]{1,2}\s*\d{1,4}'
        plate=re.compile(plate)
        matchfound=re.findall(plate, reading)
        if matchfound:
            return matchfound[0]

'''
#General Number plate rules
def rules(reading):
    plate = r'\w{1,2}\s*\w{2,3}\s*\w{1,2}'
    plate=re.compile(plate)
    matchfound=re.findall(plate, reading)
    if matchfound:
        return matchfound[0]
'''

def normalise(reading, rulebased=True):
    reading=reading.upper()
    reading = re.sub(r"[ \n\-\.\_]", "", reading)
    if rulebased:
        return rules(reading)
    else:return reading
    
def validate(text):
    plate=normalise(text, rulebased=True)
    if plate:
        return plate
    else: return None

