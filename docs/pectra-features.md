# New Staking Features in Pectra

[Pectra](https://eips.ethereum.org/EIPS/eip-7600), combining changes on the consensus layer ([Electra](https://github.com/ethereum/consensus-specs/tree/dev/specs/electra)) with changes on the execution layer (Prague), is the next hard fork planned to upgrade the Ethereum protocol. This document covers the new staking-related features and changes included in this upgrade.

## Fork Schedule

Pectra was [officially announced on Holesky and Sepolia](https://blog.ethereum.org/2025/02/14/pectra-testnet-announcement). Here is the planned schedule for these forks:

- [Holesky](https://github.com/eth-clients/holesky) at epoch 115968 (Feb. 24, 2025, 21:55 UTC)
- [Sepolia](https://github.com/eth-clients/sepolia) at epoch 222464 (Mar. 5, 2025, 7:29 UTC)

Once both testnets have successfully upgraded, a mainnet activation schedule will be chosen.

## Consolidated or Compounding Validators

[EIP-7251: Increase the MAX_EFFECTIVE_BALANCE](https://eips.ethereum.org/EIPS/eip-7251) defines a new type of validator called a consolidated or compounding validator. It enables stakers to earn compounding rewards on a single validator that can have up to 2048 effective ETH on its balance. This can be referred to as a type 2 or `0x02` validator, with `0x02` being the first 2 bytes of its withdrawal credentials. Previously, only type 0 (`0x00`) and type 1 (`0x01`) validators existed. Here are all the validator types available after Pectra:

- Type 0 or `0x00`: A regular validator without a withdrawal address. It can also be called a *BLS* or *locked* validator. Its balance continues to increase until it is converted to a type 1 validator.
- Type 1 or `0x01`: A regular validator with a withdrawal address. Its balance is capped at 32 ETH, after which an automatic partial withdrawal sends any excess balance to the withdrawal address on a rolling window (typically every few days).
- Type 2 or `0x02`: A compounding validator with a withdrawal address. Its balance is capped at 2048 ETH, after which an automatic partial withdrawal sends any excess balance to the withdrawal address on a rolling window. The rewards structure and slashing penalties are adjusted to be compounding and roughly equivalent to running multiple regular validators without the associated computational burden for the network or node operator.

### Rewards and Proposer Selection Probability

Unlike traditional validators, type 2 validators allow **compounding rewards**, meaning that earned rewards remain within the validator’s balance instead of being automatically withdrawn above 32 ETH. This compounding effect enables long-term validators to accumulate higher returns over time.  

However, **the fundamental reward structure remains unchanged**—attestation, proposal, and sync committee rewards are calculated the same way as for type 1 validators. The probability of being selected as a **block proposer or sync committee member is directly proportional to the validator’s effective balance**. This means that while a single type 2 validator with 2048 ETH has a higher probability of proposing a block compared to a 32 ETH validator, splitting the same 2048 ETH across multiple 32 ETH validators results in an identical overall proposal probability.  

Additionally, **slashing penalties have been reduced**, making large validators less risky than before. Previously, slashing resulted in an immediate loss of 1/32 of a validator's balance, but with EIP-7251, this penalty has been reduced to **1/4096**, significantly lowering the downside for high-balance validators.

If you currently run a type 0 or type 1 validator, nothing will change after Pectra. Type 1 validators will continue receiving automatic partial withdrawals for balances above 32 ETH. You will have the option to use the new type 2 validator if desired.

New validators can be deposited directly as type 2 validators. There is also a migration path from type 1 to type 2 validators through the consolidation request operation. This operation allows stakers to consolidate one or multiple validators into one or many larger type 2 validators. The operation is performed on the execution layer with a transaction sent from the validator withdrawal address to a smart contract. There are two types of transactions possible with the consolidation request operation:

1. Transform an existing type 1 validator to a type 2 validator
2. Transfer the balance from a type 1 or type 2 validator to a type 2 validator. This will exit the source validator and consolidate its balance on the target validator

For a consolidation to work, the validator you're moving from must still be active (not exited), and the request must come from the same wallet that controls the withdrawal address of that validator. This is to ensure that only the person who owns the validator can approve moving its balance. The withdrawal address of the target validator (the one being consolidated into) does not have to match the withdrawal address of the source validator (the one being converted).

While it has always been possible to deposit additional funds into an existing validator, this practice will likely become more common with the new compounding validator type. Previously, 32 ETH was the only possible maximum effective ETH balance, and most well-behaved validators' balances stayed near 32 ETH. After Pectra, we will see a wider distribution of validator balances on the consensus layer. Every integer increment in your validator's balance increases your potential rewards. For type 0 and type 1 validators, this caps at 32 ETH, but for type 2 validators, it caps at 2048 ETH. For example, if you have a type 2 validator with 44 ETH and want to stake an additional ETH, you can deposit it to increase your rewards. New deposits or top-ups must include at least 1 ETH to be valid.

Various delays apply after performing a consolidation request operation, depending on the transaction type. The network defines a maximum of 2 consolidation requests per block, with 1 being the target. To avoid hindering and prevent others from using this feature a fee is used for rate limiting. It gets exponentially more expensive to add more consolidation requests as the network processes more than 1 per block. Requests are added to a queue and they are processed in order on the next block with available room.

## User-Triggered Exit and Withdrawals

[EIP-7002: Execution layer triggerable withdrawals](https://eips.ethereum.org/EIPS/eip-7002) defines new mechanisms allowing stakers to manually exit or withdraw any valid amount from their validator balance. These operations are performed on the execution layer via a transaction sent from the validator withdrawal address to a smart contract.

Manual withdrawal requests are only possible with type 2 validators defined in [EIP-7251](#consolidated-or-compounding-validators). You can specify any withdrawal amount, but the operation will ensure at least 32 ETH remains in your validator's balance to prevent unexpected exits due to insufficient funds.

Manual exit requests are available for both type 1 and type 2 validators. When requested, a validator will exit similarly to a voluntary exit performed on the consensus layer. While voluntary exits on the consensus layer are free, manual exit requests require the owner to pay gas fees and rate limiting fees.

For these requests to work, the validator must be active on the consensus layer, and the withdrawal address must match the address sending the transaction.

Various delays apply after performing an exit or withdrawal using this new mechanism. The network defines a maximum of 16 exit or withdrawal requests per block, with 2 being the target. To avoid hindering and prevent others from using this feature a fee is used for rate limiting. It gets exponentially more expensive to add more exit or withdrawal requests as the network processes more than 2 per block. Requests are added to a queue and they are processed in order on the next block with available room.

## More Blobs

[EIP-7691: Blob throughput increase](https://eips.ethereum.org/EIPS/eip-7691) increases the number of blobs to scale Ethereum via L2 solutions. It raises the target number of blobs per block from 3 to 6 and increases the maximum number of blobs per block from 6 to 9.

This will likely increase bandwidth requirements for stakers until PeerDAS is included in a later fork.

## Faster deposits

[EIP-6110: Supply validator deposits on chain](https://eips.ethereum.org/EIPS/eip-6110) improves the validator deposit mechanism on the beacon chain. This change reduces the delay between making a deposit and its recognition by the beacon chain from over 9 hours to approximately 13 minutes.

## Support

If you have questions or need additional support, connect with the EthStaker community on:

* Discord: [dsc.gg/ethstaker](https://dsc.gg/ethstaker)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)
