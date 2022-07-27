# Guide on how to join the Goerli/Prater merge testnet

[*#TestingTheMerge*](https://twitter.com/search?q=%23TestingTheMerge) is an Ethereum community initiative to test [the merge upgrade](https://ethereum.org/en/eth2/merge/) with various testnets. It is being spear headed by [Marius van der Wijden](https://twitter.com/vdWijden) and [Parithosh Jayanthi](https://twitter.com/parithosh_j). It is meant to test the recent experimental features added to various Ethereum clients supporting this protocol upgrade.

This guide is meant for people with little or some experience in running Ethereum clients and using the command-line interface (CLI). It will show you step by step how to setup your machine to join the *Goerli/Prater* merge testnet by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd and APT (like Ubuntu 20.04 or Ubuntu 22.04, but it should work on most recent debian derivatives) on a modern x86 CPU (Intel, AMD). A clean install of your operating system on a dedicated machine or a virtual machine before proceeding is preferable.

## Overview

We will use the latest version for Geth and the latest version for Lighthouse. We will configure them to connect to the *Goerli/Prater* merge testnet.

## Executing the commands

Almost all of these commands will be performed in a terminal. Start your *Terminal* application. Any line that starts with the dollar sign (`$`) is a command that need to be executed in your terminal. Do not input the dollar sign (`$`) in your terminal, only the text that comes after that.

Executing a command with `sudo` will occasionally ask you for your password. Make sure to enter your account password correctly. You can execute the command again if you fail to enter the correct password after a few attempts.

## Installing Prerequisites

Make sure we have fully updated packages first.

```console
$ sudo apt -y update
$ sudo apt -y upgrade
```

Install prerequisites commonly available.

```console
$ sudo apt -y install software-properties-common wget curl ccze
```

## Installing Geth

Add the Ethereum PPA and install the Geth package.

```console
$ sudo add-apt-repository -y ppa:ethereum/ethereum
$ sudo apt -y install geth
```

## Installing Lighthouse

Download [the latest release version for Lighthouse](https://github.com/sigp/lighthouse/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the linux x86_64 version.

```console
$ cd ~
$ wget https://github.com/sigp/lighthouse/releases/download/v2.4.0/lighthouse-v2.4.0-x86_64-unknown-linux-gnu.tar.gz
$ tar xvf lighthouse-v2.4.0-x86_64-unknown-linux-gnu.tar.gz
$ rm lighthouse-v2.4.0-x86_64-unknown-linux-gnu.tar.gz
```

Install this Lighthouse version globally.

```console
$ sudo cp ~/lighthouse /usr/local/bin
$ rm ~/lighthouse
```

## Creating the JWT token file

Create a JWT token file in a neutral location and make it readable to everyone. We will use the `/var/lib/ethereum/jwttoken` location to store the JWT token file.

```
$ sudo mkdir -p /var/lib/ethereum
$ openssl rand -hex 32 | tr -d "\n" | sudo tee /var/lib/ethereum/jwttoken
$ sudo chmod +r /var/lib/ethereum/jwttoken
```

## Configuring your Geth node

Create a dedicated user for running Geth, create a directory for holding the data and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false goeth
$ sudo mkdir -p /var/lib/goethereum
$ sudo chown -R goeth:goeth /var/lib/goethereum
```

Create a systemd service config file to configure the Geth node service.

```console
$ sudo nano /etc/systemd/system/geth.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`).

```ini
[Unit]
Description=Go Ethereum Client - Geth (Goerli)
After=network.target
Wants=network.target

[Service]
User=goeth
Group=goeth
Type=simple
Restart=always
RestartSec=5
TimeoutStopSec=180
ExecStart=geth \
    --goerli \
    --http \
    --datadir /var/lib/goethereum \
    --metrics \
    --metrics.expensive \
    --pprof \
    --authrpc.jwtsecret=/var/lib/ethereum/jwttoken

[Install]
WantedBy=default.target
```

Reload systemd to reflect the changes and start the service. Check status to make sure it’s running correctly.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl start geth.service
$ sudo systemctl status geth.service
```

It should say active (running) in green text. If not then go back and repeat the steps to fix the problem. Press Q to quit (will not affect the geth service).

Enable the geth service to automatically start on reboot.

```console
$ sudo systemctl enable geth.service
```

You can watch the live messages from your Geth node logs using this command. Make sure nothing suspicious shows up in your logs.

```console
$ sudo journalctl -f -u geth.service -o cat | ccze -A
```

Press `Ctrl` + `C` to stop showing those messages.

## Configuring your Lighthouse beacon node

Create a dedicated user for running the Lighthouse beacon node, create a directory for holding the data, copy testnet files and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false lighthousebeacon
$ sudo mkdir -p /var/lib/lighthouse
$ sudo chown -R lighthousebeacon:lighthousebeacon /var/lib/lighthouse
```

Create a systemd service config file to configure the Lighthouse beacon node service.

```console
$ sudo nano /etc/systemd/system/lighthousebeacon.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`).

```ini
[Unit]
Description=Lighthouse Ethereum Client Beacon Node (Prater)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=lighthousebeacon
Group=lighthousebeacon
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/lighthouse bn \
    --network prater \
    --datadir /var/lib/lighthouse \
    --http \
    --execution-endpoint http://127.0.0.1:8551 \
    --metrics \
    --validator-monitor-auto \
    --checkpoint-sync-url=https://goerli.checkpoint-sync.ethdevops.io \
    --execution-jwt=/var/lib/ethereum/jwttoken

[Install]
WantedBy=multi-user.target
```

Reload systemd to reflect the changes and start the service. Check status to make sure it’s running correctly.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl start lighthousebeacon.service
$ sudo systemctl status lighthousebeacon.service
```

It should say active (running) in green text. If not then go back and repeat the steps to fix the problem. Press Q to quit (will not affect the Lighthouse beacon node service).

Enable the Lighthouse beacon node service to automatically start on reboot.

```console
$ sudo systemctl enable lighthousebeacon.service
```

You can watch the live messages from your Lighthouse beacon node logs using this command. Make sure nothing suspicious shows up in your logs.

```console
$ sudo journalctl -f -u lighthousebeacon.service -o cat | ccze -A
```

Press `Ctrl` + `C` to stop showing those messages.

## Trying the Goerli/Prater merge testnet

### Requesting testnet funds

You can request Goerli ETH from [EthStaker Discord server](https://discord.io/ethstaker) in the #request-goerli-eth💸 channel with a BrightID verification. You can check out [these other faucet links](https://faucetlink.to/goerli) as well. You will need at least 32 Goerli ETH if you want to do a validator deposit for Goerli. The EthStaker Discord faucet will give you 32.05 Goerli ETH in one go.

## Adding a validator

### Creating your validator keys and performing the deposit

There are 2 great tools to create your validator keys:

* GUI based: [Wagyu Key Gen](https://github.com/stake-house/wagyu-key-gen)
* CLI based: [staking-deposit-cli](https://github.com/ethereum/staking-deposit-cli)

If you choose the *Wagyu Key Gen* application, make sure to select the *Prater* network and follow the instructions provided.

If you choose the *staking-deposit-cli* application, here is how to create your validator keys:

```console
$ cd ~
$ wget https://github.com/ethereum/staking-deposit-cli/releases/download/v2.2.0/staking_deposit-cli-9ab0b05-linux-amd64.tar.gz
$ tar xvf staking_deposit-cli-9ab0b05-linux-amd64.tar.gz
$ cd staking_deposit-cli-9ab0b05-linux-amd64/
$ ./deposit new-mnemonic --num_validators 1 --chain prater
$ ls -d $PWD/validator_keys/*
```

Make sure to store your keystore password and your mnemonic somewhere safe. You should end up with a deposit file (starts with `deposit_data-` and ends with `.json`) and one or more keystore files (starts with `keystore-` and ends with `.json`), 1 per validator. Copy them around if needed. Make sure your deposit file and your keystore files are in a known and accessible location on your machine.

Next we will do the deposit using the Prater launchpad. Make sure you have access to a browser with MetaMask, your account with the funds from the faucet and the deposit file we just created.

Go to [the Prater launchpad](https://prater.launchpad.ethereum.org/en/). Follow the instructions, make sure *Prater* is the selected network in MetaMask and use the deposit file to perform your deposit.

You can check that your deposit transaction went through on [the transaction explorer](https://goerli.etherscan.io/address/0xff50ed3d0ec03aC01D4C79aAd74928BFF48a7b2b).

### Configuring your Lighthouse validator client

Create a dedicated user for running the Lighthouse validator client, create a directory for holding the data and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false lighthousevalidator
$ sudo mkdir -p /var/lib/lighthouse/validators
$ sudo chown -R lighthousevalidator:lighthousevalidator /var/lib/lighthouse/validators
$ sudo chmod 700 /var/lib/lighthouse/validators
```

Import your keystore that includes your validator key for the Lighthouse validator client. Running the first command will prompt you for that keystore password. Make sure to enter it correctly and avoid leaving it blank. Make sure to replace `/path/to/keystores` with the actual path to your keystores created [in the previous step](#creating-your-validator-keys-and-performing-the-deposit).

```console
$ sudo /usr/local/bin/lighthouse account validator import \
    --directory /path/to/keystores \
    --datadir /var/lib/lighthouse \
    --network prater
$ sudo chown -R lighthousevalidator:lighthousevalidator /var/lib/lighthouse/validators
```

Create a systemd service config file to configure the Lighthouse validator client service.

```console
$ sudo nano /etc/systemd/system/lighthousevalidator.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`). Make sure to replace the `0x0000000000000000000000000000000000000000` address with your own Ethereum address that you control where you want to receive the transaction tips.

```ini
[Unit]
Description=Lighthouse Ethereum Client Validator Client (Prater)
Wants=network-online.target
After=network-online.target

[Service]
User=lighthousevalidator
Group=lighthousevalidator
Type=simple
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/lighthouse vc \
    --network prater \
    --datadir /var/lib/lighthouse \
    --graffiti EthStaker \
    --metrics \
    --suggested-fee-recipient 0x0000000000000000000000000000000000000000

[Install]
WantedBy=multi-user.target
```

Reload systemd to reflect the changes and start the service. Check status to make sure it’s running correctly.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl start lighthousevalidator.service
$ sudo systemctl status lighthousevalidator.service
```

It should say active (running) in green text. If not then go back and repeat the steps to fix the problem. Press Q to quit (will not affect the Lighthouse validator client service).

Enable the Lighthouse validator client service to automatically start on reboot.

```console
$ sudo systemctl enable lighthousevalidator.service
```

You can watch the live messages from your Lighthouse validator client logs using this command.

```console
$ sudo journalctl -f -u lighthousevalidator.service -o cat | ccze -A
```

Press `Ctrl` + `C` to stop showing those messages.

## What's next?

You performs a lot of different tasks to help with the [*#TestingTheMerge*](https://twitter.com/search?q=%23TestingTheMerge) initiave. Check out [the program structure](https://hackmd.io/WKpg6SNzQbi1jVKNgrSgWg). There are different tasks for all technical abilities.

## Support

If you have any question or if you need additional support, make sure to get in touch with people involved with this initiative:

* EthStaker Discord: [discord.io/ethstaker](https://discord.io/ethstaker) in the #ropsten channel
* Eth R&D Discord: [discord.gg/qGpsxSA](https://discord.gg/qGpsxSA) in the #testing channel under the *Merge* category.

## Credits

Based on [Somer Esat's guide](https://github.com/SomerEsat/ethereum-staking-guide).
Based on [Ethereum community's guide](https://notes.ethereum.org/qrDBhhydTsyKFmGaBl2COQ).
