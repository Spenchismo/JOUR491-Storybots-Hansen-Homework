import csv

reader = csv.reader(open("drunks.csv", "rU"),dialect=csv.excel)

reader.next()

for row in reader:
    print row[0], "is a real drunk. They drank", row[1], "drinks in one sitting one time."