import re

def validate(reading):
    regcodes=['ap', 'ar', 'as', 'br', 'cg', 'ga', 'gj', 'hr', 'hp', 'jk', 'jh', 'ka', 'kl', 'mp', 'mh', 'mn', 'ml', 'mz', 'nl', 'od', 'pb', 'rj', 'sk', 'tn', 'tr', 'up', 'uk', 'wb', 'ts', 'an', 'ch', 'dn', 'dd', 'ld', 'dl', 'py']
    reading=reading.upper()
    reading = re.sub(r"[ \n\-\.]", "", reading)
    for i in regcodes:
        plate = i + r'\s*\d{1,2}\s*[a-z]{1,2}\s*\d{1,4}'
        plate=re.compile(plate)
        matchfound=re.fullmatch(plate, reading.lower())
        if matchfound:
            return reading

test = "KL 01-Bk \n1001"
print(validate(test))

