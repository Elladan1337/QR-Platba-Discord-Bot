import requests

url = "http://api.paylibo.com/paylibo/generator/czech/image"
params = {
	'accountPrefix':'51',
	'accountNumber':'9056360217',
	'bankCode':'0100',
	'amount':600,
	'currency':'CZK',
	'vs':'',
	'ks':'',
	'ss':'',
	'identifier':'',
	'date':'2023-01-01',
	'message':'pozdravy od Jáchyma',
	'compress':False,
	'branding':False,
	'size':400
}
print(params)
response = requests.get(url = url, params = params, stream=True)
print(response.status_code)
if response.status_code == 200:
	with open('img.png', 'wb') as out_file:
		out_file.write(response.content)