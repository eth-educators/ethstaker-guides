# Guide on how to setup a Holeksy testnet node (Reth/Lodestar)

[Holešky](https://github.com/eth-clients/holesky) is a new Ethereum testnet meant to replace Goerli as a staking, infrastructure and protocol-developer testnet.

This guide is meant for people with little or some experience in running Ethereum clients and using the command-line interface (CLI). It will show you step by step how to setup your machine to join the *Holesky* testnet by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd and APT (like Ubuntu 22.04 or Debian 12) on a modern x86 CPU (Intel, AMD). A clean install of your operating system on a dedicated machine or a virtual machine before proceeding is preferable.

## Overview

We will use the latest version for Reth and the latest version for Lodestar. We will configure them to connect to the *Holesky* testnet.

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
$ sudo apt -y install wget curl ccze
```

## Installing Reth

Download [the latest release version for Reth](https://github.com/paradigmxyz/reth/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the linux x86_64 version.

```console
$ cd ~
$ wget https://github.com/paradigmxyz/reth/releases/download/v1.0.1/reth-v1.0.1-x86_64-unknown-linux-gnu.tar.gz
$ tar xvf reth-v1.0.1-x86_64-unknown-linux-gnu.tar.gz
$ rm reth-v1.0.1-x86_64-unknown-linux-gnu.tar.gz
```

Install this Reth version globally.

```console
$ sudo cp ~/reth /usr/local/bin
$ rm ~/reth
```

## Installing Lodestar

Download [the latest release version for Lodestar](https://github.com/ChainSafe/lodestar/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the linux amd64 version.

```console
$ cd ~
$ wget https://github.com/ChainSafe/lodestar/releases/download/v1.20.0/lodestar-v1.20.0-linux-amd64.tar.gz
$ tar xvf lodestar-v1.20.0-linux-amd64.tar.gz
$ rm lodestar-v1.20.0-linux-amd64.tar.gz
```

Install this Lodestar version globally.

```console
$ sudo cp ~/lodestar /usr/local/bin
$ rm ~/lodestar
```

## Creating the JWT token file

Create a JWT token file in a neutral location and make it readable to everyone. We will use the `/var/lib/ethereum/jwttoken` location to store the JWT token file.

```
$ sudo mkdir -p /var/lib/ethereum
$ openssl rand -hex 32 | tr -d "\n" | sudo tee /var/lib/ethereum/jwttoken
$ sudo chmod +r /var/lib/ethereum/jwttoken
```

## Configuring your Reth node

Create a dedicated user for running Reth, create a directory for holding the data and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false reth
$ sudo mkdir -p /var/lib/reth/logs
$ sudo chown -R reth:reth /var/lib/reth
```

Create a systemd service config file to configure the Reth node service.

```console
$ sudo nano /etc/systemd/system/reth.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`).

```ini
[Unit]
Description=Reth Execution Client (Holesky)
After=network.target
Wants=network.target

[Service]
User=reth
Group=reth
Type=simple
Restart=always
RestartSec=5
TimeoutStopSec=180
ExecStart=reth node \
  --full \
  --chain holesky \
  --datadir /var/lib/reth \
  --log.file.directory /var/lib/reth/logs \
  --metrics 6061 \
  --authrpc.jwtsecret /var/lib/ethereum/jwttoken

[Install]
WantedBy=default.target
```

Reload systemd to reflect the changes and start the service. Check status to make sure it’s running correctly.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl start reth.service
$ sudo systemctl status reth.service
```

It should say active (running) in green text. If not then go back and repeat the steps to fix the problem. Press Q to quit (will not affect the reth service).

Enable the reth service to automatically start on reboot.

```console
$ sudo systemctl enable reth.service
```

You can watch the live messages from your Reth node logs using this command. Make sure nothing suspicious shows up in your logs.

```console
$ sudo journalctl -f -u reth.service -o cat | ccze -A
```

Press `Ctrl` + `C` to stop showing those messages.

## Configuring your Lodestar beacon node

Create a dedicated user for running the Lodestar beacon node, create a directory for holding the data, copy testnet files and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false lodestarbeacon
$ sudo mkdir -p /var/lib/lodestar
$ sudo chown -R lodestarbeacon:lodestarbeacon /var/lib/lodestar
```

Create a systemd service config file to configure the Lodestar beacon node service.

```console
$ sudo nano /etc/systemd/system/lodestarbeacon.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`).

```ini
[Unit]
Description=Lodestar Beacon Node (Holesky)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=lodestarbeacon
Group=lodestarbeacon
Restart=always
RestartSec=5
ExecStart=lodestar beacon \
    --network holesky \
    --dataDir /var/lib/lodestar \
    --checkpointSyncUrl https://holesky.beaconstate.ethstaker.cc \
    --metrics \
    --metrics.port 6071 \
    --jwtSecret /var/lib/ethereum/jwttoken

[Install]
WantedBy=multi-user.target
```

