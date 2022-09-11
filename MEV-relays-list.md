# MEV relays list for Mainnet

Here is a list of MEV relays for the Ethereum Mainnet network. To add one to your mev-boost configuration, simply copy and paste the *Relay URL* in your `-relays` flag value. You can add multiple relays comma-separated to the `-relays` flag, like this: `-relays https://relay1,https://relay2`. If you are using multiple relays, the current algorithm for mev-boost will select the one that gives you the most profit.

Selecting your relays **can be an important decision** for some stakers. You should do your own diligence when selecting which relay you want to use.

| Operator | Notes | Relay URL |
|----------|-------|-----------|
| [Flashbots](https://www.flashbots.net/) | | `https://0xac6e77dfe25ecd6110b8e780608cce0dab71fdd5ebea22a16c0205200f2f8e2e3ad3b71d3499c54ad14d6c21b41a37ae@boost-relay.flashbots.net` |
| [bloXroute](https://bloxroute.com/) | [Max profit relay](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) that propagates all available transactions/bundles with no filtering. | `https://0x8b5d2e73e2a3a55c6c87b8b6eb92e0149a125c852751db1422fa951e42a09b82c142c3ea98d0d9930b056a3bc9896b8f@bloxroute.max-profit.blxrbdn.com` |
| [bloXroute](https://bloxroute.com/) | [Ethical relay](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) that propagates non-frontrunning bundles and private transactions. | `https://0xad0a8bb54565c2211cee576363f3a347089d2f07cf72679d16911d740262694cadb62d7fd7483f27afd714ca0f1b9118@bloxroute.ethical.blxrbdn.com` |
| [bloXroute](https://bloxroute.com/) | [Regulated relay](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) that propagates all available transactions/bundles except the ones sent from/to wallet addresses that are sanctioned by OFAC. | `https://0xb0b07cd0abef743db4260b0ed50619cf6ad4d82064cb4fbec9d3ec530f7c5e6793d9f286c4e082c0244ffb9f2658fe88@bloxroute.regulated.blxrbdn.com` |
| [Blocknative](https://www.blocknative.com/) |  | `https://0x9000009807ed12c1f08bf4e81c6da3ba8e3fc3d953898ce0102433094e5f22f21102ec057841fcb81978ed1ea0fa8246@builder-relay-mainnet.blocknative.com` |

If you need help installing and configuring mev-boost on your machine, check out our [Guide on how to prepare a staking machine for the Merge](https://github.com/remyroy/ethstaker/blob/main/prepare-for-the-merge.md#choosing-and-configuring-an-mev-solution)