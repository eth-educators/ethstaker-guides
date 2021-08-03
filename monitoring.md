# Guide on how to do monitoring for a validator using Prometheus, Node Exporter and Grafana

Monitoring your system resources is an important task for any system administrator using any kind of machine whether you are a professional managing a large data center or simply someone tinkering at home.

This guide is meant for people with no or little experience in monitoring. It will show you step by step how to do monitoring on your machine by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd (like Ubuntu 20.04) on a modern x86 CPU (Intel, AMD).

## Why would you want to do monitoring?

Here are some good reasons why you might want to do monitoring on your machine:

1. **Information visibility**: You want to expose and be able to easily see your machine details.
2. **Issue tracking and debugging**: You want to be able to inspect what happened in the past and see clearly how your machine reacted to some event.
3. **Issue prevention**: You want to be able to see potential resources exhaustion ahead of time.

## Overview

We will install 3 tools with this guide for monitoring: [Prometheus](https://prometheus.io/docs/introduction/overview/), [Node exporter](https://prometheus.io/docs/guides/node-exporter/) and [Grafana](https://grafana.com/oss/grafana/).

**Prometheus** is an open-source systems monitoring project. It collects and stores different metrics in a specialized database. It provides all those metrics to any other tool who wants to query them in an flexible, efficient and easy way. In our setup, it will collect metrics from Node Exporter and optionally from Ethereum clients and it will provide them on-demand to Grafana.

**Node exporter** is an open-source project that expose your hardware and OS metrics. In our setup, it will provide your system metrics to Prometheus.

**Grafana** is a an open-source project used to visualize metrics. It can be used to create dashboards that easily show the metrics you are interested in. In our setup, it will query the metrics stored on Prometheus to show them in a browser with nice charts and diagrams.

![Monitoring - Overview](images/monitoring-overview.png)

## Installing Node exporter

Create a user account for the service to run under. This account will not be able to log into the machine. It will only be used to run the service.

```console
$ sudo useradd --no-create-home --shell /bin/false node_exporter
```

## Installing Prometheus

Create a user account for the service to run under. This account will not be able to log into the machine. It will only be used to run the service.

```console
$ sudo useradd --no-create-home --shell /bin/false prometheus
```

Create the configuration and data directories with proper ownership.

```console
$ sudo mkdir /etc/prometheus
$ sudo mkdir /var/lib/prometheus
$ sudo chown -R prometheus:prometheus /etc/prometheus
$ sudo chown -R prometheus:prometheus /var/lib/prometheus
```

Download the latest version of Prometheus from https://prometheus.io/download/ . As of this date, the latest stable release version is 2.28.1 . Adjust the following instructions accordingly if there is a newer stable release version with a different archive name.

```console
$ wget https://github.com/prometheus/prometheus/releases/download/v2.28.1/prometheus-2.28.1.linux-amd64.tar.gz
```

Verify that the SHA256 Checksum as shown on https://prometheus.io/download/ is the same as the file we just downloaded.

```console
$ sha256sum prometheus-2.28.1.linux-amd64.tar.gz
```

Extract the archive.

```console
$ tar xvf prometheus-2.28.1.linux-amd64.tar.gz
```

Copy the binaries to the following locations and set ownership.

```console
$ sudo cp prometheus-2.28.1.linux-amd64/prometheus /usr/local/bin/
$ sudo cp prometheus-2.28.1.linux-amd64/promtool /usr/local/bin/
$ sudo chown -R prometheus:prometheus /usr/local/bin/prometheus
$ sudo chown -R prometheus:prometheus /usr/local/bin/promtool
```

Copy the content files to the following locations and set ownership.

```console
$ sudo cp -r prometheus-2.28.1.linux-amd64/consoles /etc/prometheus
$ sudo cp -r prometheus-2.28.1.linux-amd64/console_libraries /etc/prometheus
$ sudo chown -R prometheus:prometheus /etc/prometheus/consoles
$ sudo chown -R prometheus:prometheus /etc/prometheus/console_libraries
```

Remove the download leftovers.

```console
$ rm -rf prometheus-2.28.1.linux-amd64
$ rm prometheus-2.28.1.linux-amd64.tar.gz
```

Edit the Configuration File
Prometheus uses a configuration file so it knows where to scrape the data from. We will set this up here.
Open the YAML config file for editing.
$ sudo nano /etc/prometheus/prometheus.yml
Paste the following into the file taking care not to make any additional edits and exit and save the file.
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).
# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093
# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  - job_name: 'nodes'
    metrics_path: /metrics    
    static_configs:
      - targets: ['localhost:5054']
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']
The scrape_configs define the output target for the different job names. We have 2 job names: beacon node and node_exporter. The first is obvious, the second is for metrics related to the server instance itself (memory, CPU, disk, network etc.). We will install and configure node_exporter in the next step.
Set ownership for the config file. The prometheus account will own this.
$ sudo chown -R prometheus:prometheus /etc/prometheus/prometheus.yml
Finally, let’s test the service is running correctly.
$ sudo -u prometheus /usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries
Output should look something like this. Press Ctrl + C to exit.
level=info ts=2020-08-02T04:56:51.414Z caller=main.go:805 msg="Loading configuration file" filename=/etc/prometheus/prometheus.yml
level=info ts=2020-08-02T04:56:51.415Z caller=main.go:833 msg="Completed loading of configuration file" filename=/etc/prometheus/prometheus.yml
level=info ts=2020-08-02T04:56:51.415Z caller=main.go:652 msg="Server is ready to receive web requests."
Set Prometheus to Auto-Start as a Service
Create a systemd service file to store the service config which tells systemd to run Prometheus as the prometheus user, with the configuration file located in the /etc/prometheus/prometheus.yml directory, and to store its data in the /var/lib/prometheus directory.
$ sudo nano /etc/systemd/system/prometheus.service
Paste the following into the file. Exit and save.
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target
[Service]
Type=simple
User=prometheus
Group=prometheus
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries
[Install]
WantedBy=multi-user.target
Reload systemd to reflect the changes.
$ sudo systemctl daemon-reload
And then start the service with the following command and check the status to make sure it’s running correctly.
$ sudo systemctl start prometheus
$ sudo systemctl status prometheus
Output should look something like this.

If you did everything right, it should say active (running) in green. If not then go back and repeat the steps to fix the problem. Press Q to quit.
Lastly, enable Prometheus to start on boot.
$ sudo systemctl enable prometheus

## Security risks

(TODO)

## What's next?

You might want to add *alerting* to your setup. If so, check out my other [guide on how to do alerting for a validator on low resources with Prometheus and PagerDuty](alerting.md).

## Support

If you have any question or if you need additional support, make sure to get in touch with the ethstaker community on:

* Discord: [discord.gg/e84CFep](https://discord.gg/e84CFep)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)

## Credits

Based on [Somer Esat's guide](https://someresat.medium.com/guide-to-staking-on-ethereum-2-0-ubuntu-pyrmont-lighthouse-a634d3b87393).