Reload systemd to reflect the changes and start the service. Check status to make sure it’s running correctly.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl start lodestarbeacon.service
$ sudo systemctl status lodestarbeacon.service
```

It should say active (running) in green text. If not then go back and repeat the steps to fix the problem. Press Q to quit (will not affect the Lodestar beacon node service).

Enable the Lodestar beacon node service to automatically start on reboot.

```console
$ sudo systemctl enable lodestarbeacon.service
```

You can watch the live messages from your Lodestar beacon node logs using this command. Make sure nothing suspicious shows up in your logs.

```console
$ sudo journalctl -f -u lodestarbeacon.service -o cat | ccze -A
```

Press `Ctrl` + `C` to stop showing those messages.

## Trying the Holesky testnet

### Requesting testnet funds

Requesting or obtaining enough Holesky ETH to perform your validator deposit can be challenging. We suggest you use the EthStaker #cheap-holesky-validator free process. Join the [EthStaker Discord server](https://dsc.gg/ethstaker) and use the `/cheap-holesky-deposit` slash command (start typing the command and it will show up above your input box). From there, follow the instructions from the bot. As an alternative, you can try obtaining 32 Holesky ETH from various faucets or bridges on https://faucetlink.to/holesky . Holesky ETH was also distributed to anyone who created or deployed a smart contract previously on Goerli. You might already have some Holesky ETH in your wallet if you were involved with smart contracts on Goerli.

## Adding a validator

### Creating your validator keys and performing the deposit

There are 2 great tools to create your validator keys:

* GUI based: [Wagyu Key Gen](https://github.com/stake-house/wagyu-key-gen)
* CLI based: [staking-deposit-cli](https://github.com/ethereum/staking-deposit-cli)

If you choose the *Wagyu Key Gen* application, make sure to select the *Holesky* network and follow the instructions provided. If you are using the #cheap-holesky-validator process, you will need to use `0x4D496CcC28058B1D74B7a19541663E21154f9c84` as your withdrawal address. This is only required for that process. When on Mainnet, you should use a withdrawal address you control if you want to use one.

If you choose the *staking-deposit-cli* application, here is how to create your validator keys. Make sure to replace the `0x4D496CcC28058B1D74B7a19541663E21154f9c84` withdrawal address with your own address that you control if you need or want to:

```console
$ cd ~
$ wget https://github.com/ethereum/staking-deposit-cli/releases/download/v2.7.0/staking_deposit-cli-fdab65d-linux-amd64.tar.gz
$ tar xvf staking_deposit-cli-fdab65d-linux-amd64.tar.gz
$ rm staking_deposit-cli-fdab65d-linux-amd64.tar.gz
$ cd staking_deposit-cli-fdab65d-linux-amd64/
$ ./deposit new-mnemonic --num_validators 1 --chain holesky --execution_address 0x4D496CcC28058B1D74B7a19541663E21154f9c84
$ ls -d $PWD/validator_keys/*
```

Make sure to store your keystore password and your mnemonic somewhere safe. You should end up with a deposit file (starts with `deposit_data-` and ends with `.json`) and one or more keystore files (starts with `keystore-` and ends with `.json`), 1 per validator. Copy them around if needed. Make sure your deposit file and your keystore files are in a known and accessible location on your machine.

Next we will need to perform your deposit. If you used the #cheap-holesky-validator process, you can perform your deposit on https://holesky.launchpad.ethstaker.cc/ . If you managed to obtained 32 Holesky ETH, you can use the official Holesky launchpad on https://holesky.launchpad.ethereum.org/ .

### Configuring your Lodestar validator client

Create a dedicated user for running the Lodestar validator client, create a directory for holding the data and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false lodestarvalidator
$ sudo mkdir -p /var/lib/lodestar/validators
$ sudo chown -R lodestarvalidator:lodestarvalidator /var/lib/lodestar/validators
$ sudo chmod 700 /var/lib/lodestar/validators
```

Import your keystore that includes your validator key for the Lodestar validator client. Running the first command will prompt you for that keystore password. Make sure to enter it correctly and avoid leaving it blank. Make sure to replace `/path/to/keystores` with the actual path to your keystores created [in the previous step](#creating-your-validator-keys-and-performing-the-deposit).

```console
$ sudo lodestar validator import \
    --importKeystores /path/to/keystores \
    --dataDir /var/lib/lodestar/validators \
    --network holesky
$ sudo chown -R lodestarvalidator:lodestarvalidator /var/lib/lodestar/validators
```

Create a systemd service config file to configure the Lodestar validator client service.

```console
$ sudo nano /etc/systemd/system/lodestarvalidator.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`). Make sure to replace the `0x0000000000000000000000000000000000000000` address with your own Ethereum address that you control where you want to receive the transaction tips.

```ini
[Unit]
Description=Lodestar Validator Client (Holesky)
Wants=network-online.target
After=network-online.target

[Service]
User=lodestarvalidator
Group=lodestarvalidator
Type=simple
Restart=always
RestartSec=5
ExecStart=lodestar validator \
    --network holesky \
    --dataDir /var/lib/lodestar/validators \
    --graffiti EthStaker \
    --metrics true \
    --suggestedFeeRecipient 0x0000000000000000000000000000000000000000

[Install]
WantedBy=multi-user.target
```

Reload systemd to reflect the changes and start the service. Check status to make sure it’s running correctly.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl start lodestarvalidator.service
$ sudo systemctl status lodestarvalidator.service
```

It should say active (running) in green text. If not then go back and repeat the steps to fix the problem. Press Q to quit (will not affect the Lodestar validator client service).

Enable the Lodestar validator client service to automatically start on reboot.

```console
$ sudo systemctl enable lodestarvalidator.service
```

You can watch the live messages from your Lodestar validator client logs using this command.

```console
$ sudo journalctl -f -u lodestarvalidator.service -o cat | ccze -A
```

Press `Ctrl` + `C` to stop showing those messages.

## Support

If you have any question or if you need additional support, make sure to get in touch with the EthStaker community on:

* Discord: [dsc.gg/ethstaker](https://dsc.gg/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)

## Credits

Based on [Somer Esat's guide](https://github.com/SomerEsat/ethereum-staking-guide).
