#JSON parsing and creation
"""JSON is a syntax for storing and exchanging data
JSON is text, written with JavaScript object notation
"""
import json
"""if you have a JSON string, you can parse it by using the
json.loads() method"""

# some JSON:
x = '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])

#2
# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)
"""The example above prints a JSON string, but it is not very easy to read, with no indentations and line breaks.

The json.dumps() method has parameters to make it easier to read the result:"""
json.dumps(x, indent=4)

""" You can convert Python objects of the following types, into JSON strings:

dict
list
tuple
string
int
float
True
False
None
"""

import json

with open("sample-data.json", "r") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':60} {'Description':15} {'Speed':10} {'MTU':5}")
print("-" * 80)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]

    dn = attributes["dn"]
    descr = attributes["descr"]
    speed = attributes["speed"]
    mtu = attributes["mtu"]

    print(f"{dn:60} {descr:15} {speed:10} {mtu:5}")