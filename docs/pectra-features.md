# New staking features included in Pectra

[Pectra](https://eips.ethereum.org/EIPS/eip-7600), combining changes on the consensus layer ([Electra](https://github.com/ethereum/consensus-specs/tree/dev/specs/electra)) with changes on the execution layer (Prague), is the next hard fork in line to upgrade the Ethereum protocol. This document covers the new staking related features and changes included with this upgrade.

## Consolidated or compounding validators

[EIP-7251: Increase the MAX_EFFECTIVE_BALANCE](https://eips.ethereum.org/EIPS/eip-7251) defines a new type of validator that I will call a consolidated or compounding validator. It enables stakers to earn compounding rewards on a single validator that can have up to 2048 effective ETH on its balance. It can be refered to as a type 2 or `0x02` validator, with `0x02` being the first 2 bytes of its withdrawal credential. We were used to only having type 0 or `0x00` validators and type 1 or `0x01` validators before. Here are all the different validator types we will have after Pectra:

- Type 0 or `0x00`: A regular validator without a withdrawal address. It can also be called a *BLS* or *locked* validator. Its balance keeps increasing after each successful duty performed without anywhere to go until there is a withdrawal address added with the BLS to execution change operation. Peforming this BLS to execution change operation will transform it into a type 1 validator.
- Type 1 or `0x01`: A regular validator with a withdrawal address. Its balance is maxed at 32 ETH after which an automatic partial withdrawal will send any excess balance to the withdrawal address on a rolling window (there are usually a few days between those automatic withdrawals).
- Type 2 or `0x02`: A compounding validator with a withdrawal address. Its balance is maxed at 2048 ETH after which an automatic partial withdrawal will send any excess balance to the withdrawal address on a rolling window (there are usually a few days between those automatic withdrawals). The rewards structure and slashing penalties are changed such that they are compounding and somewhat equivalent to running multiple regular validators without the related computational burden for the network or the node operator.

If you are currently running a type 0 or type 1 validator, nothing will change for you after Pectra. Type 1 validators will keep obtaining their automatic partial withdrawals on balances above 32 ETH. You will get the opportunity to use the new type 2 validator if you want.

Similar to depositing for a type 1 validator, stakers will be able to create brand new type 2 validators by creating a new deposit with the correct withdrawal credentials. There will also be a migration path from a type 1 validator to a type 2 validator through the consolidation request operation. The consolidation request operation enables stakers to consolidate 1 or multiple validators into one or many larger type 2 validators. This operation is performed on the execution layer with a transaction sent from the validator withdrawal address to a smart contract. There are 2 types of transactions you can perform with the consolidation request operation:

1. Transform an existing type 1 validator to a type 2 validator.
2. Transfert the balance from a type 1 or type 2 validator to a type 2 validator. This will effectively exit the source validator and consolidate its balance on the target validator.

In order for this operation to work, the validators must be active on the consensus layer and they must share the same associated withdrawal address. The withdrawal address must also match with the address of the one sending the transaction, meaning that the withdrawal address is controlling this consolidation request operation.

It was always possible to deposit additional funds into an existing validator but with this new compounding validator type the top up action will likely become more commun. It used to be that 32 ETH was the only possible maximum effective ETH balance and most well-behaved validators' balance would be near 32 ETH. There will be a lot of different and desirable increments on a compounding validator balance and we will see a much wilder distribution on the consensus layer after Pectra. Every integer increment changes on your validator's balance increase the amount of rewards you can get. For type 0 and type 1 validators, it caps at 32 ETH, but for type 2 validators, it caps at 2048 ETH. If you have a type 2 validator with 44 ETH on balance and you have 1 additional ETH you want to stake, you can deposit this 1 ETH on that validator to increase your rewards for instance. A new deposit or performing this top up action needs to include at least 1 ETH to be valid meaning that you cannot send 0.5 ETH with the deposit action if you are missing 0.5 ETH to reach the next increment.

There are various delays after performing a consolidation request operation depending on the type of transaction. There is also a queue and some increasing fee if demand for this operation exceed the target configured by the network to control congestion. The current configuration says there is a maximum of 2 consolidation requests per block and 1 is the target amount of consolidation request per block.

## User triggered exit and withdrawals

[EIP-7002: Execution layer triggerable withdrawals](https://eips.ethereum.org/EIPS/eip-7002) defines new mechanisms to allow stakers to manually exit or withdraw any valid amount from their validator balance. These operations are performed on the execution layer with a transaction sent from the validator withdrawal address to a smart contract.

This manual withdrawal request is only possible with type 2 validators defined in [EIP-7251](#consolidated-or-compounding-validators). You can pass any amount to withdraw but it will max out to leave 32 ETH on your validator's balance no matter what meaning that you cannot overdraw and cause an unexpected exit because there isn't enough ETH left after withdrawal on your validator's balance.

This manual exit request is possible for type 1 or type 2 validators. When asked for, a validator exited in this way will be exited in a similar way as the voluntary exit performed on the consensus layer. As a reminder, performing a voluntary exit on the consensus layer is free while you will need to pay for gas and the queue fee for performing a manual exit request with this mechanism.

In order for these requests to work, the validator must be active on the consensus layer. The withdrawal address must also match with the address of the one sending the transaction, meaning that the withdrawal address is controlling these requests.

There are various delays after performing an exit or a withdraw with this new mechanism. There is also a queue and some increasing fee if demand for this operation exceed the target configured by the network to control congestion. The current configuration says there is a maximum of 16 exit or withdrawal requests per block and 2 is the target amount of exit or withdrawal requests per block.

## More blobs

## Support

If you have any question or if you need additional support, make sure to get in touch with the EthStaker community on:

* Discord: [dsc.gg/ethstaker](https://dsc.gg/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)
