# Guide on how to setup a Hoodi testnet node (Nethermind/Lighthouse)

[Hoodi](https://github.com/eth-clients/hoodi) is a new Ethereum testnet meant to replace Holesky as a staking, infrastructure and protocol-developer testnet.

This guide is meant for people with little or some experience in running Ethereum clients and using the command-line interface (CLI). It will show you step by step how to setup your machine to join the *Hoodi* testnet by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd and APT (like Ubuntu 24.04 or Debian 12) on a modern x86 CPU (Intel, AMD). A clean install of your operating system on a dedicated machine or a virtual machine before proceeding is preferable.

## Overview

We will use the latest version for Nethermind and the latest version for Lighthouse. We will configure them to connect to the *Hoodi* testnet.

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
$ sudo apt -y install wget curl ccze unzip
```

## Installing Nethermind

Download [the latest release version for Nethermind](https://github.com/NethermindEth/nethermind/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the linux-x64 version.

```console
$ cd ~
$ wget https://github.com/NethermindEth/nethermind/releases/download/1.31.6/nethermind-1.31.6-4e68f8ee-linux-x64.zip
$ sudo mkdir -p /usr/share/nethermind
$ sudo unzip nethermind-1.31.6-4e68f8ee-linux-x64.zip -d /usr/share/nethermind
$ rm nethermind-1.31.6-4e68f8ee-linux-x64.zip
```

## Installing Lighthouse

Download [this specific version for Lighthouse](https://github.com/sigp/lighthouse/releases/tag/v7.0.0-beta.4) and extract it. If the latest version is more recent and supports the Hoodi network, use that version and adjust for the new URL and archive name. Make sure to use the linux x86_64 version.

```console
$ cd ~
$ wget https://github.com/sigp/lighthouse/releases/download/v7.0.0-beta.5/lighthouse-v7.0.0-beta.5-x86_64-unknown-linux-gnu.tar.gz
$ tar xvf lighthouse-v7.0.0-beta.5-x86_64-unknown-linux-gnu.tar.gz
$ rm lighthouse-v7.0.0-beta.5-x86_64-unknown-linux-gnu.tar.gz
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

## Configuring your Nethermind node

Create a dedicated user for running Nethermind, create a directory for holding the data and assign the proper permissions.

```console
$ sudo useradd --no-create-home --shell /bin/false nethermind
$ sudo mkdir -p /var/lib/nethermind
$ sudo chown -R nethermind:nethermind /var/lib/nethermind
```

Create a systemd service config file to configure the Nethermind node service.

```console
$ sudo nano /etc/systemd/system/nethermind.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`).

```ini
[Unit]
Description=Nethermind Execution Client (Hoodi)
After=network.target
Wants=network.target

[Service]
User=nethermind
Group=nethermind
Type=simple
Restart=always
RestartSec=5
TimeoutStopSec=180
WorkingDirectory=/var/lib/nethermind
Environment="DOTNET_BUNDLE_EXTRACT_BASE_DIR=/var/lib/nethermind"
ExecStart=/usr/share/nethermind/nethermind \
  --config hoodi \
  --datadir /var/lib/nethermind \
  --Metrics.Enabled true \
  --Metrics.ExposePort 6061 \
  --Sync.SnapSync true \
  --JsonRpc.JwtSecretFile /var/lib/ethereum/jwttoken \
  --JsonRpc.Enabled true \
  --HealthChecks.Enabled true \
  --JsonRpc.EnabledModules='[Eth, Subscribe, Trace, TxPool, Web3, Personal, Proof, Net, Parity, Health, Rpc, Admin]' \
  --JsonRpc.AdditionalRpcUrls=http://127.0.0.1:8555|http|admin \
  --JsonRpc.EnginePort 8551

[Install]
WantedBy=default.target
```

Reload systemd to reflect the changes and start the service. Check status to make sure it’s running correctly.

```console
$ sudo systemctl daemon-reload
$ sudo systemctl start nethermind.service
$ sudo systemctl status nethermind.service
```

It should say active (running) in green text. If not then go back and repeat the steps to fix the problem. Press Q to quit (will not affect the nethermind service).

Enable the nethermind service to automatically start on reboot.

```console
$ sudo systemctl enable nethermind.service
```

You can watch the live messages from your Nethermind node logs using this command. Make sure nothing suspicious shows up in your logs.

