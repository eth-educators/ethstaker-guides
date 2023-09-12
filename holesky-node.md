# Guide on how to setup a Holeksy testnet node (Nethermind/Lighthouse)

[Holešky](https://github.com/eth-clients/holesky) is a new Ethereum testnet meant to replace Goerli as a staking, infrastructure and protocol-developer testnet.

This guide is meant for people with little or some experience in running Ethereum clients and using the command-line interface (CLI). It will show you step by step how to setup your machine to join the *Holesky* testnet by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd and APT (like Ubuntu 22.04 or Debian 12) on a modern x86 CPU (Intel, AMD). A clean install of your operating system on a dedicated machine or a virtual machine before proceeding is preferable.

## Overview

We will use the latest version for Nethermind and the latest version for Lighthouse. We will configure them to connect to the *Holesky* testnet.

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
$ sudo apt -y install wget curl ccze unzip libsnappy-dev
```

## Installing Nethermind

Download [the latest release version for Nethermind](https://github.com/NethermindEth/nethermind/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the linux-x64 version.

```console
$ cd ~
$ wget https://github.com/NethermindEth/nethermind/releases/download/1.20.3/nethermind-1.20.3-e8c161a5-linux-x64.zip
$ sudo mkdir -p /usr/share/nethermind
$ sudo unzip nethermind-1.20.3-e8c161a5-linux-x64.zip -d /usr/share/nethermind
$ rm nethermind-1.20.3-e8c161a5-linux-x64.zip
```

## Installing Lighthouse

Download [the latest release version for Lighthouse](https://github.com/sigp/lighthouse/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the linux x86_64 version.

```console
$ cd ~
$ wget https://github.com/sigp/lighthouse/releases/download/v4.4.1/lighthouse-v4.4.1-x86_64-unknown-linux-gnu.tar.gz
$ tar xvf lighthouse-v4.4.1-x86_64-unknown-linux-gnu.tar.gz
$ rm lighthouse-v4.4.1-x86_64-unknown-linux-gnu.tar.gz
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
Description=Nethermind Execution Client (Holesky)
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
ExecStart=/usr/share/nethermind/Nethermind.Runner \
  --config holesky \
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
Description=Lighthouse Beacon Node (Holesky)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=lighthousebeacon
Group=lighthousebeacon
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/lighthouse bn \
    --network holesky \
    --datadir /var/lib/lighthouse \
    --http \
    --execution-endpoint http://127.0.0.1:8551 \
    --metrics \
    --execution-jwt /var/lib/ethereum/jwttoken \
    --gui \
    --validator-monitor-auto

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

## Trying the Holesky testnet

### Requesting testnet funds

TODO (Waiting on testnet launch and public faucets)

## Adding a validator

TODO (Waiting on testnet launch and public launchpad)

## Support

If you have any question or if you need additional support, make sure to get in touch with the EthStaker community on:

* Discord: [discord.io/ethstaker](https://discord.io/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)

## Credits

Based on [Somer Esat's guide](https://github.com/SomerEsat/ethereum-staking-guide).
