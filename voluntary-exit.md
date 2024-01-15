# Guide on how to perform a voluntary exit for your validator

At some point during a normal validator's lifecycle, you will want to exit and potentially obtain your balance back, the initial deposit plus any remaining rewards, assuming you have a withdrawal address associated with your validator. This document will guide you through some steps to perform a voluntary exit of your validator.

This guide is meant for people who are staking on Ethereum either through their own node or with a non-custodial service. It will explain in details which steps or actions you should take in order to perform a voluntary exit.

There are a lot of different ways to perform a voluntary exit. Each consensus client has their own documentation on this. This guide will focus on using [ethdo](https://github.com/wealdtech/ethdo) and [the beaconcha.in website](https://beaconcha.in/) to perform this task for simplicity. Check out the documentation for each client to learn more about how to do this natively.

- [Prysm](https://docs.prylabs.network/docs/wallet/exiting-a-validator)
- [Nimbus](https://nimbus.guide/voluntary-exit.html)
- [Lodestar](https://chainsafe.github.io/lodestar/reference/cli/#validator-voluntary-exit)
- [Teku](https://docs.teku.consensys.net/HowTo/Voluntary-Exit)
- [Lighthouse](https://lighthouse-book.sigmaprime.io/voluntary-exit.html)

A video tutorial of this guide can be seen on https://youtu.be/KoBAacMWA_k .

## Overview

We will use 3 tools with this guide: [ethdo](https://github.com/wealdtech/ethdo), [the beaconcha.in broadcast tool](https://beaconcha.in/tools/broadcast) and [Tails](https://tails.boum.org/).

**ethdo** is a command-line tool for managing common tasks in Ethereum. In this guide, we will use it to sign your voluntary exit from all the validator details we will provide.

**beaconcha.in** is an open-source Ethereum explorer. In this guide, we will use it to broadcast the voluntary exit using their *Broadcast Signed Messages* tool.

**Tails** is a portable operating system that protects against surveillance and malicious actors. In this guide, we will use it to perform all the sensible operations offline to prevent exposing your secrets.

The first step will be to prepare and generate a file for offline signing using ethdo. The second step will be to boot a computer into Tails, sign and generate your voluntary exit file using ethdo. The third step will be to broadcast this voluntary exit. You will need 2 USB sticks, one to boot the Tails operating system from and the second one to hold ethdo and the documents we will need. You will also need a PC that supports [AMD64 instructions](https://tails.boum.org/doc/about/requirements/index.en.html) to boot into.

### Required details

To perform a voluntary exit, you need the validator signing key. This can be obtained through 2 main ways, either with *your mnemonic*, the 24 words used to create your validator keys, or with *the keystore file and the associated password*. If you do not have either of them, you are likely out of luck and you are unlikely to ever be able to perform a voluntary exit.

You will also need the validator public key or the validator index as identified by the beacon chain. Both of these can be found on [the beaconcha.in website](https://beaconcha.in/). You can find your validator's page by searching by public key, deposit address, validator index or a few other ways. From there, you should be able to find your validator index or public key at the top of the validator's page.

**NEVER** enter your mnemonic into a machine that was or will be online. This would potentially expose you to a malicious actor stealing your money.

### Tooling

For most of this guide, we will use ethdo *version 1.34.1*. You should use the latest stable version available from https://github.com/wealdtech/ethdo/releases and adapt this guide to that latest version if a new version is released.

## Preparing for offline generation

Using ethdo, we will connect to a beacon node endpoint and create a file named `offline-preparation.json` to be used later. If you do not have direct access to your own beacon node endpoint, ethdo will fallback using its own public endpoint assuming you are connected to the internet.

### On Windows

Open a powershell command prompt, press `⊞ Win`+`R`, type `powershell` and press `↵ Enter`. You will see a blue or black window where you can type commands.

Download the etho archive and the associated checksum file.

```powershell
$ProgressPreference = 'SilentlyContinue'; iwr https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-windows-exe.zip -outfile ethdo-1.34.1-windows-exe.zip
$ProgressPreference = 'SilentlyContinue'; iwr https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-windows-exe-zip.sha256 -outfile ethdo-1.34.1-windows-exe-zip.sha256
```

Compute the archive hash value and compare it to the expected value.

```powershell
Get-FileHash .\ethdo-1.34.1-windows-exe.zip | Select -Property @{n='hash';e={$_.hash.tolower()}} | Select -ExpandProperty "hash"
cat .\ethdo-1.34.1-windows-exe-zip.sha256
```

Both of these output values should match. As of today and for version `1.34.1`, they should both be `2bdace8bb85fb4362e769c8321db90e4e4be7ab62842bf73905258fad502cd55`. If they do not match, there might be a security issue and you should seek further support.

Extract the ethdo archive and generate the preparation file.

```powershell
Expand-Archive .\ethdo-1.34.1-windows-exe.zip
cd .\ethdo-1.34.1-windows-exe\
.\ethdo.exe validator exit --prepare-offline
```

You should see a message saying *offline-preparation.json generated* if everything worked fine.

Download the Linux version of ethdo as well to prepare for when we will need to execute this offline on Tails.

```powershell
$ProgressPreference = 'SilentlyContinue'; iwr https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-linux-amd64.tar.gz -outfile ethdo-1.34.1-linux-amd64.tar.gz
$ProgressPreference = 'SilentlyContinue'; iwr https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-linux-amd64.tar.gz.sha256 -outfile ethdo-1.34.1-linux-amd64.tar.gz.sha256
```

Open an explorer window in this current directory to easily access the files we just obtained.

```powershell
start .
```

### On macOS

Open a terminal. Download the etho archive and the associated checksum file.

```console
curl -O -L https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-darwin-amd64.tar.gz
curl -O -L https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-darwin-amd64.tar.gz.sha256
```

Make sure ethdo checksum matches.

```console
shasum -a 256 ethdo-1.34.1-darwin-amd64.tar.gz
cat ethdo-1.34.1-darwin-amd64.tar.gz.sha256
```

Both of these output values should have matching checksum. As of today and for version `1.34.1`, they should both be `fa6394fa4bae96d2ec840050c53cb3308c6448884449066bb8cb5997529c1b05`. If they do not match, there might be a security issue and you should seek further support.

Extract the ethdo archive and generate the preparation file.

```console
tar xvf ethdo-1.34.1-darwin-amd64.tar.gz
./ethdo validator exit --prepare-offline
```

You should see a message saying *offline-preparation.json generated* if everything worked fine.

Download the Linux version of ethdo as well to prepare for when we will need to execute this offline on Tails.

```console
curl -O -L https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-linux-amd64.tar.gz
curl -O -L https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-linux-amd64.tar.gz.sha256
```

Open an finder window in this current directory to easily access the files we just obtained.

```console
open .
```

### On Linux

Open a terminal. Download the etho archive and the associated checksum file.

```console
wget https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-linux-amd64.tar.gz
wget https://github.com/wealdtech/ethdo/releases/download/v1.34.1/ethdo-1.34.1-linux-amd64.tar.gz.sha256
```

Make sure ethdo checksum matches.

```console
sha256sum ethdo-1.34.1-linux-amd64.tar.gz
cat ethdo-1.34.1-linux-amd64.tar.gz.sha256
```

Both of these output values should have matching checksum. As of today and for version `1.34.1`, they should both be `6af0e3fbd841ae2267028f59ef037ad897dc7c1c60eb1b7a90f30234ed4d427a`. If they do not match, there might be a security issue and you should seek further support.

Extract the ethdo archive and generate the preparation file.

```console
tar xvf ethdo-1.34.1-linux-amd64.tar.gz
./ethdo validator exit --prepare-offline
```

You should see a message saying *offline-preparation.json generated* if everything worked fine.

### Prepared alternative

If you are having issues creating your `offline-preparation.json`, you can use these alternative files. They are regenerated every day at 0:00 UTC. You will need to extract the archive first (either the `.tar.gz` file on Linux or macOS or the `.zip` file on Windows) to get the `offline-preparation.json` file.

For Mainnet:
- https://files.ethstaker.cc/offline-preparation-mainnet.tar.gz
- https://files.ethstaker.cc/offline-preparation-mainnet.tar.gz.sha256
- https://files.ethstaker.cc/offline-preparation-mainnet.zip
- https://files.ethstaker.cc/offline-preparation-mainnet.zip.sha256

For Goerli:
- https://files.ethstaker.cc/offline-preparation-goerli.tar.gz
- https://files.ethstaker.cc/offline-preparation-goerli.tar.gz.sha256
- https://files.ethstaker.cc/offline-preparation-goerli.zip
- https://files.ethstaker.cc/offline-preparation-goerli.zip.sha256

### Finalizing your documents

Copy those files on your second USB stick.

- `offline-preparation.json`
- `ethdo-1.34.1-linux-amd64.tar.gz`
- `ethdo-1.34.1-linux-amd64.tar.gz.sha256`

If you want to use your keystore file and the associated password to generate your voluntary exit file, make sure to copy the keystore file on the same USB stick that you put the `offline-preparation.json` file. Try avoiding entering the associated password in a file on the same USB stick in clear text.

If instead you want to use your mnemonic to generate your voluntary exit, avoid entering it in a file on your USB stick. Try to keep it away from any electronic document and any electronic medium. If you have it on a paper or in steel, keep it close as we will need it in the next step.

## Signing and generating your voluntary exit file

Install Tails on your first USB stick which should be empty by following [the instructions from their website](https://tails.boum.org/install/index.en.html). Unplug any wired connection and restart a machine on your Tails USB stick. During start, you will be asked to select your language, keyboard layout and formats. Click *Start Tails* to reach the Desktop.

Plug in your second USB stick and copy all the documents and tools we included in the home folder.

### Verifying and extracting ethdo

Start a terminal. Make sure ethdo checksum matches.

```console
sha256sum ethdo-1.34.1-linux-amd64.tar.gz
cat ethdo-1.34.1-linux-amd64.tar.gz.sha256
```

Both of these output values should have matching checksum. As of today and for version `1.34.1`, they should both be `6af0e3fbd841ae2267028f59ef037ad897dc7c1c60eb1b7a90f30234ed4d427a`. If they do not match, there might be a security issue and you should seek further support.

Extract the ethdo archive.

```console
tar xvf ethdo-1.34.1-linux-amd64.tar.gz
```

From here you can either use [your keystore file and the associated password](#generating-a-voluntary-exit-using-your-keystore-file-and-the-associated-password) or use [your mnemonic](#generating-a-voluntary-exit-using-your-mnemonic) to generate your voluntary exit file.

### Generating a voluntary exit using your keystore file and the associated password

There are 3 inputs for the next command that will generate your voluntary exit file.

1. Your keystore filename. This is going to be *KEYSTORE_FILENAME* in the template.
2. Your keystore password. This is going to be *KEYSTORE_PASSWORD* in the template.
3. The resulting filename. This is going to be *RESULTING_FILENAME* in the template.

As a template, the command call looks like:

```console
./ethdo validator exit --validator="KEYSTORE_FILENAME" --passphrase='KEYSTORE_PASSWORD' --json --offline > RESULTING_FILENAME
```

Here is a concrete example of using this command.

```console
./ethdo validator exit --validator="keystore-m_12381_3600_0_0_0-1679368539.json" --passphrase='testing123' --json --offline > 459921-exit.json
```

In this example, it would result in a file named `459921-exit.json` in your home folder for performing the voluntary exit of the validator that is using the imported keystore file.

Copy that resulting file back on your second USB stick. We will need it on the next step to broadcast the voluntary exit.

### Generating a voluntary exit using your mnemonic

There are 3 inputs for the next command that will generate your voluntary exit file.

1. Your validator index as identified on the beacon chain or your validator public key. This is going to be *VALIDATOR_INDEX* in the template.
2. Your mnemonic. This is going to be *MNEMONIC* in the template.
3. The resulting filename. This is going to be *RESULTING_FILENAME* in the template.

As a template, the command call looks like:

```console
./ethdo validator exit --validator=VALIDATOR_INDEX --json --offline --mnemonic="MNEMONIC" > RESULTING_FILENAME
```

Here is a concrete example of using this command.

```console
./ethdo validator exit --validator=459921 --json --offline --mnemonic="silent hill auto ability front sting tunnel empower venture once wise local suffer repeat deny deliver hawk silk wedding random coil you town narrow" > 459921-exit.json
```

In this example, it would result in a file named `459921-exit.json` in your home folder for performing the voluntary exit of validator 459921.

Copy that resulting file back on your second USB stick. We will need it on the next step to broadcast the voluntary exit.

## Broadcasting your voluntary exit

Shut down Tails and go back to your main connected machine. Plug your second USB stick. Browse to https://beaconcha.in/tools/broadcast, the beaconcha.in broadcast tool. Drag and drop or select your voluntary exit json file on that website from your USB stick. Click the *Submit & Broadcast* button. 

Your validator will enter the exit queue and it will eventually fully exit the network. Your validator is expected to perform its duties even after you broadcast your voluntary exit. Make sure to let your validator run and perform its regular duties as long as it's not fully exited.

### Using a beacon node for broadcasting

If you have access to a beacon node, a consensus client currently in sync with an exposed beacon node API endpoint, you can manually submit your voluntary exit with that beacon node. That alternative process is usually harder than just using beaconcha.in broadcast tool. If you have a node running under Linux this can be done with the curl tool on the command line interface. You will need your voluntary exit file on the machine where you want to execute this command.

There are 2 inputs for the next command that will broadcast your voluntary exit using a beacon node.

1. Your beacon node API endpoint URL. This is going to be *BEACON_NODE* in the template.
2. The path to your voluntary exit file. This is going to be *EXIT_FILE* in the template.

As a template, the command call looks like:

```console
curl -X POST BEACON_NODE/eth/v1/beacon/pool/voluntary_exits -H "Content-Type: application/json" -d @EXIT_FILE
```

Here is a concrete example of using this command.

```console
curl -X POST http://localhost:5052/eth/v1/beacon/pool/voluntary_exits -H "Content-Type: application/json" -d @459921-exit.json
```

## Full exit / withdrawal process

There are multiple steps and delays when performing a voluntary exit and waiting for the final withdrawal. Check out [this great graphic](https://media.discordapp.net/attachments/939440360789266462/1105846872700108850/exit1.png) by Ladislaus to find more about those steps.

## Support

If you have any question or if you need additional support, make sure to get in touch with the ethstaker community on:

* Discord: [dsc.gg/ethstaker](https://dsc.gg/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)
