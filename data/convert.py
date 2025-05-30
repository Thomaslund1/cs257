import csv
import numpy as np

filePath = './games1-1000.csv'
outPath = "./games.csv"

def grabDat(fileLoc):
    out = []
    headers = []
    with open(fileLoc, newline='', encoding='utf8') as data:
        reader = csv.reader(data)
        headers = next(reader, [])
        for row in reader:
            cleaned_row = [cell if cell != '' else '0' for cell in row]
            out.append(cleaned_row)
        out = list(zip(*out))  # Transpose rows and columns
    return out, headers

dat, headers = grabDat(filePath)

# Write transposed data back to CSV
with open(outPath, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(dat)

# ------------------------------
# Mechanics-specific splitting
# ------------------------------
mechanics_index = headers.index("mechanic")  # Index of the mechanics column
game_id_index = 1  # Assuming ID column is at index 1

mechanics_map = {}         # {mechanic_name: id}
game_to_mechanics = []     # [(mechanic_id, game_id)]

for game_idx in range(len(dat[mechanics_index])):
    mechanics_raw = dat[mechanics_index][game_idx]
    game_id = dat[game_id_index][game_idx]

    # Skip if no mechanics
    if not mechanics_raw or mechanics_raw.strip() == '0':
        continue

    # Split by comma, strip whitespace
    mechanic_list = [m.strip() for m in mechanics_raw.split(',') if m.strip()]
    
    for mech in mechanic_list:
        if mech not in mechanics_map:
            mechanics_map[mech] = len(mechanics_map)  # assign new ID

        mechanic_id = mechanics_map[mech]
        game_to_mechanics.append([mechanic_id, game_id])

# Write mechanics table: [mechanic_name, mechanic_id]
with open("mechanics.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for mech, mid in mechanics_map.items():
        writer.writerow([mech, mid])

# Write mapping table: [mechanic_id, game_id]
with open("mechanics_to_game.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(game_to_mechanics)

# ------------------------------
# Process other headers as before (skip mechanics column)
# ------------------------------
for i in range(len(headers)):
    if i == game_id_index or i == mechanics_index:
        continue

    ids = {}
    idsToNames = []

    for j in range(len(dat[i])):
        attr_value = dat[i][j]
        if attr_value not in ids:
            ids[attr_value] = len(ids)
        idsToNames.append([ids[attr_value], dat[game_id_index][j]])

    newIds = [[k, ids[k]] for k in ids]

    if newIds:
        with open(f"./{headers[i]}.csv", 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(newIds)

    if idsToNames:
        with open(f"./{headers[i]}_to_name.csv", 'w', encoding='utf-8', newline='') as g:
            writer = csv.writer(g)
            writer.writerows(idsToNames)

# Optionally, load daterTab.txt (no changes needed here)
with open('./daterTab.txt', 'r') as f:
    dater = [line.strip() for line in f]

# Print headers for debugging
for header in headers:
    print(header)
