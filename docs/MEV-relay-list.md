# MEV relay list for Mainnet

Here is a list of MEV relays for the Ethereum Mainnet network. To add one to your mev-boost configuration, simply copy and paste the *Relay URL* in your `-relays` flag value. You can add multiple relays comma-separated to the `-relays` flag, like this: `-relays https://relay1,https://relay2`. If you are using multiple relays, the current algorithm for mev-boost will select the relay that offers you the most profit.

Selecting your relays **can be an important decision** for some stakers. You should do your own diligence when selecting which relay you want to use.

| Operator/Relay Name | Filtering/Censorship/Compliance | MEV Strategies/Ethical considerations | Relay software | Profit sharing model | Builders and searchers | Status | Payload validated on the relay | Notes | Support | Relay URL |
|-|-|-|-|-|-|-|-|-|-|-|
| [Aestus](https://aestus.live) | No filtering and no censorship | Maximize validator payout by including all available transactions and MEV bundles | [Aestus' fork of mev-boost-relay](https://github.com/aestus-relay/mev-boost-relay) | 100% to validator | Public and permissionless. | [Dashboard](https://mainnet.aestus.live) | Yes | [Blog post](https://medium.com/@aestus_relay/introducing-the-aestus-relay-4a36f03acc31) | [Twitter](https://twitter.com/AestusRelay) [Email](mailto:contact@aestus.live) | `https://0xa15b52576bcbf1072f4a011c0f99f9fb6c66f3e1ff321f11f461d15e31b1cb359caa092c71bbded0bae5b5ea401aab7e@aestus.live` |
| [Agnostic Gnosis](https://twitter.com/GnosisDAO) | No filtering and no censorship | Maximize validator payout by including all available transactions and MEV bundles | [Gnosis's fork of mev-boost-relay](https://github.com/gnosis/mev-boost-relay) | 100% to validator | Public and permissionless. | [Dashboard](https://agnostic-relay.net/) | Unknown | [Blog post](https://www.gnosis.io/blog/agnostic-relay-a-credibly-neutral-tool) | [Discord](http://discord.gg/gnosischain) | `https://0xa7ab7a996c8584251c8f925da3170bdfd6ebc75d50f5ddc4050a6fdc77f2a3b5fce2cc750d0865e05d7228af97d69561@agnostic-relay.net` |
| [bloXroute Max Profit](https://bloxroute.com/) | Filters out OFAC sanctioned addresses as of [Dec 2023](https://twitter.com/bloXrouteLabs/status/1736819783520092357) (Called *Max profit* in the [documentation][3]) | Maximize validator payout without including transactions and bundles sent from/to wallet addresses that are sanctioned by OFAC | [bloXroute's fork of mev-boost-relay](https://github.com/bloXroute-Labs/mev-relay) | Unknown | Internal and external builders. External searchers. | [Dashboard](https://bloxroute.max-profit.blxrbdn.com/) | Yes | [Documentation for bloXroute relays offering](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) | [Discord](https://discordapp.com/invite/mB95H7s) [Email](mailto:support@bloxroute.com) | `https://0x8b5d2e73e2a3a55c6c87b8b6eb92e0149a125c852751db1422fa951e42a09b82c142c3ea98d0d9930b056a3bc9896b8f@bloxroute.max-profit.blxrbdn.com` |
| [bloXroute Regulated](https://bloxroute.com/) | Filters out OFAC sanctioned addresses (Called *Regulated* in the [documentation][3]) | Maximize validator payout without including transactions and bundles sent from/to wallet addresses that are sanctioned by OFAC | [bloXroute's fork of mev-boost-relay](https://github.com/bloXroute-Labs/mev-relay) | Unknown | Internal and external builders. External searchers. | [Dashboard](https://bloxroute.regulated.blxrbdn.com/) | Yes | [Documentation for bloXroute relays offering](https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators#relay-types) | [Discord](https://discordapp.com/invite/mB95H7s) [Email](mailto:support@bloxroute.com) | `https://0xb0b07cd0abef743db4260b0ed50619cf6ad4d82064cb4fbec9d3ec530f7c5e6793d9f286c4e082c0244ffb9f2658fe88@bloxroute.regulated.blxrbdn.com` |
| [Titan Relay](https://docs.titanrelay.xyz/) | No filtering and no censorship | Maximize validator payout by including all available transactions and MEV bundles | [Helix](https://github.com/gattaca-com/helix) | 100% to validator | Internal and external builders. Permissionless | [Dashboard](https://titanrelay.xyz/) | Yes | [Titan Relay documentation](https://docs.titanrelay.xyz/) | [Discord](https://x.com/titanbuilderxyz) | `https://0x8c4ed5e24fe5c6ae21018437bde147693f68cda427cd1122cf20819c30eda7ed74f72dece09bb313f2a1855595ab677d@global.titanrelay.xyz` |
| [Titan Relay Regional](https://docs.titanrelay.xyz/) | Filters out OFAC sanctioned addresses | Maximize validator payout without including transactions and bundles sent from/to wallet addresses that are sanctioned by OFAC | [Helix](https://github.com/gattaca-com/helix) | 100% to validator | Internal and external builders. Permissionless | [Dashboard](https://regional.titanrelay.xyz/) | Yes | [Titan Relay documentation](https://docs.titanrelay.xyz/) | [Discord](https://x.com/titanbuilderxyz) | `https://0x8c4ed5e24fe5c6ae21018437bde147693f68cda427cd1122cf20819c30eda7ed74f72dece09bb313f2a1855595ab677d@regional.titanrelay.xyz` |
| [Flashbots](https://boost.flashbots.net/) | Filters out OFAC sanctioned addresses ([Twitter Screenshot][2]) | Maximize validator payout without including transactions and bundles sent from/to wallet addresses that are sanctioned by OFAC | [mev-boost-relay](https://github.com/flashbots/mev-boost-relay) | Specific to builder of bid with highest validator value. 100% to validator from Flashbots builders. | Internal and external builders. Permissionless. | [Dashboard](https://boost-relay.flashbots.net/) | Yes | [Flashbots documentation](https://docs.flashbots.net/flashbots-mev-boost/introduction) | [Discord](https://discord.com/invite/3TjWjBerRb) | `https://0xac6e77dfe25ecd6110b8e780608cce0dab71fdd5ebea22a16c0205200f2f8e2e3ad3b71d3499c54ad14d6c21b41a37ae@boost-relay.flashbots.net` |
| [Manifold](https://securerpc.com/) | No filtering and no censorship | Maximize validator payout by including all available private transactions and MEV bundles | [mev-freelay](https://github.com/manifoldfinance/mev-freelay) | Varied | Internal and external builders. Permissionless. | [Dashboard](https://mainnet-relay.securerpc.com/) | Yes | [Manifold documentation](https://kb.manifoldfinance.com/) This relay had a major issue on October 15th 2022 ([1][4], [2][5]). | [Forum](https://forums.manifoldfinance.com/) [Email](mailto:sam@manifoldfinance.com) | `https://0x98650451ba02064f7b000f5768cf0cf4d4e492317d82871bdc87ef841a0743f69f0f1eea11168503240ac35d101c9135@mainnet-relay.securerpc.com` |
| [Ultra Sound](https://relay.ultrasound.money/) | No filtering and no censorship | Maximize validator payout by including all available transactions and MEV bundles | [mev-boost-relay](https://github.com/flashbots/mev-boost-relay) | 100% to validator | Public and permissionless. | [Dashboard](https://relay.ultrasound.money/) | Yes |  | [Twitter](https://twitter.com/ultrasoundmoney) [Email](mailto:contact@ultrasound.money) | `https://0xa1559ace749633b997cb3fdacffb890aeebdb0f5a3b6aaa7eeeaf1a38af0a8fe88b9e4b1f61f236d2e64d95733327a62@relay.ultrasound.money` |
| [Wenmerge](https://relay.wenmerge.com) | No filtering and no censorship | Maximize validator payout by including all available transactions and MEV bundles | [mev-boost-relay](https://github.com/flashbots/mev-boost-relay) | 100% to validator from wenmerge builders. Specific to builder of bid with highest validator value.| Public and permissionless. | [Dashboard](https://relay.wenmerge.com/) | Yes | A relay from Wenmerge to support eth community. | [Website](https://wenmerge.com) [Twitter](https://twitter.com/Wenmerge2022) [Email](mailto:contact@wenmerge.com) | `https://0x8c7d33605ecef85403f8b7289c8058f440cbb6bf72b055dfe2f3e2c6695b6a1ea5a9cd0eb3a7982927a463feb4c3dae2@relay.wenmerge.com` |
|[Proof Relay](https://pon.network/)|Only filtering is availability of ZK Proof for block and validator payment|Open auction - maximum value|[Proof Relay](https://github.com/pon-pbs/proof-relay)|100% to validator|Public and permissionless.|[Status](https://proof-relay.ponrelay.com/relay/config)|No - header only|[Docs](https://docs.pon.network/)|[Discord](https://discord.gg/rXjDArC776)|`https://0xa44f64faca0209764461b2abfe3533f9f6ed1d51844974e22d79d4cfd06eff858bb434d063e512ce55a1841e66977bfd@proof-relay.ponrelay.com`|

[1]: https://discord.com/channels/761540124940697600/1019624727234490378/1024710921706295388
[2]: https://twitter.com/bantg/status/1559948198508118016
[3]: https://docs.bloxroute.com/the-merge-eth2.0/mev-relay-instructions-for-validators
[4]: https://research.lido.fi/t/lido-on-ethereum-relay-voting-proposal/3135/11
[5]: https://hackmd.io/@manifoldx/2022-10-15

## External relay monitoring

* [MEV Panda](https://www.mevpanda.com) by OreoMev
* [calldata.pics](https://calldata.pics) by Toni Wahrstätter
* [censorship.pics](https://censorship.pics) by Toni Wahrstätter
* [mevboost.pics](https://www.mevboost.pics/) by Toni Wahrstätter
* [timing.pics](https://timing.pics) by Toni Wahrstätter
* [tornado.pics](https://tornado.pics) by Toni Wahrstätter
* [MEV Watch](https://www.mevwatch.info/) by Labrys
* [Relays](https://beaconcha.in/relays) from beaconcha.in
* [Relay Scan](https://www.relayscan.io) from Chris Hager
* [Transparency dashboard](https://transparency.flashbots.net/) by Flashbots
* [Relay Monitor](https://app.metrika.co/ethereum/dashboard/mev/relay-overview?tr=1d) by Metrika
* [Rated Network](https://www.rated.network/relays?network=mainnet) by Rated Network
* [Inclusion Watch](https://www.inclusion.watch) by donnoh.eth and emiliano.eth
* [Neutrality Watch](https://eth.neutralitywatch.com/) specifically analyses Lido operators. [Github](https://github.com/mikgur/Ethereum-censorability-monitor).

# MEV relay list for Holesky testnet

Here is a list of MEV relays for the Ethereum Holesky test network. To add one to your mev-boost configuration, simply copy and paste the *Relay URL* in your `-relays` flag value. You can add multiple relays comma-separated to the `-relays` flag, like this: `-relays https://relay1,https://relay2`. If you are using multiple relays, the current algorithm for mev-boost will select the relay that offers you the most profit.

Selecting your relays **can be an important decision** for some stakers. You should do your own diligence when selecting which relay you want to use.

| Operator | Notes | Relay URL |
|----------|-------|-----------|
| [Flashbots](https://www.flashbots.net/) | | `https://0xafa4c6985aa049fb79dd37010438cfebeb0f2bd42b115b89dd678dab0670c1de38da0c4e9138c9290a398ecd9a0b3110@boost-relay-holesky.flashbots.net` |
| [Aestus](https://holesky.aestus.live/) | | `https://0xab78bf8c781c58078c3beb5710c57940874dd96aef2835e7742c866b4c7c0406754376c2c8285a36c630346aa5c5f833@holesky.aestus.live` |
| [Titan](https://holesky.titanrelay.xyz/) | | `https://0xaa58208899c6105603b74396734a6263cc7d947f444f396a90f7b7d3e65d102aec7e5e5291b27e08d02c50a050825c2f@holesky.titanrelay.xyz` |

# MEV relay list for Sepolia testnet

Here is a list of MEV relays for the Ethereum Sepolia test network. To add one to your mev-boost configuration, simply copy and paste the *Relay URL* in your `-relays` flag value. You can add multiple relays comma-separated to the `-relays` flag, like this: `-relays https://relay1,https://relay2`. If you are using multiple relays, the current algorithm for mev-boost will select the relay that offers you the most profit.

Selecting your relays **can be an important decision** for some stakers. You should do your own diligence when selecting which relay you want to use.

| Operator | Notes | Relay URL |
|----------|-------|-----------|
| [Flashbots](https://www.flashbots.net/) | | `https://0xafa4c6985aa049fb79dd37010438cfebeb0f2bd42b115b89dd678dab0670c1de38da0c4e9138c9290a398ecd9a0b3110@boost-relay-sepolia.flashbots.net` |

# Configuring MEV boost software

If you need help installing and configuring mev-boost on your machine, check out our [Guide on how to prepare a staking machine for the Merge](https://github.com/eth-educators/ethstaker-guides/blob/main/prepare-for-the-merge.md#choosing-and-configuring-an-mev-solution)
