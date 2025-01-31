# New staking features included in Pectra

[Pectra](https://eips.ethereum.org/EIPS/eip-7600), combining changes on the consensus layer ([Electra](https://github.com/ethereum/consensus-specs/tree/dev/specs/electra)) with changes on the execution layer (Prague), is the next hard fork in line to upgrade the Ethereum protocol. This document covers the new staking related features and changes included with this upgrade.

## Consolidated or compounding validators

[EIP-7251: Increase the MAX_EFFECTIVE_BALANCE](https://eips.ethereum.org/EIPS/eip-7251) defines a new type of validator that I will call a consolidated or compounding validator. It enables stakers to earn compounding rewards on a single validator that can have up to 2048 effective ETH on its balance. It can be refered to as a type 2 or `0x02` validator, with `0x02` being the first 2 bytes of its withdrawal credential. We were used to only having type 0 or `0x00` validators and type 1 or `0x01` validators before. Here are all the different validator types we will have after Pectra:

- Type 0 or `0x00`: A regular validator without a withdrawal address. It can also be called a *BLS* or *locked* validator. Its balance keeps increasing after each successful duty performed without anywhere to go until there is a withdrawal address added with the BLS to execution change operation. Peforming this BLS to execution change operation will transform it into a type 1 or `0x01` validator.
- Type 1 or `0x01`: A regular validator with a withdrawal address. Its balance is maxed at 32 ETH after which an automatic partial withdrawal will send any excess balance to the withdrawal address on a rolling window (there are usually a few days between those automatic withdrawals).
- Type 2 or `0x02`: A compounding validator with a withdrawal address. Its balance is maxed at 2048 ETH after which an automatic partial withdrawal will send any excess balance to the withdrawal address on a rolling window (there are usually a few days between those automatic withdrawals). The rewards structure and slashing penalties are changed such that they are compounding and somewhat equivalent to running multiple regular validators without the related computational burden for the network or the node operator.

If you are currently running a type 0 or type 1 validator, nothing will change for you after Pectra. Type 1 validators will keep obtaining their automatic partial withdrawals on balances above 32 ETH. You will get the opportunity to use the new type 2 validator if you want.

Similar to depositing for a type 1 validator, stakers will be able to create brand new type 2 validators by creating a new deposit with the correct withdrawal credentials. There will also be a migration path from a type 1 or `0x01` validator to a type 2 or `0x02` validator through the consolidation request operation. This operation is performed on the execution layer with a transaction sent from the validator withdrawal address to a smart contract. You need to pass 2 values with this transaction:

- A source validator public key
- A target validator public key

In order for this operation to work, both validators must be active on the consensus layer and the source validator withdrawal address and the target validator withdrawal address must match. The withdrawal address must also match with the address of the one sending the transaction, meaning that the withdrawal address is controlling this consolidation request operation. If all the conditions are met and the source validator public key and the target validator public key match and this validator is of type 1, it will be upgraded in-place to a type 2 validator. If all the conditions are met, the target validator is of type 2 and the source validator public key and the target validator public key are different, the balance from the source validator will be transfered and sent to the balance of the target validator. The source validator will effectively be exited.

The consolidation request operation enables stakers to consolidate 1 or multiple validators into one or many larger type 2 validators.

It was always possible to deposit additional funds into an existing validator but with this new compounding validator type the top up action will likely become more commun. It used to be that 32 ETH was the only possible effective ETH balance and most validators' balance would be near 32 ETH but there will be a lot of different and desirable increments on a compounding validator balance and we will see a much wilder distribution on the consensus layer after Pectra.

## User triggered exit and withdrawals

## More blobs

## Support

If you have any question or if you need additional support, make sure to get in touch with the EthStaker community on:

* Discord: [dsc.gg/ethstaker](https://dsc.gg/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)
