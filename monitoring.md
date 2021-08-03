# Guide on how to do monitoring for a validator using Prometheus, Node Exporter and Grafana

Monitoring your system resources is an important task for any system administrator using any kind of machine whether you are a professional managing a large data center or simply someone tinkering at home.

This guide is meant for people with no or little experience in monitoring. It will show you step by step how to do monitoring on your machine by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd (like Ubuntu 20.04) on a modern x86 CPU (Intel, AMD).

## Why would you want to do monitoring?

Here are some good reasons why you might want to do monitoring on your machine:

1. Information visibility: You want to expose and be able to easily see your machine details.
2. Issue tracking and debugging: You want to be able to inspect what happened in the past and see clearly how your machine reacted to some event.
3. Issue prevention: You want to be able to see potential resources exhaustion ahead of time.

## Overview

We will install 3 tools with this guide for monitoring: [Prometheus](https://prometheus.io/docs/introduction/overview/), [Node exporter](https://prometheus.io/docs/guides/node-exporter/) and [Grafana](https://grafana.com/oss/grafana/).

**Prometheus** is an open-source systems monitoring project. It collects and stores different metrics in a specialized database. It provides all those metrics to any other tool who wants to query them in an flexible, efficient and easy way. In our setup, it will collect metrics from Node Exporter and optionally from Ethereum clients and it will provide them on-demand to Grafana.

**Node exporter** is an open-source project that expose your hardware and OS metrics. In our setup, it will provide your system metrics to Prometheus.

**Grafana** is a an open-source project used to visualize metrics. It can be used to create dashboards that easily show the metrics you are interested in. In our setup, it will query the metrics stored on Prometheus to show them in a browser with nice charts and diagrams.

![Monitoring - Overview](images/monitoring-overview.png)

## Support

If you have any question or if you need additional support, make sure to get in touch with the ethstaker community on:

* Discord: [discord.gg/e84CFep](https://discord.gg/e84CFep)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)

## Credits

Based on [Somer Esat's guide](https://someresat.medium.com/guide-to-staking-on-ethereum-2-0-ubuntu-pyrmont-lighthouse-a634d3b87393).