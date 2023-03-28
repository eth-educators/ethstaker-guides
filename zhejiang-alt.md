# Guide on how to join the Zhejiang testnet (Besu/Teku)

[*Zhejiang*](https://zhejiang.ethpandaops.io/) is public Ethereum testnet to test the forks that will include changes for [withdrawals](https://ethereum.org/en/staking/#accordion-panel-:R17alelajkau:). Zhejiang went through the Shanghai fork on the execution layer side and the Capella fork on the consensus layer side. Both of these forks happened at the same time and they included [various features to be tested](https://notes.ethereum.org/@launchpad/zhejiang#What-is-in-the-Zhejiang-testnet) including withdrawals and BLS to execution changes. You can expect Sepolia, Goerli and Mainnet to go through these forks in a similar manner. You can find some of the common questions and answers on this in the [ETH Withdrawals FAQ](https://notes.ethereum.org/@launchpad/withdrawals-faq).

This guide is meant for people with little or some experience in running Ethereum clients and using the command-line interface (CLI). It will show you step by step how to setup your machine to join the *Zhejiang* testnet by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd and APT (like Ubuntu 20.04 or Ubuntu 22.04, but it should work on most recent debian derivatives) on a modern x86 CPU (Intel, AMD). A clean install of your operating system on a dedicated machine or a virtual machine before proceeding is preferable.

## Overview

We will use recent versions for Besu and for Teku. We will configure them to connect to the *Zhejiang* testnet. This is an alternative guide to [the main one who uses the Geth/Lighthouse combo](zhejiang.md) for its clients.

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
$ sudo apt -y install software-properties-common wget curl ccze apt-transport-https libjemalloc-dev git
```

Install Adoptium JDK (Java).

```console
$ sudo mkdir -p /etc/apt/keyrings
$ wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | sudo tee /etc/apt/keyrings/adoptium.asc
$ echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | sudo tee /etc/apt/sources.list.d/adoptium.list
$ sudo apt -y update
$ sudo apt -y install temurin-17-jdk
```

## Zhejiang configuration details

Obtain the Zhejiang configuration files and make them accessible.

```console
$ cd ~
$ git clone https://github.com/ethpandaops/withdrawals-testnet.git
$ sudo mkdir -p /var/lib/ethereum/zhejiang
$ sudo cp -R ~/withdrawals-testnet/zhejiang-testnet/custom_config_data /var/lib/ethereum/zhejiang
```

## Installing Besu

Download [the latest release version for Besu](https://github.com/hyperledger/besu/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the download link that ends with `tar.gz`.

```console
$ cd ~
$ wget https://hyperledger.jfrog.io/hyperledger/besu-binaries/besu/23.1.2/besu-23.1.2.tar.gz
$ tar xvf besu-23.1.2.tar.gz
$ rm besu-23.1.2.tar.gz
```

Install this Besu version globally.

```console
$ sudo cp -a ./besu-23.1.2 /usr/local/bin/besu
$ rm -rf ./besu-23.1.2
```

## Installing Teku

Download [the latest release version for Teku](https://github.com/ConsenSys/teku/releases) and extract it. If the latest version is more recent than what is used here, use that version and adjust for the new URL and archive name. Make sure to use the download link from the *Downloads* section of the release description. It should be a file that ends with `tar.gz` and it should **not** be the one called 'Source code'.

```console
$ cd ~
$ wget https://artifacts.consensys.net/public/teku/raw/names/teku.tar.gz/versions/23.3.1/teku-23.3.1.tar.gz
$ tar xvf teku-23.3.1.tar.gz
$ rm teku-23.3.1.tar.gz
```

Install this Teku version globally.

```console
$ sudo cp -a ./teku-23.3.1 /usr/local/bin/teku
$ rm -rf ./teku-23.3.1
```

## Creating the JWT token file

Create a JWT token file in a neutral location and make it readable to everyone. We will use the `/var/lib/ethereum/zhejiang/jwttoken` location to store the JWT token file.

```
$ sudo mkdir -p /var/lib/ethereum/zhejiang
$ openssl rand -hex 32 | tr -d "\n" | sudo tee /var/lib/ethereum/zhejiang/jwttoken
$ sudo chmod +r /var/lib/ethereum/zhejiang/jwttoken
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
Description=Besu Ethereum Client (Zhejiang)
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
    --network-id=1337803 \
    --genesis-file=/var/lib/ethereum/zhejiang/custom_config_data/besu.json \
    --sync-mode=FULL \
    --rpc-http-enabled=true \
    --engine-rpc-port=8551 \
    --engine-host-allowlist=localhost,127.0.0.1 \
    --data-path=/var/lib/besu \
    --data-storage-format=BONSAI \
    --metrics-enabled=true \
    --engine-jwt-secret=/var/lib/ethereum/zhejiang/jwttoken \
    --bootnodes="enode://691c66d0ce351633b2ef8b4e4ef7db9966915ca0937415bd2b408df22923f274873b4d4438929e029a13a680140223dcf701cabe22df7d8870044321022dfefa@64.225.78.1:30303,enode://89347b9461727ee1849256d78e84d5c86cc3b4c6c5347650093982b726d71f3d08027e280b399b7b6604ceeda863283dcfe1a01e93728b4883114e9f8c7cc8ef@146.190.238.212:30303,enode://c2892072efe247f21ed7ebea6637ade38512a0ae7c5cffa1bf0786d5e3be1e7f40ff71252a21b36aa9de54e49edbcfc6962a98032adadfa29c8524262e484ad3@165.232.84.160:30303,enode://71e862580d3177a99e9837bd9e9c13c83bde63d3dba1d5cea18e89eb2a17786bbd47a8e7ae690e4d29763b55c205af13965efcaf6105d58e118a5a8ed2b0f6d0@68.183.13.170:30303,enode://2f6cf7f774e4507e7c1b70815f9c0ccd6515ee1170c991ce3137002c6ba9c671af38920f5b8ab8a215b62b3b50388030548f1d826cb6c2b30c0f59472804a045@161.35.147.98:30303"

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

## Trying the Zhejiang testnet

### Requesting testnet funds

You can request Zhejiang ETH from [the main faucet](https://faucet.zhejiang.ethpandaops.io/). You can request Zhejiang ETH from [pk910's faucet](https://zhejiang-faucet.pk910.de/). You can request Zhejiang ETH from [EthStaker Discord server](https://discord.io/ethstaker) in the #request-zhejiang-eth💸 channel. You will need at least 32 Zhejiang ETH if you want to do a validator deposit for Zhejiang.

## Adding a validator

### Creating your validator keys and performing the deposit

There are 2 great tools to create your validator keys:

* GUI based: [Wagyu Key Gen](https://github.com/stake-house/wagyu-key-gen)
* CLI based: [staking-deposit-cli](https://github.com/ethereum/staking-deposit-cli)

If you choose the *Wagyu Key Gen* application, make sure to select the *Zhejiang* network and follow the instructions provided.

If you choose the *staking-deposit-cli* application, here is how to create your validator keys (without a withdrawal address):

```console
$ cd ~
$ wget https://github.com/ethereum/staking-deposit-cli/releases/download/v2.5.0/staking_deposit-cli-d7b5304-linux-amd64.tar.gz
$ tar xvf staking_deposit-cli-d7b5304-linux-amd64.tar.gz
$ rm staking_deposit-cli-d7b5304-linux-amd64.tar.gz
$ cd staking_deposit-cli-d7b5304-linux-amd64/
$ ./deposit new-mnemonic --num_validators 1 --chain zhejiang
$ ls -d $PWD/validator_keys/*
```

Make sure to store your keystore password and your mnemonic somewhere safe. You should end up with a deposit file (starts with `deposit_data-` and ends with `.json`) and one or more keystore files (starts with `keystore-` and ends with `.json`), 1 per validator. Copy them around if needed. Make sure your deposit file and your keystore files are in a known and accessible location on your machine.

Next we will do the deposit using the Zhejiang launchpad. Make sure you have access to a browser with MetaMask, your account with the funds from the faucet and the deposit file we just created.

Go to [the Zhejiang launchpad](https://zhejiang.launchpad.ethereum.org/). Follow the instructions, make sure *Zhejiang* is the selected network in MetaMask (if you don't have that network in your dropdown list, go to https://zhejiang.ethpandaops.io/ and click the *Add network to Metamask*) and use the deposit file to perform your deposit.

You can check that your deposit transaction went through on [the transaction explorer](https://blockscout.com/eth/zhejiang-testnet/address/0x4242424242424242424242424242424242424242).

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

Create a systemd service config file to configure the Teku node service.

```console
$ sudo nano /etc/systemd/system/teku.service
```

Paste the following service configuration into the file. Exit and save once done (`Ctrl` + `X`, `Y`, `Enter`). Make sure to replace the `0x0000000000000000000000000000000000000000` address with your own Ethereum address that you control where you want to receive the transaction tips.

```ini
[Unit]
Description=Teku Ethereum Client (Zhejiang)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=teku
Group=teku
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/teku/bin/teku \
    --network /var/lib/ethereum/zhejiang/custom_config_data/config.yaml \
    --data-path /var/lib/teku \
    --validator-keys /var/lib/teku/validator_keys:/var/lib/teku/validator_keys \
    --rest-api-enabled true \
    --ee-endpoint http://127.0.0.1:8551 \
    --metrics-enabled true \
    --validators-graffiti EthStaker \
    --initial-state=https://beacon.zhejiang.ethpandaops.io/eth/v2/debug/beacon/states/finalized \
    --validators-proposer-default-fee-recipient 0x0000000000000000000000000000000000000000 \
    --ee-jwt-secret-file /var/lib/ethereum/zhejiang/jwttoken \
    --p2p-discovery-bootnodes="enr:-Iq4QMCTfIMXnow27baRUb35Q8iiFHSIDBJh6hQM5Axohhf4b6Kr_cOCu0htQ5WvVqKvFgY28893DHAg8gnBAXsAVqmGAX53x8JggmlkgnY0gmlwhLKAlv6Jc2VjcDI1NmsxoQK6S-Cii_KmfFdUJL2TANL3ksaKUnNXvTCv1tLwXs0QgIN1ZHCCIyk,enr:-Ly4QOS00hvPDddEcCpwA1cMykWNdJUK50AjbRgbLZ9FLPyBa78i0NwsQZLSV67elpJU71L1Pt9yqVmE1C6XeSI-LV8Bh2F0dG5ldHOIAAAAAAAAAACEZXRoMpDuKNezAAAAckYFAAAAAAAAgmlkgnY0gmlwhEDhTgGJc2VjcDI1NmsxoQIgMUMFvJGlr8dI1TEQy-K78u2TJE2rWvah9nGqLQCEGohzeW5jbmV0cwCDdGNwgiMog3VkcIIjKA,enr:-MK4QMlRAwM7E8YBo6fqP7M2IWrjFHP35uC4pWIttUioZWOiaTl5zgZF2OwSxswTQwpiVCnj4n56bhy4NJVHSe682VWGAYYDHkp4h2F0dG5ldHOIAAAAAAAAAACEZXRoMpDuKNezAAAAckYFAAAAAAAAgmlkgnY0gmlwhJK-7tSJc2VjcDI1NmsxoQLDq7LlsXIXAoJXPt7rqf6CES1Q40xPw2yW0RQ-Ly5S1YhzeW5jbmV0cwCDdGNwgiMog3VkcIIjKA,enr:-MS4QCgiQisRxtzXKlBqq_LN1CRUSGIpDKO4e2hLQsffp0BrC3A7-8F6kxHYtATnzcrsVOr8gnwmBnHYTFvE9UmT-0EHh2F0dG5ldHOIAAAAAAAAAACEZXRoMpDuKNezAAAAckYFAAAAAAAAgmlkgnY0gmlwhKXoVKCJc2VjcDI1NmsxoQK6J-uvOXMf44iIlilx1uPWGRrrTntjLEFR2u-lHcHofIhzeW5jbmV0c4gAAAAAAAAAAIN0Y3CCIyiDdWRwgiMo,enr:-LK4QOQd-elgl_-dcSoUyHDbxBFNgQ687lzcKJiSBtpCyPQ0DinWSd2PKdJ4FHMkVLWD-oOquXPKSMtyoKpI0-Wo_38Bh2F0dG5ldHOIAAAAAAAAAACEZXRoMpDuKNezAAAAckYFAAAAAAAAgmlkgnY0gmlwhES3DaqJc2VjcDI1NmsxoQNIf37JZx-Lc8pnfDwURcHUqLbIEZ1RoxjZuBRtEODseYN0Y3CCIyiDdWRwgiMo,enr:-KG4QLNORYXUK76RPDI4rIVAqX__zSkc5AqMcwAketVzN9YNE8FHSu1im3qJTIeuwqI5JN5SPVsiX7L9nWXgWLRUf6sDhGV0aDKQ7ijXswAAAHJGBQAAAAAAAIJpZIJ2NIJpcIShI5NiiXNlY3AyNTZrMaECpA_KefrVAueFWiLLDZKQPPVOxMuxGogPrI474FaS-x2DdGNwgiMog3VkcIIjKA" \
    --p2p-static-peers="/ip4/64.225.78.1/tcp/9000/p2p/16Uiu2HAkwbLbPXhPua835ErpoywHmgog4oydobcj3uKtww8UmW3b,/ip4/146.190.238.212/tcp/9000/p2p/16Uiu2HAm8bVLELrPczXQesjUYF8EetaKokgrdgZKj8814ZiGNggk,/ip4/165.232.84.160/tcp/9000/p2p/16Uiu2HAm7xM7nYVz3U9iWGH6NwExZTWtJGGeZ7ejQrcuUFUwtQmH,/ip4/68.183.13.170/udp/9000/p2p/16Uiu2HAmHXzTmWAtVexas5YskEpbcyDQ5Qck3jdLgErWumjKExUx"

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

## Adding a withdrawal address

In order to add a withdrawal address on a validator, you need to perform a BLS to execution change. Ideally, you want to perform this on an offline machine that was never online and never will be such as a live OS booted from a USB drive ([tails](https://tails.boum.org/) is a nice operating system for this). This is to protect your mnemonic and to avoid potentially compromising it. For testing purposes where there is nothing of real value at stake like on Zhejiang, you can avoid this precaution.

Download and extract a special version of staking-deposit-cli.

```console
$ cd ~
$ wget https://github.com/ethereum/staking-deposit-cli/releases/download/v2.5.0/staking_deposit-cli-d7b5304-linux-amd64.tar.gz
$ tar xvf staking_deposit-cli-d7b5304-linux-amd64.tar.gz
$ rm staking_deposit-cli-d7b5304-linux-amd64.tar.gz
```

Find all the following information for the next commmand:

1. Your mnemonic.
2. Your validator index. This should be 0 if you only created 1 validator from this mnemonic.
3. Your BLS withdrawal credentials. This can be found on the [Zhejiang beaconcha.in website](https://zhejiang.beaconcha.in/). Search for your validator by public key, validator indice or deposit address. On your validator page, click on the deposits tab. The withdrawal credentials should be right there. It should start with `0x00` meaning that your validator does not currently have a withdrawal address.
4. Your validator indice. This is a number assigned to your validator by the consensus layer during activation. You can also find this on [Zhejiang beaconcha.in website](https://zhejiang.beaconcha.in/). It's the number at the top when you reach your validator page.
5. Your withdraw address where you want your rewards and eventually your deposit to go to.

Run the following command by replacing every `<number>` element with the information above.

```console
$ cd ~/staking_deposit-cli-d7b5304-linux-amd64
$ ./deposit --language=english generate-bls-to-execution-change \
  --chain=zhejiang \
  --mnemonic="<1>" \
  --bls_withdrawal_credentials_list="<3>" \
  --validator_start_index=<2> \
  --validator_indices=<4> \
  --execution_address="<5>"
```

A concret example of this would be something like this.

```
./deposit --language=english generate-bls-to-execution-change \
  --chain=zhejiang \
  --mnemonic="midnight stuff system off insane pen normal sunny century staff unfold youth spread myth ranch pony never media appear curve mule diamond century unfold" \
  --bls_withdrawal_credentials_list="0x00f48911b8ac7c05407d21f206253bff655d848fb99a9d3a0caaf35171c04bf5" \
  --validator_start_index=0 \
  --validator_indices=62180 \
  --execution_address="0x56883e030E000fccfD22fC14Fa021568045d48FE"
```

During this command execution, you will be asked to enter your withdraw address again. Double check you have the correct and enter it again. It will end with a message like this one.

```
Success!
Your SignedBLSToExecutionChange JSON file can be found at: /home/<username>/staking_deposit-cli-d7b5304-linux-amd64/bls_to_execution_changes
```

Display the content of that file.

```console
$ awk '{print}' $HOME/staking_deposit-cli-d7b5304-linux-amd64/bls_to_execution_changes/*.json
```

Use the beaconcha.in tool to broadcast your BLS to execution change. Go to https://zhejiang.beaconcha.in/tools/broadcast and paste the content of your file that was just displayed. Refresh your validator page on the [Zhejiang beaconcha.in website](https://zhejiang.beaconcha.in/). It should eventually show a withdrawal address associated with your validator and `0x01` withdrawal credentials.

## Performing a volontary exit

Once you have a withdrawal address associated with your validator, you can try and perform a volontary exit to receive your full deposit and all the remaining rewards.

Teku comes with a nice tool to perform a voluntary exit. You will need your validator keystore file and associated password file. If you don't have it anymore, it's stored on disk. You can find all this information by calling this command. It will show you the path to your keystore(s) and the associated password file(s).

```console
$ sudo ls /var/lib/teku/validator_keys
```

That directory should have a password file for each keystore as created in the [Configuring your Teku node](#configuring-your-teku-node) section. The password file is the one that ends with the `.txt` extension and the keystore file is the one that ends with the `.json` extension. Once you have the path to your keystore and the password file, call the `voluntary-exit` command and follow the instructions from there. Make sure to replace `<path-to-keystore-file>` with the actual path to your keystore and `<path-to-password-file>` with the actual path to your password file.

```
$ sudo /usr/local/bin/teku/bin/teku voluntary-exit \
  --beacon-node-api-endpoint=http://127.0.0.1:5051 \
  --validator-keys=<path-to-keystore-file>:<path-to-password-file>
```

Voluntary exits and withdrawals take a while before actually completing even after performing this step. To learn more about these delays and the various validator states, check out the great [ladislaus blog post](https://mirror.xyz/ladislaus.eth/wmoBbUBes2Wp1_6DvP6slPabkyujSU7MZOFOC3QpErs) on this.

## Support

If you have any question or if you need additional support, make sure to get in touch with people involved with this:

* EthStaker Discord: [discord.io/ethstaker](https://discord.io/ethstaker) in the #zhejiang-🔑 channel.
* Eth R&D Discord: [discord.gg/qGpsxSA](https://discord.gg/qGpsxSA) in the #testing channel under the *Shanghai* category.

## Credits

Based on the following documents:

- [Somer Esat's guide](https://github.com/SomerEsat/ethereum-staking-guide).
- [How to run a node on the Zhejiang testnet?](https://notes.ethereum.org/@launchpad/zhejiang).
- [How to use staking-deposit-cli to generate SignedBLSToExecutionChange](https://notes.ethereum.org/@launchpad/btec).
- [Voluntarily exit a validator](https://docs.teku.consensys.net/HowTo/Voluntary-Exit#docusaurus_skipToContent_fallback) from Teku documentation.
