import re

def valid(reading):
  regcodes=['ap', 'ar', 'as', 'br', 'cg', 'ga', 'gj', 'hr', 'hp', 'jk', 'jh', 'ka', 'kl', 'mp', 'mh', 'mn', 'ml', 'mz', 'nl', 'od', 'pb', 'rj', 'sk', 'tn', 'tr', 'up', 'uk', 'wb', 'ts', 'an', 'ch', 'dn', 'dd', 'ld', 'dl', 'py']
  for i in regcodes:
    plate = i + r'\s*\d{2}\s*[a-z]{1-2}\s*\d{1-4}'
    plate=re.compile(plate)
    matchfound=re.fullmatch(plate, reading.lower())
    if matchfound:
      return matchfound

test = "py34 nh 3209"

print(valid(test))
