-- Written by Jared Dunbar
-- Configuration

-- Force TCP mode (for debugging, will try HTTP otherwise)
use_tcp = false

--
-- File Format:
--
-- location - the IP address or hostname of the server
-- inputSide - the side from which you want to gather the data on the probe. Valid sides are XP, XN, YP, YN, ZP, ZN
-- set - the set graph this is a member of
-- name - the name of the datapoints
-- unit - the unit of the measurement. v, w, a, va, c, f, k, p are all accepted (see the webapp for detals)
-- color - the color of the data set, in RRGGBB format

component = require("component")

probes = {}
inter = {}

i = 0
j = 0

for k,v in component.list() do
    if v == "ElnProbe" then
        print("Found an Eln Probe: " .. k)
        probes[i] = k
        i = i + 1
    end
end

for k,v in component.list() do
    if v == "internet" then
        print("Found an internet card: " .. k)
        inter[j] = k
        j = j + 1
    end
end

probe = component.proxy(component.get(probes[0]))
internet = component.proxy(component.get(inter[0]))

configFile = io.open("ps.txt", "r")

location = configFile:read("*l")
inputSide = configFile:read("*l")
set = configFile:read("*l")
name = configFile:read("*l")
unit = configFile:read("*l")
color = configFile:read("*l")

if internet.isHttpEnabled() or internet.isTcpEnabled() then
    print("We are permitted access to the internet")
else
    print("We are not able to connect to the internet. Please contact your server administrator, or check your OpenComputers configuration file")
    os.exit(1)
end

if not internet.isHttpEnabled() then
    print("HTTP is not enabled on the server, falling back to TCP mode")
    use_tcp = true
end

if not internet.isTCPEnabled() then
    print("TCP is not enabled on the server, falling back to HTTP mode")
    use_tcp = false
end

if use_tcp then
    while 1 do
        sendDataTCP(location, inputSide, set, name, unit, color, probe, internet)
    end
else
    while 1 do
        sendDataHTTP(location, inputSide, set, name, unit, color, probe, internet)
    end
end


function sendDataHTTP(location, inputSide, set, name, unit, color, probe, internet)
    val = probe.signalGetIn(inputSide)

    conn = internet.request("http://" .. location .. "/data?" .. generateParameters(name, set, unit, color, val))
    conn.finishConnect()
    conn.close()
    return 0
end

function sendDataTCP(location, inputSide, set, name, unit, color, probe, internet)
    val = probe.signalGetIn(inputSide)
    conn = internet.connect(location, 80)
    conn.finishConnect()
    -- for the time being, it appears that POST requests are broken with the webserver??
    conn.write("GET /data?" .. generateParameters(name, set, unit, color, val) .. " HTTP/1.1\r\n")
    conn.close()
    return 0
end

function generateParameters(name, set, unit, color, val)
    return "name=" .. name .. "&set=" .. set .. "&unit=" .. unit .. "&color=" .. color .. "&value=" .. val
end