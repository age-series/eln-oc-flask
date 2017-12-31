# Eln OC Flask App

This flask app is designed to be able to visualize Electrical Age power networks with assitance from a OpenComputers or ComputerCraft lua tie-in.

## Structure

In game - one needs to have an Electrical Age signal cable coming from the thing they would like to monitor. This cable then goes to the Electrical Age Computer Probe, and that needs to be connected to the computer. That computer then runs the powerserver.lua program in the oc-lua folder of this repository. That program takes in a few parameters (such as what it is measuring, range, what grouping of data you want it to show with, colors, etc). This then sends HTTP requests to the flask app running on the server.

On the server - This does not need to necessarily run on the same computer the actual server runs on, meaning to use this program you don't have to be the minecraft server's administrator. This server runs the flask app, which has to be fully accesssible (no firewall) to the Minecraft server for incoming TCP traffic, and established connections.

## A note to Minecraft Server Administrators

### OpenComputers Config Changes

For this to work, you need to have ```enableHttp``` flag set to ```true```, as well as the computer with the flask server not being in the blacklist (or being contained in the whitelist). The rest of the config below doesn't really affect the program.

Please remember that this allows anyone on the server to query TCP ports on any IP if you use less restrictive settings. This means that hypothetically, a user can use a HTTP request through your server to any other server. Not really DoS attacks, but it can technically try a slow brute force attack against any computer. If you modify the blacklist to not include local IP addresses, it can also break into things on your local network, so be cautious.

If your server is whitelisted, and you trust your friends, this is probably less of a problem.

Sample from the OpenComputers configuration file:

```conf
  # Internet settings, security related.
  internet {
    # Whether to allow HTTP requests via internet cards. When enabled,
    # the `request` method on internet card components becomes available.
    enableHttp: true

    # Whether to allow adding custom headers to HTTP requests.
    enableHttpHeaders: true

    # Whether to allow TCP connections via internet cards. When enabled,
    # the `connect` method on internet card components becomes available.
    enableTcp: true

    # This is a list of blacklisted domain names. If an HTTP request is made
    # or a socket connection is opened the target address will be compared
    # to the addresses / adress ranges in this list. It it is present in this
    # list, the request will be denied.
    # Entries are either domain names (www.example.com) or IP addresses in
    # string format (10.0.0.3), optionally in CIDR notation to make it easier
    # to define address ranges (1.0.0.0/8). Domains are resolved to their
    # actual IP once on startup, future requests are resolved and compared
    # to the resolved addresses.
    # By default all local addresses are blocked. This is only meant as a
    # thin layer of security, to avoid average users hosting a game on their
    # local machine having players access services in their local network.
    # Server hosters are expected to configure their network outside of the
    # mod's context in an appropriate manner, e.g. using a system firewall.
    blacklist: [
      "127.0.0.0/8"
      "10.0.0.0/8"
      "192.168.0.0/16"
      "172.16.0.0/12"
    ]

    # This is a list of whitelisted domain names. Requests may only be made
    # to addresses that are present in this list. If this list is empty,
    # requests may be made to all addresses not blacklisted. Note that the
    # blacklist is always applied, so if an entry is present in both the
    # whitelist and the blacklist, the blacklist will win.
    # Entries are of the same format as in the blacklist. Examples:
    # "gist.github.com", "www.pastebin.com"
    whitelist: []

    # The time in seconds to wait for a response to a request before timing
    # out and returning an error message. If this is zero (the default) the
    # request will never time out.
    requestTimeout: 0

    # The maximum concurrent TCP connections *each* internet card can have
    # open at a time.
    maxTcpConnections: 4

    # The number of threads used for processing host name lookups and HTTP
    # requests in the background. The more there are, the more concurrent
    # connections can potentially be opened by computers, and the less likely
    # they are to delay each other.
    threads: 4
}
```