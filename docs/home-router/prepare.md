Gather some information about your current network, so you are prepared for the change.

- Verify your ISP supports bridge mode, and find out how to enable it
- Document your current setup
    - WiFi SSID(s) and their passwords
    - Internal ("LAN") network address, e.g. `10.1.0.0/24` or `192.168.1.0/24`
    - DHCP settings, specifically any "DHCP reservation" settins. Your node likely has one,
a gaming console may as well
    - Do you have any devices with a static IP? Your node might use a static IP, instead
of a DHCP reservation.
    - Port forwarding settings. Your node likely has some, gaming consoles may as well. This
may be in an app, not configurable via your ISP router's web interface
    - Is IPv6 configured? Note down anything that doesn't look like "default" settings
- Verify you have logins to everything you need
    - Your ISP's website
    - Your ISP router's web interface, if any
    - Your ISP's app, if any
    - Your new router's web interface
- Make a plan
    - Are you going to keep your current LAN network address?
        - Pro: Any static IPs can remain as-is
        - Con: You'd need to set up your new router isolated, so it doesn't conflict with
the existing network during initial setup
        - Ethstaker have documented not keeping the current LAN network address, and relying
on DHCP reservation
    - Read through the documentation and ensure you are comfortable, before you take the
final step of activating your new router, and switching your ISP router to "bridge mode"

On the left, you'll find navigation for router setup and final switchover.
