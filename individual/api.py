import flask as fl
import json


import argparse as arg
import csv

def getParse():
    parser = arg.ArgumentParser(description="Sort the list of games by a given data header")
    parser.add_argument('host',metavar="host",help="which collumn to sort by, as an int")
    parser.add_argument('port',metavar="port",help="which collumn to sort by, as an int",type=int)
    args = parser.parse_args()
    return args

def grabDat():
    fileLoc = '../data/data.csv'
    with open(fileLoc, newline='',encoding='utf8') as data:
        reader = csv.DictReader(data)
        data = list(reader)
    return data

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
    
    return combined

def main():
    args = getParse()
    dat,headers = grabDat(args.dataLocation)
    dat = sortBy(dat,int(args.colNum))
    print(args.colNum)
    print(dat[args.colNum])
    print(dat)

args = getParse()

dat = grabDat()

app = fl.Flask(__name__)

@app.route('/')
def home():
    return("This is a lovely homepage for the flask endpoint assignment of cs257 visit /help for a list of commands")

@app.route('/help')
def help():
    return("Use /search/[paramater]/[value] to search for games in the list that satisfy the condition game[paramater] = value"
    "<br> Ex: /search/name/Terraforming Mars")

@app.route('/search/<param>/<value>')
def serach(param,value):
    out = []
    value = value.replace("%20"," ")
    param = param.replace("%20"," ")
    try:
        for i in dat:
            if i[param]==value:
                out.append(i)
    except KeyError:
        return "No such header found, check spelling"
    if(len(out) > 0):
        return json.dumps(out,indent=2)
    return("No games returned for that search term")

app.run(host=args.host, port=args.port, debug=True)