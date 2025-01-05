# Comcast Bridge Mode

You are ready to make the Netgear RS router your sole router, and switch the Comcast router
to being a "dumb modem". This will disrupt network connectivity for all devices in your home.

Hopefully, just for a few minutes.

## Switch Comcast router to bridge mode

- Connect the Netgear RS router to one of the LAN (local network) ports on the Comcast router.
- Disconnect any other wired connections from the Comcast router - such as your node -
and connect them to one of the LAN (local network) ports on the Netgear RS router. The 2.5G
ones are nice if your node has 2.5G support, and don't hurt if it doesn't.
- Connect to the Comcast router via LAN or WiFi, navigate to `http://10.0.0.1`, and switch
"Bridge Mode" to "Enabled". Comcast has [instructions](https://www.xfinity.com/support/articles/wireless-gateway-enable-disable-bridge-mode)
for this.

In our testing, the Netgear RS router did not receive an external public IP right away.
We power cycled the Comcast router/modem and the Netgear RS, and then it worked.

You can see the external address at Advanced -> Internet Port -> IP Address. Netgear have
[documentation](https://www.netgear.com/hub/technology/what-is-router-ip-address/) for this.

A public IP is any that isn't private: Does not look like `192.168.x.x` or `10.x.x.x` or `172.16.x.x` through
`172.31.x.x`.

## Configure IPv6 on Netgear

Comcast offers IPv6 services in the US, and we'd want that to continue working for you.

On the Netgear web interface, go to Advanced -> Advanced Setup -> IPv6, and set "Internet Connection Type" to "Auto Detect", then click "Apply"

You can verify this worked by coming back to that page and seeing that an IPv6 address has been assigned to the Netgear RS. Your devices on
the network should also show that they have both an IPv4 and an IPv6 address.
