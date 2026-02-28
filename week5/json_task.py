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