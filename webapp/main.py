#!/usr/bin/python3

# Created by Jared Dunbar

from flask import Flask, request, render_template, Response
from collections import defaultdict
import string, random, pprint

app = Flask(__name__)

data = defaultdict(dict)
datatype = defaultdict(dict)
datacolor = defaultdict(dict)

CACHE_SIZE = 100

@app.route('/')
def index():
    return render_template("index.html", charts=list(data.keys()))

@app.route('/data', methods=["GET", "POST"])
def setdata():
    iunit = request.values.get("unit") # Used to store what kind of data we will be showing,
        # ex, Volts, Watts, Amps, Temperature, Percent. Will override previous value
    iname = request.values.get("name") # Used to store the name of the data we will be storing, to show in the key
    ivalue = request.values.get("value") # Used to store the value of the data
    icolor = request.values.get("color") # Used to set the color of the line in the graph. Will override previous
    iset = request.values.get("set") # Used to put some pieces of data in the same graph (since that may be handy

    # Cast types cleanly
    unit = str(iunit)
    name = str(iname)
    try:
        value = float(ivalue)
    except Exception:
        return "Error, need a float number", 400
    color = str(icolor)
    setname = str(iset)

    unit = unit.strip()
    name = name.strip()
    color = color.strip()
    setname = setname.strip()

    unit = clean(unit)
    name = clean(name)
    color = clean(color)
    setname = clean(setname)

    # Input Checks
    if name == "None" or name == "":
        # Everything needs a name
        return "Error, need a name for the data", 400
    if unit == "None" or unit == "":
        # Everything needs a unit, if not with one, will get percent
        unit = "percent"
    if setname == "None" or setname == "":
        # Everything without a set will be part of the default set
        setname = "default"
    if color == "None" or color == "":
        # These are CSS colors, or 6 character Hex numbers. Not going to check much with these
        color = "Red"
    if unit == "temp":
        unit = "tempc"

    # Valid units are lowercase volt, watt, amp, voltamp, temp, tempc, tempf, tempk, and percent
    # Also accepted are v, w, a, va, c, f, k, p

    # temp will become tempc, automatically.
    # Units will automatically scale depending on the range (ex, Watt, mW, kW, etc.)

    # Append the newest value, set the unit, set the color
    if not data[setname]:
        data[setname] = {}
        data[setname][name] = []
    data[setname][name].append(value)
    datatype[setname] = unit
    datacolor[setname][name] = color

    # Remove the oldest value in the array, if larger than 100 units
    while len(data[setname][name]) > CACHE_SIZE:
        data[setname][name].pop(0)

    # Did everything go to plan? Return OK to the client, to notify them that we think everything went well!
    return "OK"

@app.route('/dump')
def dump():
    pp = pprint.PrettyPrinter(indent=4)
    thing = pp.pformat(data)
    thing2 = pp.pformat(datatype)
    thing3 = pp.pformat(datacolor)
    return "{}, {}, {}".format(thing, thing2, thing3)

@app.route('/update.json')
def update():
    values = ""
    return Response(values, mimetype="application/json")

def clean(inputStr):
    return "".join(
        [c for c in inputStr if c in string.ascii_letters or c in string.whitespace or c in "\\/.,?!|~+=_-[]@#$%^*()"])

def generateSecureKey(size):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

app.secret_key = generateSecureKey(64)

if __name__ == "__main__":
    app.run(debug=True)