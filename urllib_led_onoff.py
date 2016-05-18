from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urlencode

params = urlencode({
    'switch': "off",
})

header={'CustomHeader': 'CustomValue'}
req = Request(url='http://127.0.0.1:3000/api/sensors/573ad01b4ef7764f19dbad3f', headers=header, method='PUT')
res = urlopen(req, params.encode('utf8'), timeout=5)
#res = urlopen(req, timeout=5)

print(res)
print(res.status, res.reason)

exit(0)