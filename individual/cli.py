'''
cli.py 
Thomas Lund
16-Apr-2025

NAME: cli.py - command-line interface
SYNOPSIS: cli.py {filepath to csv} {collumn to sort by: int}
DESCRIPTOPM: Prints the sorted collumn, then the entire array sorted by the given collumn. With no libraries this makes quite a mess of a print
data format: headers = ['author','pageNumber'] dat = [['kant','keats','pound'],['550','475','80']] etc
'''
import argparse as arg
import csv

def getParse():
    parser = arg.ArgumentParser(description="Sort the list of games by a given data header")
    parser.add_argument('dataLocation',metavar="file path",help="Where the data is as a csv file")
    parser.add_argument('colNum',metavar="Collumn number",help="which collumn to sort by, as an int",type=int)
    args = parser.parse_args()
    return args

def grabDat(fileLoc):
    out = []
    headers = []
    fileLoc = './data.csv'
    with open(fileLoc, newline='',encoding='utf8') as data:
        reader = csv.reader(data)
        isFirst = 1
        isSecond = 0
        for row in reader:
            if isSecond:
                for i in row:
                    out.append([i])
                isSecond=0
            if isFirst:
                for i in row:
                    headers.append(i)
                isFirst = 0
                isSecond = 1
            else:
                for ind,i in enumerate(row):
                    out[ind].append(i)
    return out

def sortBy(dat,collumn):
    dat[0],dat[collumn] = dat[collumn],dat[0]
    try:
        dat[0] = [int(i) for i in dat[0]]
    except:
        pass
    combined = list(zip(*dat))
    combined.sort()
    combined = list(zip(*combined))
    combined[0],combined[collumn] = combined[collumn],combined[0]
    print(combined[collumn])
    return combined

def main():
    args = getParse()
    dat = grabDat(args.dataLocation)
    dat = sortBy(dat,int(args.colNum))
    print(args.colNum)
    print(dat)

main()
