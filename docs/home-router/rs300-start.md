We've tested and documented switching to a Netgear RS300 on Comcast. Any router in the
[Netgear RS line](https://www.netgear.com/home/wifi/routers/listing-filter/ax-wifi7/) should work the same way.

The Netgear routers have a mobile app as well as a web interface. We've documented setting it up via
the web interface from a laptop.

- [App instructions](https://kb.netgear.com/119/How-do-I-set-up-and-install-my-NETGEAR-router)
- [Laptop instructions](https://kb.netgear.com/22697/How-do-I-install-my-NETGEAR-router-using-the-router-web-interface)

Where it says "connect your modem to the yellow Internet port on the back of your NETGEAR router", the
"modem" here is your current ISP router. Use one of its Ethernet LAN, local network, ports, to connect to the "Internet"
port on the Netgear RS.

Netgear will prompt you for an admin password, download a firmware update, and restart. At that
point, you should be able to log in with the new admin password and continue setup.

You may also have the option to set a new WiFi SSID and password. These should be set to the existing SSID
and password from your ISP's router, so that you don't have to reconfigure any devices in your network.

Netgear defaults to an internal `192.168.1.0/24` network. We haven't tested what happens if that also happens to be
the default network of the ISP router. It's possible firmware update will fail, or that you'll need to set up the Netgear router
without Internet connection, and connect it only after the ISP router has been switched to "bridge mode". Firmware
update in that case would happen as the last step, not the first step.
