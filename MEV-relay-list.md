# MEV relay list for Mainnet

Here is a list of MEV relays for the Ethereum Mainnet network. To add one to your mev-boost configuration, simply copy and paste the *Relay URL* in your `-relays` flag value. You can add multiple relays comma-separated to the `-relays` flag, like this: `-relays https://relay1,https://relay2`. If you are using multiple relays, the current algorithm for mev-boost will select the relay that offers you the most profit.

Selecting your relays **can be an important decision** for some stakers. You should do your own diligence when selecting which relay you want to use.

| Operator | Filtering/Censorship/Compliance | MEV Strategies/Ethical considerations | Relay software | Profit sharing model | Builders and searchers | Status | Payload validated on the relay | Notes | Support | Relay URL |
|-|-|-|-|-|-|-|-|-|-|-|
| [Flashbots](https://boost.flashbots.net/) | Filters out OFAC sanctioned addresses ([Twitter Screenshot][2]) | Maximize validator payout without including transactions and bundles sent from/to wallet addresses that are sanctioned by OFAC | [mev-boost-relay](https://github.com/flashbots/mev-boost-relay) | Specific to builder of bid with highest validator value. 100% to validator from Flashbots builders. | Internal and external builders | [Dashboard](https://boost-relay.flashbots.net/) | Yes | [Flashbots documentation](https://docs.flashbots.net/flashbots-mev-boost/introduction) | [Discord](https://discord.com/invite/3TjWjBerRb) | `https://0xac6e77dfe25ecd6110b8e780608cce0dab71fdd5ebea22a16c0205200f2f8e2e3ad3b71d3499c54ad14d6c21b41a37ae@boost-relay.flashbots.net` |
| [bloXroute](https://bloxroute.com/) | No filtering and no censorship (Called *Max profit* in the [documentation][3]) | Maximize validator payout by including all available private transactions and MEV bundles | Internal software | Unknown | Internal builder and external searchers. Upcoming external builders. | [Dashboard](https://bloxroute.max-profit.blxrbdn.com/) | Yes | [Documentation for bloXroute relays offering](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) | [Discord](https://discordapp.com/invite/mB95H7s) [Email](mailto:support@bloxroute.com) | `https://0x8b5d2e73e2a3a55c6c87b8b6eb92e0149a125c852751db1422fa951e42a09b82c142c3ea98d0d9930b056a3bc9896b8f@bloxroute.max-profit.blxrbdn.com` |
| [bloXroute](https://bloxroute.com/) | Filters out generalized frontrunning and sandwiching MEV bundles (Called *Ethical* in the [documentation][3]) | Maximize validator payout without including MEV bundles running generalized frontrunning and sandwiching attacks | Internal software | Unknown | Internal builder and external searchers. Upcoming external builders. | [Dashboard](https://bloxroute.ethical.blxrbdn.com) | Yes | [Documentation for bloXroute relays offering](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) | [Discord](https://discordapp.com/invite/mB95H7s) [Email](mailto:support@bloxroute.com) | `https://0xad0a8bb54565c2211cee576363f3a347089d2f07cf72679d16911d740262694cadb62d7fd7483f27afd714ca0f1b9118@bloxroute.ethical.blxrbdn.com` |
| [bloXroute](https://bloxroute.com/) | Filters out OFAC sanctioned addresses (Called *Regulated* in the [documentation][3]) | Maximize validator payout without including transactions and bundles sent from/to wallet addresses that are sanctioned by OFAC | Internal software | Unknown | Internal builder and external searchers. Upcoming external builders. | [Dashboard](https://bloxroute.regulated.blxrbdn.com/) | Yes | [Documentation for bloXroute relays offering](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) | [Discord](https://discordapp.com/invite/mB95H7s) [Email](mailto:support@bloxroute.com) | `https://0xb0b07cd0abef743db4260b0ed50619cf6ad4d82064cb4fbec9d3ec530f7c5e6793d9f286c4e082c0244ffb9f2658fe88@bloxroute.regulated.blxrbdn.com` |
| [Blocknative](https://www.blocknative.com/) | Supports [OFAC compliance requirements](https://discord.com/channels/542403978693050389/1019351111083233421/1021808541494956092) | Maximize validator payout without MEV or OFAC sanctioned addresses | [Dreamboat](https://github.com/blocknative/dreamboat) | 100% to validator | Internal builder. External builders and MEV searchers coming up. | Coming Soon | Yes | [Documentation for Blocknative relay offering](https://docs.blocknative.com/mev-relay-instructions-for-ethereum-validators)| [Discord](https://discord.com/invite/KZaBVME) [Email](mailto:Hello@blocknative.com) | `https://0x9000009807ed12c1f08bf4e81c6da3ba8e3fc3d953898ce0102433094e5f22f21102ec057841fcb81978ed1ea0fa8246@builder-relay-mainnet.blocknative.com` |
| [Eden Network](https://docs.edennetwork.io/) | Will respect [all applicable regulations](https://discord.com/channels/761540124940697600/773571585826357259/1020818179376820334), including OFAC sanctions ([Chris on Discord][1]) | It will not frontrun their private RPC transactions ([Chris on Discord][1]) | [A fork of mev-boost-relay](https://github.com/eden-network/mev-boost-relay) | 100% to validator but subject to change ([Chris on Discord][1]) | Eden Network, but they will be opening to 3rd party builders soon ([Chris on Discord][1])  | [Dashboard](https://relay.edennetwork.io/info) | Not at the moment but likely yes in the future ([Chris on Discord][1]) | | [Discord](https://discord.gg/5jmFKh8na2) | `https://0xb3ee7afcf27f1f1259ac1787876318c6584ee353097a50ed84f51a1f21a323b3736f271a895c7ce918c038e4265918be@relay.edennetwork.io` |
| [Manifold](https://securerpc.com/) | No filtering and no censorship | Maximize validator payout by including all available private transactions and MEV bundles | Unknown | Unknown | Unknown | [Dashboard](https://mainnet-relay.securerpc.com/) | Unknown | | [Discord](https://openmev.page.link/support-chat) [Email](mailto:sam@manifoldfinance.com) | `https://0x98650451ba02064f7b000f5768cf0cf4d4e492317d82871bdc87ef841a0743f69f0f1eea11168503240ac35d101c9135@mainnet-relay.securerpc.com` |

[1]: https://discord.com/channels/761540124940697600/1019624727234490378/1024710921706295388
[2]: https://twitter.com/bantg/status/1559948198508118016
[3]: https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators

## External relay monitoring

* [MEV Relays](https://mev-relays.beaconstate.info/) by 1337
* [mevboost.org](https://www.mevboost.org/) by Anish Agnihotri
* [MEV Watch](https://www.mevwatch.info/) by Labrys
* [Relays](https://beaconcha.in/relays) from beaconcha.in

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
