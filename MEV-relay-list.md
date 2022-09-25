# MEV relay list for Mainnet

Here is a list of MEV relays for the Ethereum Mainnet network. To add one to your mev-boost configuration, simply copy and paste the *Relay URL* in your `-relays` flag value. You can add multiple relays comma-separated to the `-relays` flag, like this: `-relays https://relay1,https://relay2`. If you are using multiple relays, the current algorithm for mev-boost will select the relay that offers you the most profit.

Selecting your relays **can be an important decision** for some stakers. You should do your own diligence when selecting which relay you want to use.

| Operator | Notes | Relay URL |
|----------|-------|-----------|
| [Flashbots](https://www.flashbots.net/) | [OFAC compliant and maximizes profit](https://twitter.com/bantg/status/1559948198508118016) | `https://0xac6e77dfe25ecd6110b8e780608cce0dab71fdd5ebea22a16c0205200f2f8e2e3ad3b71d3499c54ad14d6c21b41a37ae@boost-relay.flashbots.net` |
| [bloXroute](https://bloxroute.com/) | [Max profit relay](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) that propagates all available transactions/bundles with no filtering. | `https://0x8b5d2e73e2a3a55c6c87b8b6eb92e0149a125c852751db1422fa951e42a09b82c142c3ea98d0d9930b056a3bc9896b8f@bloxroute.max-profit.blxrbdn.com` |
| [bloXroute](https://bloxroute.com/) | [Ethical relay](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) that propagates non-frontrunning bundles and private transactions. | `https://0xad0a8bb54565c2211cee576363f3a347089d2f07cf72679d16911d740262694cadb62d7fd7483f27afd714ca0f1b9118@bloxroute.ethical.blxrbdn.com` |
| [bloXroute](https://bloxroute.com/) | [Regulated relay](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) that propagates all available transactions/bundles except the ones sent from/to wallet addresses that are sanctioned by OFAC. | `https://0xb0b07cd0abef743db4260b0ed50619cf6ad4d82064cb4fbec9d3ec530f7c5e6793d9f286c4e082c0244ffb9f2658fe88@bloxroute.regulated.blxrbdn.com` |
| [Blocknative](https://www.blocknative.com/) | Supports [the OFAC compliance requirements](https://discord.com/channels/542403978693050389/1019351111083233421/1021808541494956092) | `https://0x9000009807ed12c1f08bf4e81c6da3ba8e3fc3d953898ce0102433094e5f22f21102ec057841fcb81978ed1ea0fa8246@builder-relay-mainnet.blocknative.com` |
| [Eden Network](https://v2.docs.edennetwork.io/) | Will respect [all applicable regulations](https://discord.com/channels/761540124940697600/773571585826357259/1020818179376820334), including OFAC sanctions | `https://0xb3ee7afcf27f1f1259ac1787876318c6584ee353097a50ed84f51a1f21a323b3736f271a895c7ce918c038e4265918be@relay.edennetwork.io` |
| [Manifold](https://securerpc.com/) |  | `https://0x98650451ba02064f7b000f5768cf0cf4d4e492317d82871bdc87ef841a0743f69f0f1eea11168503240ac35d101c9135@mainnet-relay.securerpc.com` |

# MEV relay list for Goerli testnet

Here is a list of MEV relays for the Ethereum Goerli test network. To add one to your mev-boost configuration, simply copy and paste the *Relay URL* in your `-relays` flag value. You can add multiple relays comma-separated to the `-relays` flag, like this: `-relays https://relay1,https://relay2`. If you are using multiple relays, the current algorithm for mev-boost will select the relay that offers you the most profit.

Selecting your relays **can be an important decision** for some stakers. You should do your own diligence when selecting which relay you want to use.

| Operator | Notes | Relay URL |
|----------|-------|-----------|
| [Flashbots](https://www.flashbots.net/) | | `https://0xafa4c6985aa049fb79dd37010438cfebeb0f2bd42b115b89dd678dab0670c1de38da0c4e9138c9290a398ecd9a0b3110@builder-relay-goerli.flashbots.net` |
| [bloXroute](https://bloxroute.com/) | [Max profit relay](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) that propagates all available transactions/bundles with no filtering. | `https://0x821f2a65afb70e7f2e820a925a9b4c80a159620582c1766b1b09729fec178b11ea22abb3a51f07b288be815a1a2ff516@bloxroute.max-profit.builder.goerli.blxrbdn.com` |
| [Blocknative](https://www.blocknative.com/) |  | `https://0x8f7b17a74569b7a57e9bdafd2e159380759f5dc3ccbd4bf600414147e8c4e1dc6ebada83c0139ac15850eb6c975e82d0@builder-relay-goerli.blocknative.com` |
| [Eden Network](https://v2.docs.edennetwork.io/) |  | `https://0xaa1488eae4b06a1fff840a2b6db167afc520758dc2c8af0dfb57037954df3431b747e2f900fe8805f05d635e9a29717b@relay-goerli.edennetwork.io` |
| [Manifold](https://securerpc.com/) |  | `https://0x8a72a5ec3e2909fff931c8b42c9e0e6c6e660ac48a98016777fc63a73316b3ffb5c622495106277f8dbcc17a06e92ca3@goerli-relay.securerpc.com/` |

# Configuring MEV boost software

If you need help installing and configuring mev-boost on your machine, check out our [Guide on how to prepare a staking machine for the Merge](https://github.com/remyroy/ethstaker/blob/main/prepare-for-the-merge.md#choosing-and-configuring-an-mev-solution)
