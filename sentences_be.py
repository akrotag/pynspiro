import requests as req
#From http://cubemonkey.net/quotes/
categories = ("miscellaneous", "literature", "people")
resp = req.get("http://subfusion.net/cgi-bin/quote.pl?quote=miscellaneous&number=1")

print(resp.text.split("<br>")[-4].strip())