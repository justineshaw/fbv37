from bs4 import BeautifulSoup # webscraper
import urllib.parse
from urllib.parse import urlparse

iframe = '<iframe src="https://www.facebook.com/ads/api/preview_iframe.php?d=AQI2dwUikeeQZnPfk_MkorI5-zjDzZD3NO_gx5b1u0tQ4JPtcgcCMKq_bV_O8h9IVUO9wrYCuOrcjsUS4jcrfKjhb6eTX981-VIgGT8mv1WAXI30sFnpmbalgquQs3hl9u8oyrbz4ezw55RXCtmYLOQAWQv4MpOlhqpmxfK1iqpVKXTc5fubG-18kHF35j9jjdlsSssUYrJQygzKuNnT42XX5kR71-WHyY91XsksUBk_0w6ytOKNZpyj6w_Aa_YZrXm34vlRsaKGQ3jxAjqRxfrR1uiUC6G8cyDrUzzAPzUVJGuDYUKQ18ji-_inTnD0v-Y-p2qgrsfGbeHlBnR7Qrs4eqDIRR6B08d7KE1OSuUYGMNuscKkEzka3yH_AlDZ8R4&amp;t=AQIpm8YjILghbv-q" width="335" height="450" scrolling="yes" style="border: none;"></iframe>'
soup = BeautifulSoup(iframe, 'html5lib')
print(iframe)
print(soup)
iframe = soup.find_all('iframe')[0]['src']
print(iframe)

'''
# Below is leadgen_id sample data
data = {
  "created_time": "2019-03-23T12:06:03+0000",
  "id": "2539358159470235",
  "field_data": [
    {
      "name": "email",
      "values": [
        "test@fb.com"
       ]
    },
    {
      "name": "full_name",
      "values": [
        "<test lead: dummy data for full_name>"
      ]
    }
  ]
}

print(data['created_time'])
print(data['id'])
for field_data in data["field_data"]:
    if field_data["name"]=='email':
        email = field_data["values"][0]
        print(email)
    elif field_data["name"] == 'full_name':
        full_name = field_data["values"][0]
        print(full_name)

# End leagden_id sample data

'''
'''


# Below is sample data for a real-time webhook ping when for a new inbound lead

data = {
    'entry': [{
        'changes': [{
            'field': 'leadgen', 'value': {
                'created_time': 1553339786, 'page_id': '1775351279446344', 'form_id': '2537788056293912', 'leadgen_id': '2539285652810819'
            }
        }],
        'id': '1775351279446344', 'time': 1553339787
    }],
    'object': 'page'
}

var = data
#print(data)
# print(var['entry'][0]['changes'][0]['value']['leadgen_id'])

if data["object"] == "page": # make sure incoming ping is from a page

    for entry in data["entry"]: # account for more than one lead at a time
        page_id = entry['id']

        for lead_event in entry["changes"]:
            print( 'page_id: ' + page_id )
            leadform = lead_event['value']['form_id']
            print('leadform: ' + leadform)
            newlead = lead_event['value']['leadgen_id']
            print('newlead: ' + newlead)

# End sample data for a real-time webhook ping when for a new inbound lead
'''
