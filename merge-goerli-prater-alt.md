# Guide on how to join the Goerli/Prater merge testnet (Besu/Teku)

[*#TestingTheMerge*](https://twitter.com/search?q=%23TestingTheMerge) is an Ethereum community initiative to test [the merge upgrade](https://ethereum.org/en/eth2/merge/) with various testnets. It is being spear headed by [Marius van der Wijden](https://twitter.com/vdWijden) and [Parithosh Jayanthi](https://twitter.com/parithosh_j). It is meant to test the recent experimental features added to various Ethereum clients supporting this protocol upgrade.

This guide is meant for people with little or some experience in running Ethereum clients and using the command-line interface (CLI). It will show you step by step how to setup your machine to join the *Goerli/Prater* merge testnet by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd and APT (like Ubuntu 20.04 or Ubuntu 22.04, but it should work on most recent debian derivatives) on a modern x86 CPU (Intel, AMD). A clean install of your operating system on a dedicated machine or a virtual machine before proceeding is preferable.

## Overview

We will use the latest version for Besu and the latest version for Teku. We will configure them to connect to the *Goerli/Prater* merge testnet. This is an alternative guide to [the main one who uses the Geth/Lighthouse combo](merge-goerli-prater.md) for its clients.

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
$ sudo apt -y install software-properties-common wget curl ccze apt-transport-https libjemalloc-dev
```

Install Adoptium JDK (Java).

```console
$ sudo mkdir -p /etc/apt/keyrings
$ wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | sudo tee /etc/apt/keyrings/adoptium.asc
$ echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | sudo tee /etc/apt/sources.list.d/adoptium.list
$ sudo apt -y update
$ sudo apt -y install temurin-17-jdk
```

## Installing Besu

Download [the latest release version for Besu](https://github.com/hyperledger/besu/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the download link that ends with `tar.gz`.

```console
$ cd ~
$ wget https://hyperledger.jfrog.io/artifactory/besu-binaries/besu/22.7.0/besu-22.7.0.tar.gz
$ tar xvf besu-22.7.0.tar.gz
$ rm besu-22.7.0.tar.gz
```

Install this Besu version globally.

```console
$ sudo cp -a ./besu-22.7.0 /usr/local/bin/besu
$ rm -rf ./besu-22.7.0
```

## Installing Teku

Download [the latest release version for Teku](https://github.com/ConsenSys/teku/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the download link from the *Downloads* section of the release description. It should be a file that ends with `tar.gz` and it should **not** be the one called 'Source code'.

```console
$ cd ~
$ wget https://artifacts.consensys.net/public/teku/raw/names/teku.tar.gz/versions/22.8.0/teku-22.8.0.tar.gz
$ tar xvf teku-22.8.0.tar.gz
$ rm teku-22.8.0.tar.gz
```

Install this Teku version globally.

```console
$ sudo cp -a ./teku-22.8.0 /usr/local/bin/teku
$ rm -rf ./teku-22.8.0
```

## Creating the JWT token file

Create a JWT token file in a neutral location and make it readable to everyone. We will use the `/var/lib/ethereum/jwttoken` location to store the JWT token file.

```
$ sudo mkdir -p /var/lib/ethereum
$ openssl rand -hex 32 | tr -d "\n" | sudo tee /var/lib/ethereum/jwttoken
$ sudo chmod +r /var/lib/ethereum/jwttoken
```

## Configuring your Besu node

Create a dedicated user for running Besu, create a directory for holding the data and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false besu
$ sudo mkdir -p /var/lib/besu
$ sudo chown -R besu:besu /var/lib/besu
```

Create a systemd service config file to configure the Besu node service.

```console
$ sudo nano /etc/systemd/system/besu.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`).

```ini
[Unit]
Description=Besu Ethereum Client (Goerli)
After=network.target
Wants=network.target

[Service]
User=besu
Group=besu
Type=simple
Restart=always
RestartSec=5
TimeoutStopSec=180
LimitNOFILE=8388608
ExecStart=/usr/local/bin/besu/bin/besu \
    --network=goerli \
    --sync-mode=X_CHECKPOINT \
    --rpc-http-enabled=true \
    --engine-rpc-port=8551 \
    --engine-host-allowlist=localhost,127.0.0.1 \
    --data-path=/var/lib/besu \
    --data-storage-format=BONSAI \
    --metrics-enabled=true \
    --engine-jwt-secret=/var/lib/ethereum/jwttoken

[Install]
WantedBy=default.target
```

Reload systemd to reflect the changes and start the service. Check status to make sure it’s running correctly.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl start besu.service
$ sudo systemctl status besu.service
```

It should say active (running) in green text. If not then go back and repeat the steps to fix the problem. Press Q to quit (will not affect the besu service).

Enable the besu service to automatically start on reboot.

```console
$ sudo systemctl enable besu.service
```

You can watch the live messages from your Besu node logs using this command. Make sure nothing suspicious shows up in your logs.

```console
$ sudo journalctl -f -u besu.service -o cat | ccze -A
```

Press `Ctrl` + `C` to stop showing those messages.

## Trying the Goerli/Prater merge testnet

### Requesting testnet funds

You can request Goerli ETH from [EthStaker Discord server](https://discord.io/ethstaker) in the #request-goerli-eth💸 channel with a BrightID verification. You can check out [these other faucet links](https://faucetlink.to/goerli) as well. You will need at least 32 Goerli ETH if you want to do a validator deposit for Goerli. The EthStaker Discord faucet will give you 32.05 Goerli ETH in one go.

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
$ rm staking_deposit-cli-9ab0b05-linux-amd64.tar.gz
$ cd staking_deposit-cli-9ab0b05-linux-amd64/
$ ./deposit new-mnemonic --num_validators 1 --chain prater
$ ls -d $PWD/validator_keys/*
```

