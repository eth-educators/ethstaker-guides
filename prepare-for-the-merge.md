# Guide on how to prepare a staking machine for the Merge

[The Merge](https://ethereum.org/en/upgrades/merge/) is a protocol upgrade that is being rolled out on all Ethereum networks being kept around. This procotol upgrade will be rolled out on mainnet and Ethereum validators will need to take some measures and some actions to make sure their staking machine will work during this upgrade and that they will keep running well after the upgrade. Tests are already underway and [the Merge upgrade has been applied to testnets](https://wenmerge.com/) already.

This guide is meant for people who are managing and maintaining staking machines. It will explain which steps or actions you should take in order to be ready for the Merge.

## Why would you want to prepare for the Merge?

There are some risks your staking machine will stop performing its duties if you are not well prepared. There are some risks your Ethereum validator will miss some rewards if you are not well prepared.

## When is the Merge going to happen on Mainnet?

The current planned date for the Merge protocol upgrade to happen is ~Q3/Q4 2022. There is some uncertainty around the actual date it will happen. Make sure to follow [the official Ethereum blog](https://blog.ethereum.org/) and watch for announcements there.

## Overview

1. Make sure you are running your own execution client.
2. Make sure your Ethereum clients are updated.
3. Make sure you are using the new configuration options for your Ethereum clients.
4. Make sure you have a configured JWT token file for the engine API.
5. Make sure you have a configured fee recipient address.
6. Make sure you have a configured MEV solution if you want one.

## Running your own execution client

Running your own execution client is going to be required after the Merge for an Ethereum validator. Some Ethereum validators are entirely relying on public infrastructure like Infura or Alchemy for their execution data. If you are in this case, you will need to install and configure your own execution client.

If you are running your own execution client and using a public infrastructure provider as a fallback endpoint, that fallback endpoint will not work after the merge. Using multiple execution clients after the Merge is going to be slightly more complex. This is out of scope for this guide.

The 2 main concerns for an Ethereum validator when running your own execution client is disk usage and bandwidth usage. It is not uncommon for an execution client to use more than 650GB on to store its data. If your disk size is less than 2TB for storing everything, you should consider migrating to a disk which is at least 2TB in size.

### Installing and configuring a new execution client

If you are not currently running your own execution client and if you used a guide or a tool to setup your staking machine, you should first look again to see if they have a section on how to setup an execution client.

### Managing your execution client disk usage

Pruning your execution client database is a good strategy for managing your execution client disk usage. If you are using Geth, [you should prune it regularly](https://gist.github.com/yorickdowne/3323759b4cbf2022e191ab058a4276b2) and you should prune it just before the Merge. Geth currently only offers offline prunning that takes a few hours to complete. Having an offline execution client after the Merge will result in your validator failing to perform all its duties meaning that you will lose rewards during that time.

Other execution clients have different strategies for managing data growth. Some are leaner in terms of disk size usage to get started with and some include online automatic pruning. You should consider running [a minority execution client](#execution-client-diversity).

I suggest you implement [monitoring](monitoring.md) and [alerting](alerting.md) to help you find out when you are low on available disk space.

### Managing your execution client bandwidth usage



### Execution client diversity

Geth is currently the supermajority execution client. It is used to build almost all blocks right now. This is not currently a big issue but it will become one after the Merge. You should consider running [a minority execution client](https://clientdiversity.org/). We have some great execution clients that work well for an Ethereum validator that should be considered:

- [Erigon](https://github.com/ledgerwatch/erigon#erigon)
- [Besu](https://hyperledger.org/use/besu)
- [Nethermind](http://nethermind.io/)

## Updating your Ethereum clients

## Using the new configuration options for your Ethereum clients

## Configuring a JWT token file

## Configuring your fee recipient address

## Choosing and configuring an MEV solution

## Support

If you have any question or if you need additional support, make sure to get in touch with the ethstaker community on:

* Discord: [discord.io/ethstaker](https://discord.io/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)
