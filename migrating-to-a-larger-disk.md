# Guide on How to Migrate to a Larger Disk for an Ethereum Validator

Disk usage is a constant concern for stakers and node operators. The blockchain data keeps growing each day with new transactions and states to store. Stakers and node operators are mainly those responsible for storing this data. During the life of a staker or a node operator, it is likely that you will need more space for this concern. Migrating to a larger disk might become the last solution for some.

This guide is meant for people with little or no experience migrating to a larger disk. It will show you step by step how to check your disk usage, which solutions are possible to manage disk usage, which tools you will need to migrate to a larger disk, and the process of migrating to a larger disk. It will assume you are using a modern Linux distribution to run your staker or node operating system. Many of these instructions and steps are possible on Windows or macOS, but this is out of scope for this guide.

If you know what you are doing, you can simply read the [Migrating to a Larger Disk](#migrating-to-a-larger-disk) section.

## Current Expected Disk Usage

On Mainnet, you should expect the current disk usage to be around **1 TB to 1.7 TB**, depending on which client and configuration you are using, excluding archive nodes. This should be accurate as of today, January 2024. It might be possible to still use a 1 TB disk in some extremely specific scenarios, but any serious staker or node operator should be using a good 2+ TB SSD. If you are building a new machine, you should consider buying or starting with a good 4 TB SSD to avoid having to perform this kind of maintenance in the short or medium term.

## Solutions to Check Before Buying a New Disk and Migrating

### Pruning

Some clients like Geth and Nethermind support pruning your existing database to lower its disk usage. The general idea is that these clients accumulate data that can be removed with a manual or automatic process.

With **Geth**, if you are still using [the default hash state scheme](https://blog.ethereum.org/2023/09/12/geth-v1-13-0), you will accumulate *unneeded* data over time. You will need to stop Geth, [perform a manual process to prune its database](https://gist.github.com/yorickdowne/3323759b4cbf2022e191ab058a4276b2), and restart it to remove this junk. During this time, your node will be offline, and staking penalties will start accruing. [The rescue node project](https://rescuenode.com/docs/) can be a good solution for stakers to prevent or lower downtime and penalties. Pruning Geth also needs around 80 GB of free space to begin with on Mainnet. If you don't have that free space, you could try to delete your consensus client database to make enough room for it and resync your consensus client using [a checkpoint sync endpoint](https://eth-clients.github.io/checkpoint-sync-endpoints/). The new [path state scheme (PBSS)](#resyncing-with-a-different-configuration) is an interesting configuration alternative for long-term low disk usage.

With **Nethermind**, you have [different configurations that enable online pruning](https://docs.nethermind.io/fundamentals/pruning) where your client is still able to serve its normal operation and clean its database at the same time. There is a manual process where you can trigger the pruning process. There is one based on a database size threshold. There is one based on a remaining storage space threshold. In any case, you are going to need around 220 GB of free space to begin that pruning process on Mainnet. A good strategy is to set the automatic pruning configuration to trigger when you are slightly above that 220 GB of remaining free space. This implies that you are effectively reserving that space exclusively for pruning.

With **Lighthouse**, you can [prune historic states](https://lighthouse-book.sigmaprime.io/database-migrations.html#how-to-prune-historic-states) if you synced your beacon node before version 4.4.1.

### Updating and Resyncing from Scratch

Clients implement improvements over time to their disk usage strategy. Updating your client and resyncing from scratch can not only remove the *unneeded* data that was accumulated over time, but it can also enable your client to use better ways of storing that data to use less disk space. For execution clients, you are likely going to experience some extended downtime (a few hours to a few days). [The rescue node project](https://rescuenode.com/docs/) can be a good solution for stakers to prevent or lower downtime and penalties. For consensus clients, you can often use [a checkpoint sync endpoint](https://eth-clients.github.io/checkpoint-sync-endpoints/) to resync from scratch in a few minutes for minimal downtime.

For example, Lighthouse beacon nodes that were synced before version 4.4.1 have [historic states](https://lighthouse-book.sigmaprime.io/database-migrations.html#how-to-prune-historic-states) that are no longer needed. Performing the prune-states command or resyncing from scratch will drastically lower disk usage.

### Resyncing with a Different Configuration

Clients often have a large number of configuration options that can influence disk usage.

With **Geth**, starting with version 1.13.0, you can use [a Path Based Storage Scheme (PBSS)](https://blog.ethereum.org/2023/09/12/geth-v1-13-0) to avoid storing unnecessary data in your database. This new storage scheme is not enabled by default, and it is not considered production-ready yet. However, since it has a good impact on current disk usage, on long-term disk usage, and on avoiding the pruning maintenance task, many stakers and node operators are using it on Mainnet. You will need to resync from scratch if you want to use this configuration alternative. During this time, your node will be offline, and staking penalties will start accruing. [The rescue node project](https://rescuenode.com/docs/) can be a good solution for stakers to prevent or lower downtime and penalties.

With **Nethermind**, the development team is exploring [3 approaches to improve disk usage: Paprika, Path-Based Storage, and Half-path](https://medium.com/nethermind-eth/nethermind-client-3-experimental-approaches-to-state-database-change-8498e3d89771). As of today, January 2024, it seems like those approaches are all experimental, but we should keep an eye on them. Version 1.26.0 should include Half-path. It will become the default sync mode for new nodes or resyncs.

### Migrating to a Different Client

Different clients and configurations can lead to lower disk usage. Migrating from a client that does not have a great disk usage strategy to one that does can help with the disk usage concern. As of today, January 2024, Geth with PBSS is one of the best execution clients and configurations in terms of disk usage. Using the Geth client as a majority choice poses a significant risk to your stake and negatively impacts the overall health of the network.

### Using Multiple Disks

If your machine supports installing multiple good SSDs and your system is configured to enable extending your partitions or volumes easily, such as [with LVM](https://www.cyberciti.biz/faq/howto-add-disk-to-lvm-volume-on-linux-to-increase-size-of-pool/), adding another disk can be an interesting alternative to migrating to a larger disk. This approach can limit the downtime it takes to gain more disk space. It has a con in terms of larger risks coming from a disk failure. Your new machine will now fail if either one of your disks fails instead of the risk coming from a single disk. Using various [RAID setups](https://en.wikipedia.org/wiki/RAID) can help alleviate the risks from disk failures in a multiple disks configuration, but it's probably overkill for home stakers and home node operators. RAID setups are out of scope for this guide.

### Monitoring and Alerting

A good practice is to install and configure [monitoring](monitoring.md) and [alerting](alerting.md) tools to watch your machine's free disk space.

## Migrating to a Larger Disk

The general idea to migrate to a larger disk is simple.

1. Stop your staking or node machine.
2. Plug both disks into the same machine (it can be the same staking or node machine, or it can be another one).
3. Boot into a live OS or a tool to perform the copy.
4. Extend your volume or your partition on the new larger disk to be able to use the full capacity.
5. Plug the larger disk into your staking or node machine and restart that machine.

From there, your machine should simply work as it did before with more disk space for its operations. Extending your volume or partition (step 4) can be performed during the copying step, after the copying step, or even after restarting your staking or node machine.

### Requirements

You will need a machine where you can plug both disks at the same time. If you don't have enough room for both SSDs, you can buy an adapter like one you plug into a USB port. You will need a USB stick to put your live OS or tools on. Tools and general support to perform this on the Apple M1, M2 or M3 platform is limited. [Asahi Linux](https://asahilinux.org/) and their derivative work might be useful instead of using Clonezilla. Various [native Apple software](https://appleinsider.com/inside/mac/best/best-disk-clone-software-for-mac) could also work. We will focus on using an amd64 platform to perform the migration for this guide.

### Preparing your USB stick

This can be done on any machine connected to the Internet.

1. Use an empty USB stick or a USB stick that does not contain any important document. Plug it in.
2. Download [the latest stable release of Clonezilla Live](https://clonezilla.org/downloads.php). The ISO version for amd64 CPU architecture is likely what you will want.
3. Download [Rufus](https://rufus.ie/en/) (On Windows) or [balena Etcher](https://etcher.balena.io/) (On macOS or Linux) to create your bootable USB stick.
4. Run Rufus or balena Etcher, select the Clonezilla Live archive you downloaded at step 2 and select your USB stick. Create your bootable USB stick by following the software instructions.

### Copying the content on the larger disk

1. Stop the machine you want to use to perform the disk copy.
2. Plug in both SSDs in the same machine.
3. Plug in your bootable USB stick.
4. Boot your machine using the USB stick image and OS. The actual instruction to boot onto a USB stick will vary from machine to machine.

There are some common keyboard keys that are often used during the boot process to access the boot menu or BIOS/UEFI settings where you can choose the boot device. Here are a few possibilities:

- F2 or Del: On many systems, pressing the F2 key or the Del key during the initial startup process will take you to the BIOS or UEFI settings. From there, you can navigate to the Boot menu and select the USB drive as the boot device.
- F12 or Esc: Some systems use the F12 key or the Esc key to directly access the boot menu during startup. Pressing either of these keys should bring up a menu where you can choose the USB drive as the boot option.
- F10 or F9: On certain computers, the F10 or F9 key might be used to access the Boot menu directly during startup.
- ESC or Tab: In some cases, pressing the ESC key or the Tab key during startup may display a boot menu where you can select the USB drive.

Keep in mind that the exact key and the process can vary, so it's recommended to check your computer's manual or look for on-screen prompts during startup. If you're still unsure, you can provide the make and model of your computer, [we can try to find it for you](#support).

## Support

If you have any question or if you need additional support, make sure to get in touch with the ethstaker community on:

* Discord: [dsc.gg/ethstaker](https://dsc.gg/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)