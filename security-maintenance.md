# Guide on how to do security and maintenance for an Ethereum validator's machine

Your staking machine is as unsafe as many others, but we can help it. Just like with many things in life, you are consistently being exposed to risks you might not even know about. You can spend a very large amount of time, efforts and money and still be exposed to many risks. The rabbit hole runs deep. This guide is a first plunge into the world of security and maintenance to give you a foundation for your own Ethereum validator's machine.

The following suggestions are general tips that can apply to many different environments and use cases. Security can be subjective. What feels safe or safer for someone can be quite different from someone else. As you start looking at these risks from different angles, you may find alternative solutions that have their own pros and cons.

This is not an exhaustive list of all the security practices someone who runs a validator or who handles cryptocurrencies should use. We have [a reference section with additional security practices](#good-security-and-maintenance-references) you should be looking at as well.

## Using a good operating system

**Risks**

* Using an operating system that is hard to secure or hard to maintain.
* Using an operating system that has poor default configuration values.
* Using an operating system that has weak support or that has a weak community.
* Using an operating system that exposes you to unnecessary risks.

If you do not know which operating system (OS) to use for your staking machine, use [Ubuntu 22.04 Desktop](https://ubuntu.com/download/desktop). If you are familiar with the command line interface (CLI) and manually typing commands in a terminal, I suggest you use [Ubuntu 22.04 Server](https://ubuntu.com/download/server). Ubuntu 22.04 is [a long term support (LTS) release](https://ubuntu.com/blog/what-is-an-ubuntu-lts-release). It will be supported until 2032 which gives you a peace of mind.

While you can use MacOS or Windows to run your staking machine, I would recommend against it. They will expose you to additional risks and they are harder to manage in terms of security and general maintenance.

There are various other good Linux distributions that can work, but the rest of this guide will assume you are using Ubuntu 22.04. If you know what you are doing and you are familiar with Linux, you should still be able to follow even if you used another modern Linux distribution.

Installing a modern Linux operating system on your own machine is often as simple as:

1. Downloading the OS image.
2. Copying the OS image on a USB drive and making it bootable. [Rufus](https://rufus.ie/en/) or [Etcher](https://www.balena.io/etcher/) are two good tools to accomplish this.
3. Plugging in that USB drive, rebooting your machine and booting your machine from that USB drive. That last part can be somewhat tricky depending on your boot sequence and your motherboard. On many modern PC, you can press and hold the `F2` key on your keyboard after a reboot to enter your [BIOS](https://en.wikipedia.org/wiki/BIOS). From there, you can select on which device or drive to boot from or you can change the boot sequence order. On Mac, you can press and hold the *Option* (`⌥`) key immediately upon hearing the startup chime to enter the Startup Manager and select which device or drive to boot from. In case of doubts, refer to your machine manual, your motherboard manual or get in touch with [the ETHStaker community](#support).

## Using a dedicated machine

**Risks**

* Exposing your machine to unrelated *daily usage* risks.
* Starving your staking machine resources.
* Unexpected or inopportune machine reboots.

## Securing your remote access

**Risks**

* Unauthorized or unintended remote access to your machine.

If you are using SSH to remotely access your machine, you should [configure your server to authenticate with keys and disable password authentication](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server).

## Securing your network with a firewall

**Risks**

* Unauthorized or unintended remote access to your machine.

## Securing the machine you use to remote connect with

**Risks**

* Unauthorized or unintended remote access to your machine.

## Performing your system updates regularly

## Performing your application updates regularly

## Using a live patching service

**Risks**

* Using a kernel that has vulnerabilities between updates or reboots.
* Missing important staking rewards during reboots.

Ubuntu and Canonical offers a live patching service called [Livepatch](https://ubuntu.com/security/livepatch) which is free for up to 3 machines.

## Limiting the installed applications and running processes

## Limiting the users who can access your machine

## Using disk encryption

**Risks**

* Physical data theft
* Unintended slashing

## Good security and maintenance references

* [Protecting Yourself and Your Funds](https://support.mycrypto.com/staying-safe/protecting-yourself-and-your-funds) by [Jennicide](https://twitter.com/Jennicide) and [MyCrypto](https://mycrypto.com/).
* [Security Best Practices for a ETH staking validator node](https://www.coincashew.com/coins/overview-eth/guide-or-security-best-practices-for-a-eth2-validator-beaconchain-node) by [CoinCashew](https://www.coincashew.com/).
* [Ethereum 2.0 Node Security Discussion](https://youtu.be/hHtvCGlPz-o) by [CryptoManufaktur](https://www.cryptomanufaktur.io/).
* [MyCrypto’s Security Guide For Dummies And Smart People Too](https://blog.mycrypto.com/mycrypto-s-security-guide-for-dummies-and-smart-people-too) by [MyCrypto](https://mycrypto.com/).
* [Guide: Crypto Wallet Tips 101 - Do's and Don'ts](https://www.coincashew.com/wallets/guide-wallet-tips-101-dos-and-donts) by [CoinCashew](https://www.coincashew.com/).

## Support

If you have any question or if you need additional support, make sure to get in touch with the ETHStaker community on:

* Discord: [dsc.gg/ethstaker](https://dsc.gg/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)
