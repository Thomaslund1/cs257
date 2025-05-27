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
        print(headers)  # Check headers
        for i in reader:
            subl = []
            for j in i:
                if j == '':
                    j = 0  # Replace empty cells with 0
                subl.append(j)
            out.append(subl)
        # Transpose data (you can use zip instead of np.array)
        out = list(zip(*out))  # Transpose rows and columns
    return out, headers

dat, headers = grabDat(filePath)

# Writing the transposed data back to a CSV
with open(outPath, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(dat)  # Writing transposed data (columns as rows)

# Example: Create IDs for a specific column (e.g., i=1)
i = 1
idsNames = {}
for j in range(len(dat[i])):
    if(dat[i][j] not in idsNames):
        idsNames[dat[i][j]] = {'id': len(idsNames)}

newIds = [[k, idsNames[k]['id']] for k in idsNames]

# Writing the newIds to a CSV
with open(f"./{headers[i]}.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(newIds)

# Process additional headers
for i in range(len(headers)):
    if i == 1:  # Skip index 1
        continue

    ids = {}
    idsToNames = []
    for j in range(len(dat[i])):
        if(dat[i][j] not in ids):
            ids[dat[i][j]] = {'id': len(ids)}
        idsToNames.append([ids[dat[i][j]]['id'], idsNames[dat[1][j]]['id']])

    newIds = [[k, ids[k]['id']] for k in ids]

    if newIds:
        with open(f"./{headers[i]}.csv", 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(newIds)

    if idsToNames:
        with open(f"./{headers[i]}_to_name.csv", 'w', encoding='utf-8', newline='') as g:
            writer = csv.writer(g)
            writer.writerows(idsToNames)

# Reading daterTab.txt correctly
dater = []
with open('./daterTab.txt', 'r') as f:
    dater = [line.strip() for line in f]  # Strip newline characters

# Print headers for debugging
for header in headers:
    print(header)
