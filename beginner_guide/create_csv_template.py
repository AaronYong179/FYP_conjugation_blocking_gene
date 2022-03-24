import csv

f = open("template_csv.csv", "w")
writer = csv.writer(f)

COLUMN_HEADERS = ["Donors",
                  "Recipients",
                  "Plasmids",
                  "Media",
                  "Temperature",
                  "Duration",
                  "C/D",
                  "log(C/D)"]

writer.writerow(COLUMN_HEADERS)
f.close()
