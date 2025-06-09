import csv

with open('./data/game.csv', 'r') as infile, open('./data/game_cleaned.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for row in reader:
        row = [field if field.strip() != '' else 'NULL' for field in row]
        writer.writerow(row)
