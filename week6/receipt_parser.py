import re
import csv
file = open("raw.txt", "r", encoding="utf8")
text = file.read()
pattern = r"\n(?P<order>[0-9]+)\.\n(?P<name>.+)\n(?P<count>.+)x(?P<price>.+)\n"
results = re.finditer(pattern, text)

with open('data.csv', "w", newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['order', 'name', 'count', 'price'])
    for x in results:
        writer.writerow([
            x.group('order'),
            x.group('name'),
            float(x.group('count').strip().replace(',', '.')),

            float(x.group('price').strip().replace(',', '.').replace(' ', ''))
        ])




#[a-z]+.?[\w]+.?@[a-z]+.[a-z]+