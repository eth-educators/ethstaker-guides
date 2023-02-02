# Guide on how to join the Zhejiang testnet (Geth/Lighthouse)

[*Zhejiang*](https://zhejiang.ethpandaops.io/) is public Ethereum testnet to test the forks that will include changes for [withdrawals](https://ethereum.org/en/staking/#accordion-panel-:R17alelajkau:). Zhejiang will go through the Shanghai fork on the execution layer side and the Capella fork on the consensus layer side. Both of these forks will happen at the same time and they will include [various features to be tested](https://notes.ethereum.org/@launchpad/zhejiang#What-is-in-the-Zhejiang-testnet) including withdrawals and BLS to execution changes.

This guide is meant for people with little or some experience in running Ethereum clients and using the command-line interface (CLI). It will show you step by step how to setup your machine to join the *Zhejiang* testnet by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd and APT (like Ubuntu 20.04 or Ubuntu 22.04, but it should work on most recent debian derivatives) on a modern x86 CPU (Intel, AMD). A clean install of your operating system on a dedicated machine or a virtual machine before proceeding is preferable.

## Overview

We will build the latest development version for Geth and a special capella version for Lighthouse. We will configure them to connect to the *Zhejiang* testnet. There will be an alternative guide to this one who will use the Besu/Teku combo for its clients (TBC).

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
$ sudo apt -y install software-properties-common wget curl ccze git gcc g++ make cmake pkg-config llvm-dev libclang-dev clang protobuf-compiler build-essential
```

Install a recent version of Go.

```console
$ cd ~
$ wget https://go.dev/dl/go1.20.linux-amd64.tar.gz
$ sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.20.linux-amd64.tar.gz
$ rm go1.20.linux-amd64.tar.gz
$ export PATH=/usr/local/go/bin:$PATH
$ cat << 'EOF' >> ~/.profile

# set PATH so it includes Go bin directory
if [ -d "/usr/local/go/bin" ] ; then
    PATH="/usr/local/go/bin:$PATH"
fi
EOF
```

Install a recent version of Rust.

```console
$ cd ~
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

You will be prompted with a menu and a few selections. Press `1` and `↵ Enter` to proceed with the default installation.

Setup your environment for Rust.

```console
$ source "$HOME/.cargo/env"
```

## Zhejiang configuration details

Obtain the Zhejiang configuration files and make them accessible.

```console
$ cd ~
$ git clone https://github.com/ethpandaops/withdrawals-testnet.git
$ sudo mkdir -p /var/lib/ethereum/zhejiang
$ sudo cp -R ~/withdrawals-testnet/zhejiang-testnet/custom_config_data /var/lib/ethereum/zhejiang
```

## Building and installing Geth

Obtain the latest development version for Geth and build it.

```console
$ cd ~
$ git clone https://github.com/ethereum/go-ethereum.git
$ cd go-ethereum
$ make geth
```

Install the Geth binary globally.

```console
$ sudo cp ~/go-ethereum/build/bin/geth /usr/local/bin/geth-dev
```

## Building and installing Geth Lighthouse

Obtain the special capella version for Lighthouse and build it.

```console
$ cd ~
$ git clone -b capella https://github.com/sigp/lighthouse.git
$ cd lighthouse
$ make
```

Install this Lighthouse version globally.

```console
$ sudo cp ~/.cargo/bin/lighthouse /usr/local/bin/lighthouse-capella
```

## Creating the JWT token file

Create a JWT token file in a neutral location and make it readable to everyone. We will use the `/var/lib/ethereum/zhejiang/jwttoken` location to store the JWT token file.

```
$ sudo mkdir -p /var/lib/ethereum/zhejiang
$ openssl rand -hex 32 | tr -d "\n" | sudo tee /var/lib/ethereum/zhejiang/jwttoken
$ sudo chmod +r /var/lib/ethereum/zhejiang/jwttoken
```

## Configuring your Geth node

Create a dedicated user for running Geth, create a directory for holding the data and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false goeth
$ sudo mkdir -p /var/lib/goethereum
$ sudo chown -R goeth:goeth /var/lib/goethereum
```

Initialize the Geth database with the Zhejiang configuration details.

```console
$ sudo -u goeth geth-dev --datadir /var/lib/goethereum init /var/lib/ethereum/zhejiang/custom_config_data/genesis.json
```

Create a systemd service config file to configure the Geth node service.

```console
$ sudo nano /etc/systemd/system/geth.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`).

```ini
[Unit]
Description=Go Ethereum Client - Geth (Zhejiang)
After=network.target
Wants=network.target

[Service]
User=goeth
Group=goeth
Type=simple
Restart=always
RestartSec=5
TimeoutStopSec=180
ExecStart=geth-dev \
    --networkid=1337803 \
    --http \
    --datadir /var/lib/goethereum \
    --metrics \
    --metrics.expensive \
    --pprof \
    --authrpc.jwtsecret=/var/lib/ethereum/zhejiang/jwttoken \
    --syncmode=full \
    --bootnodes "enode://691c66d0ce351633b2ef8b4e4ef7db9966915ca0937415bd2b408df22923f274873b4d4438929e029a13a680140223dcf701cabe22df7d8870044321022dfefa@64.225.78.1:30303,enode://89347b9461727ee1849256d78e84d5c86cc3b4c6c5347650093982b726d71f3d08027e280b399b7b6604ceeda863283dcfe1a01e93728b4883114e9f8c7cc8ef@146.190.238.212:30303,enode://c2892072efe247f21ed7ebea6637ade38512a0ae7c5cffa1bf0786d5e3be1e7f40ff71252a21b36aa9de54e49edbcfc6962a98032adadfa29c8524262e484ad3@165.232.84.160:30303,enode://71e862580d3177a99e9837bd9e9c13c83bde63d3dba1d5cea18e89eb2a17786bbd47a8e7ae690e4d29763b55c205af13965efcaf6105d58e118a5a8ed2b0f6d0@68.183.13.170:30303,enode://2f6cf7f774e4507e7c1b70815f9c0ccd6515ee1170c991ce3137002c6ba9c671af38920f5b8ab8a215b62b3b50388030548f1d826cb6c2b30c0f59472804a045@161.35.147.98:30303"

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

Create a dedicated user for running the Lighthouse beacon node, create a directory for holding the data and assign the proper permissions.

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
Description=Lighthouse Ethereum Client Beacon Node (Zhejiang)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=lighthousebeacon
Group=lighthousebeacon
Restart=always
RestartSec=5
ExecStart=lighthouse-capella bn \
    --testnet-dir /var/lib/ethereum/zhejiang/custom_config_data \
    --datadir /var/lib/lighthouse \
    --http \
    --execution-endpoint http://127.0.0.1:8551 \
    --metrics \
    --validator-monitor-auto \
    --boot-nodes="enr:-Iq4QMCTfIMXnow27baRUb35Q8iiFHSIDBJh6hQM5Axohhf4b6Kr_cOCu0htQ5WvVqKvFgY28893DHAg8gnBAXsAVqmGAX53x8JggmlkgnY0gmlwhLKAlv6Jc2VjcDI1NmsxoQK6S-Cii_KmfFdUJL2TANL3ksaKUnNXvTCv1tLwXs0QgIN1ZHCCIyk,enr:-Ly4QOS00hvPDddEcCpwA1cMykWNdJUK50AjbRgbLZ9FLPyBa78i0NwsQZLSV67elpJU71L1Pt9yqVmE1C6XeSI-LV8Bh2F0dG5ldHOIAAAAAAAAAACEZXRoMpDuKNezAAAAckYFAAAAAAAAgmlkgnY0gmlwhEDhTgGJc2VjcDI1NmsxoQIgMUMFvJGlr8dI1TEQy-K78u2TJE2rWvah9nGqLQCEGohzeW5jbmV0cwCDdGNwgiMog3VkcIIjKA,enr:-MK4QMlRAwM7E8YBo6fqP7M2IWrjFHP35uC4pWIttUioZWOiaTl5zgZF2OwSxswTQwpiVCnj4n56bhy4NJVHSe682VWGAYYDHkp4h2F0dG5ldHOIAAAAAAAAAACEZXRoMpDuKNezAAAAckYFAAAAAAAAgmlkgnY0gmlwhJK-7tSJc2VjcDI1NmsxoQLDq7LlsXIXAoJXPt7rqf6CES1Q40xPw2yW0RQ-Ly5S1YhzeW5jbmV0cwCDdGNwgiMog3VkcIIjKA,enr:-MS4QCgiQisRxtzXKlBqq_LN1CRUSGIpDKO4e2hLQsffp0BrC3A7-8F6kxHYtATnzcrsVOr8gnwmBnHYTFvE9UmT-0EHh2F0dG5ldHOIAAAAAAAAAACEZXRoMpDuKNezAAAAckYFAAAAAAAAgmlkgnY0gmlwhKXoVKCJc2VjcDI1NmsxoQK6J-uvOXMf44iIlilx1uPWGRrrTntjLEFR2u-lHcHofIhzeW5jbmV0c4gAAAAAAAAAAIN0Y3CCIyiDdWRwgiMo,enr:-LK4QOQd-elgl_-dcSoUyHDbxBFNgQ687lzcKJiSBtpCyPQ0DinWSd2PKdJ4FHMkVLWD-oOquXPKSMtyoKpI0-Wo_38Bh2F0dG5ldHOIAAAAAAAAAACEZXRoMpDuKNezAAAAckYFAAAAAAAAgmlkgnY0gmlwhES3DaqJc2VjcDI1NmsxoQNIf37JZx-Lc8pnfDwURcHUqLbIEZ1RoxjZuBRtEODseYN0Y3CCIyiDdWRwgiMo,enr:-KG4QLNORYXUK76RPDI4rIVAqX__zSkc5AqMcwAketVzN9YNE8FHSu1im3qJTIeuwqI5JN5SPVsiX7L9nWXgWLRUf6sDhGV0aDKQ7ijXswAAAHJGBQAAAAAAAIJpZIJ2NIJpcIShI5NiiXNlY3AyNTZrMaECpA_KefrVAueFWiLLDZKQPPVOxMuxGogPrI474FaS-x2DdGNwgiMog3VkcIIjKA" \
    --execution-jwt /var/lib/ethereum/zhejiang/jwttoken

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
$ rm staking_deposit-cli-9ab0b05-linux-amd64.tar.gz
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

TODO

## Support

If you have any question or if you need additional support, make sure to get in touch with people involved with this:

* EthStaker Discord: [discord.io/ethstaker](https://discord.io/ethstaker) in the #zhejiang-🔑 channel
* Eth R&D Discord: [discord.gg/qGpsxSA](https://discord.gg/qGpsxSA) in the #testing channel under the *Shanghai* category.

## Credits

Based on [Somer Esat's guide](https://github.com/SomerEsat/ethereum-staking-guide).
Based on [How to run a node on the Zhejiang testnet?](https://notes.ethereum.org/@launchpad/zhejiang).