Make sure to store your keystore password and your mnemonic somewhere safe. You should end up with a deposit file (starts with `deposit_data-` and ends with `.json`) and one or more keystore files (starts with `keystore-` and ends with `.json`), 1 per validator. Copy them around if needed. Make sure your deposit file and your keystore files are in a known and accessible location on your machine.

Next we will do the deposit using the Prater launchpad. Make sure you have access to a browser with MetaMask, your account with the funds from the faucet and the deposit file we just created.

Go to [the Prater launchpad](https://prater.launchpad.ethereum.org/en/). Follow the instructions, make sure *Prater* is the selected network in MetaMask and use the deposit file to perform your deposit.

You can check that your deposit transaction went through on [the transaction explorer](https://goerli.etherscan.io/address/0xff50ed3d0ec03aC01D4C79aAd74928BFF48a7b2b).

## Configuring your Teku node

Create a dedicated user for running the Teku node, create a directory for holding the data, copy testnet files and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false teku
$ sudo mkdir -p /var/lib/teku
$ sudo chown -R teku:teku /var/lib/teku
```

Create a directory for validator keys and copy your keystore file(s). Make sure to replace `/path/to/keystore` with the actual path to your keystore created [in the previous step](#creating-your-validator-keys-and-performing-the-deposit) (only copy the keystore files, the ones that starts with `keystore-` and ends with `.json`). Perform the cp command for each keystore you have. You will typically only have 1 for the Goerli/Prater merge testnet.

```console
$ sudo mkdir -p /var/lib/teku/validator_keys
$ sudo cp /path/to/keystore /var/lib/teku/validator_keys
$ ls /var/lib/teku/validator_keys
```

The output of that last listing (`ls` command) should look like this:

```console
keystore-m_12381_3600_0_0_0-1659033295.json
```

Create your password file(s). For each `keystore_m*.json` file, create an equivalently named password file. The name of that password file should be the same one as your keystore file except the extension should be `.txt` and the content should be your keystore password. Before you execute the next command replace `<jsonfilename>` with the name of the json file.

```console
$ sudo nano /var/lib/teku/validator_keys/<jsonfilename>.txt
```

If my keystore file was named `keystore-m_12381_3600_0_0_0-1659033295.json`, my command above would have been `$ sudo nano /var/lib/teku/validator_keys/keystore-m_12381_3600_0_0_0-1659033295.txt`.

Type your keystore password into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`).

Assign the proper permissions to the validator keys directory.

```console
$ sudo chown -R teku:teku /var/lib/teku/validator_keys
$ sudo chmod -R 700 /var/lib/teku/validator_keys
```

List the files in the validator keys directory and make sure you have a corresponding `.txt` file with your keystore password in it for each keystore file you have.

```console
$ sudo ls /var/lib/teku/validator_keys
```

Download a checkpoint state for quick sync.

```console
$ sudo curl -o /var/lib/teku/finalized-state.ssz -H 'Accept: application/octet-stream' https://goerli.checkpoint-sync.ethdevops.io/eth/v2/debug/beacon/states/finalized
$ sudo chown teku:teku /var/lib/teku/finalized-state.ssz
```

Create a systemd service config file to configure the Teku node service.

```console
$ sudo nano /etc/systemd/system/teku.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`). Make sure to replace the `0x0000000000000000000000000000000000000000` address with your own Ethereum address that you control where you want to receive the transaction tips.

```ini
[Unit]
Description=Teku Ethereum Client (Prater)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=teku
Group=teku
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/teku/bin/teku \
    --network prater \
    --data-path /var/lib/teku \
    --validator-keys /var/lib/teku/validator_keys:/var/lib/teku/validator_keys \
    --rest-api-enabled true \
    --ee-endpoint http://127.0.0.1:8551 \
    --metrics-enabled true \
    --validators-graffiti EthStaker \
    --validators-proposer-default-fee-recipient 0x0000000000000000000000000000000000000000 \
    --initial-state /var/lib/teku/finalized-state.ssz \
    --ee-jwt-secret-file /var/lib/ethereum/jwttoken

[Install]
WantedBy=multi-user.target
```

Reload systemd to reflect the changes and start the service. Check status to make sure it’s running correctly.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl start teku.service
$ sudo systemctl status teku.service
```

It should say active (running) in green text. If not then go back and repeat the steps to fix the problem. Press Q to quit (will not affect the Teku node service).

Enable the Teku node service to automatically start on reboot.

```console
$ sudo systemctl enable teku.service
```

You can watch the live messages from your Teku node logs using this command. Make sure nothing suspicious shows up in your logs.

```console
$ sudo journalctl -f -u teku.service -o cat | ccze -A
```

Press `Ctrl` + `C` to stop showing those messages.

## What's next?

You performs a lot of different tasks to help with the [*#TestingTheMerge*](https://twitter.com/search?q=%23TestingTheMerge) initiative. Check out [the program structure](https://hackmd.io/WKpg6SNzQbi1jVKNgrSgWg). There are different tasks for all technical abilities.

## Support

If you have any question or if you need additional support, make sure to get in touch with people involved with this initiative:

* EthStaker Discord: [discord.io/ethstaker](https://discord.io/ethstaker) in the #ropsten channel
* Eth R&D Discord: [discord.gg/qGpsxSA](https://discord.gg/qGpsxSA) in the #testing channel under the *Merge* category.

## Credits

Based on [Somer Esat's guide](https://github.com/SomerEsat/ethereum-staking-guide).
Based on [Ethereum community's guide](https://notes.ethereum.org/qrDBhhydTsyKFmGaBl2COQ).