```console
$ sudo journalctl -f -u nethermind.service -o cat | ccze -A
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
Description=Lighthouse Beacon Node (Hoodi)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=lighthousebeacon
Group=lighthousebeacon
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/lighthouse bn \
    --network hoodi \
    --datadir /var/lib/lighthouse \
    --http \
    --execution-endpoint http://127.0.0.1:8551 \
    --checkpoint-sync-url https://hoodi.beaconstate.ethstaker.cc \
    --metrics \
    --execution-jwt /var/lib/ethereum/jwttoken \
    --validator-monitor-auto \
    --boot-nodes=enr:-OS4QMJGE13xEROqvKN1xnnt7U-noc51VXyM6wFMuL9LMhQDfo1p1dF_zFdS4OsnXz_vIYk-nQWnqJMWRDKvkSK6_CwDh2F0dG5ldHOIAAAAADAAAACGY2xpZW502IpMaWdodGhvdXNljDcuMC4wLWJldGEuM4RldGgykNLxmX9gAAkQAAgAAAAAAACCaWSCdjSCaXCEhse4F4RxdWljgiMqiXNlY3AyNTZrMaECef77P8k5l3PC_raLw42OAzdXfxeQ-58BJriNaqiRGJSIc3luY25ldHMAg3RjcIIjKIN1ZHCCIyg,enr:-LK4QDwhXMitMbC8xRiNL-XGMhRyMSOnxej-zGifjv9Nm5G8EF285phTU-CAsMHRRefZimNI7eNpAluijMQP7NDC8kEMh2F0dG5ldHOIAAAAAAAABgCEZXRoMpDS8Zl_YAAJEAAIAAAAAAAAgmlkgnY0gmlwhAOIT_SJc2VjcDI1NmsxoQMoHWNL4MAvh6YpQeM2SUjhUrLIPsAVPB8nyxbmckC6KIN0Y3CCIyiDdWRwgiMo,enr:-LK4QPYl2HnMPQ7b1es6Nf_tFYkyya5bj9IqAKOEj2cmoqVkN8ANbJJJK40MX4kciL7pZszPHw6vLNyeC-O3HUrLQv8Mh2F0dG5ldHOIAAAAAAAAAMCEZXRoMpDS8Zl_YAAJEAAIAAAAAAAAgmlkgnY0gmlwhAMYRG-Jc2VjcDI1NmsxoQPQ35tjr6q1qUqwAnegQmYQyfqxC_6437CObkZneI9n34N0Y3CCIyiDdWRwgiMo

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

## Trying the Hoodi testnet

### Requesting testnet funds

Requesting or obtaining enough Hoodi ETH to perform your validator deposit can be challenging. We suggest you use the EthStaker #cheap-hoodi-validator free process. Join the [EthStaker Discord server](https://dsc.gg/ethstaker) and use the `/cheap-hoodi-deposit` slash command (start typing the command and it will show up above your input box). From there, follow the instructions from the bot. As an alternative, you can try obtaining 32 Hoodi ETH from this great faucet on https://hoodi-faucet.pk910.de/ . Hoodi ETH was also distributed to many people who previously interacted with the Holesky network. You might already have some Hoodi ETH in your wallet if you used Holesky so check first.

## Adding a validator

### Creating your validator keys and performing the deposit

There are 2 great tools to create your validator keys:

* GUI based: [Wagyu Key Gen](https://github.com/stake-house/wagyu-key-gen)
* CLI based: [ethstaker-deposit-cli](https://github.com/eth-educators/ethstaker-deposit-cli)

If you choose the *Wagyu Key Gen* application, make sure to select the *Hoodi* network and follow the instructions provided. If you are using the #cheap-hoodi-validator process, you will need to use `0x4D496CcC28058B1D74B7a19541663E21154f9c84` as your withdrawal address. This is only required for that process. When on Mainnet, you should use a withdrawal address you control if you want to use one.

If you choose the *ethstaker-deposit-cli* application, here is how to create your validator keys. Make sure to replace the `0x4D496CcC28058B1D74B7a19541663E21154f9c84` withdrawal address with your own address that you control if you need or want to:

```console
$ cd ~
$ wget https://github.com/eth-educators/ethstaker-deposit-cli/releases/download/v1.1.0/ethstaker_deposit-cli-08f1e66-linux-amd64.tar.gz
$ tar xvf ethstaker_deposit-cli-08f1e66-linux-amd64.tar.gz
$ rm ethstaker_deposit-cli-08f1e66-linux-amd64.tar.gz
$ cd ethstaker_deposit-cli-08f1e66-linux-amd64/
$ ./deposit new-mnemonic --num_validators 1 --chain hoodi --execution_address 0x4D496CcC28058B1D74B7a19541663E21154f9c84
$ ls -d $PWD/validator_keys/*
```

Make sure to store your keystore password and your mnemonic somewhere safe. You should end up with a deposit file (starts with `deposit_data-` and ends with `.json`) and one or more keystore files (starts with `keystore-` and ends with `.json`), 1 per validator. Copy them around if needed. Make sure your deposit file and your keystore files are in a known and accessible location on your machine.

Next we will need to perform your deposit. If you used the #cheap-hoodi-validator process, you can perform your deposit on https://cheap.hoodi.launchpad.ethstaker.cc/ . If you managed to obtained 32 Hoodi ETH, you can use the official Hoodi launchpad on https://hoodi.launchpad.ethereum.org/ .

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
    --network hoodi
$ sudo chown -R lighthousevalidator:lighthousevalidator /var/lib/lighthouse/validators
```

Create a systemd service config file to configure the Lighthouse validator client service.

```console
$ sudo nano /etc/systemd/system/lighthousevalidator.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`). Make sure to replace the `0x0000000000000000000000000000000000000000` address with your own Ethereum address that you control where you want to receive the transaction tips.

```ini
[Unit]
Description=Lighthouse Validator Client (Hoodi)
Wants=network-online.target
After=network-online.target

[Service]
User=lighthousevalidator
Group=lighthousevalidator
Type=simple
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/lighthouse vc \
    --network hoodi \
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

## Support

If you have any question or if you need additional support, make sure to get in touch with the EthStaker community on:

* Discord: [dsc.gg/ethstaker](https://dsc.gg/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)

## Credits

Based on [Somer Esat's guide](https://github.com/SomerEsat/ethereum-staking-guide).
