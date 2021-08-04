# Guide on how to do monitoring for a validator using Prometheus, Node Exporter and Grafana

Monitoring your system resources is an important task for any system administrator using any kind of machine whether you are a professional managing a large data center or simply someone tinkering at home.

This guide is meant for people with no or little experience in monitoring. It will show you step by step how to do monitoring on your machine by giving you the instructions to install and configure all the tools needed. It will assume you are using a modern linux distribution with systemd and APT (like Ubuntu 20.04) on a modern x86 CPU (Intel, AMD).

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

## Executing the commands

Almost all of these commands will be performed in a terminal. Start your *Terminal* application. Any line that starts with the dollar sign (`$`) is a command that need to be executed in your terminal. Do not input the dollar sign (`$`) in your terminal, only the text that comes after that.

## Installing Node exporter

Create a user account for the service to run under. This account will not be able to log into the machine. It will only be used to run the service.

```console
$ sudo useradd --no-create-home --shell /bin/false node_exporter
```

Download the latest version of Node exporter from https://prometheus.io/download/ . As of this date, the latest stable release version is 1.2.0 . Adjust the following instructions accordingly if there is a newer stable release version with a different archive name. The file name should end with *linux-amd64.tar.gz* (for linux and AMD64 instructions set).

```console
$ wget https://github.com/prometheus/node_exporter/releases/download/v1.2.0/node_exporter-1.2.0.linux-amd64.tar.gz
```

Verify that the SHA256 Checksum as shown on https://prometheus.io/download/ is the same as the file we just downloaded.

```console
$ sha256sum node_exporter-1.2.0.linux-amd64.tar.gz
```

Extract the archive.

```console
$ tar xvf node_exporter-1.2.0.linux-amd64.tar.gz
```

Copy the binaries to the following locations and set ownership.

```console
$ sudo cp node_exporter-1.2.0.linux-amd64/node_exporter /usr/local/bin
$ sudo chown -R node_exporter:node_exporter /usr/local/bin/node_exporter
```

Remove the download leftovers.

```console
$ rm -rf node_exporter-1.2.0.linux-amd64
$ rm node_exporter-1.2.0.linux-amd64.tar.gz
```

Create a systemd service file to store the service config which tells systemd to run Node exporter as the node_exporter user.

```console
$ sudo nano /etc/systemd/system/node_exporter.service
```

```ini
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter --web.listen-address="localhost:9100"

[Install]
WantedBy=multi-user.target
```

Reload systemd to reflect the changes.

```console
$ sudo systemctl daemon-reload
```

And then start the service with the following command and check the status to make sure it’s running correctly.

```console
$ sudo systemctl start node_exporter
$ sudo systemctl status node_exporter
```

Output should look something like this.

```
● node_exporter.service - Node Exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; disabled; vendo>
     Active: active (running) since Wed 2021-08-04 10:48:25 EDT; 4s ago
   Main PID: 10984 (node_exporter)
      Tasks: 5 (limit: 18440)
     Memory: 2.4M
     CGroup: /system.slice/node_exporter.service
             └─10984 /usr/local/bin/node_exporter

Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
Aug 04 10:48:25 remy-MINIPC-PN50 node_exporter[10984]: level=info ts=2021-08-04>
```

If you did everything right, it should say active (running) in green. If not then go back and repeat the steps to fix the problem. Press Q to quit. Finally, enable Node Exporter to start on boot.

```console
$ sudo systemctl enable node_exporter
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

Download the latest version of Prometheus from https://prometheus.io/download/ . As of this date, the latest stable release version is 2.28.1 . Adjust the following instructions accordingly if there is a newer stable release version with a different archive name. The file name should end with *linux-amd64.tar.gz* (for linux and AMD64 instructions set).

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

Setup the Prometheus configuration file. Open the YAML config file for editing.

```console
$ sudo nano /etc/prometheus/prometheus.yml
```

Paste the following into the file taking care not to make any additional edits. Exit and save the file.

```yaml
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']
```

The scrape_configs section define the different jobs where Prometheus will poll data from. We have 1 job so far in this configuration file: node_exporter. It will poll data from Node exporter and store all your hardware and OS metrics in the Prometheus database.

Set ownership for the config file. The prometheus account will own this.

```console
$ sudo chown -R prometheus:prometheus /etc/prometheus/prometheus.yml
```

Finally, let’s test the service is running correctly.

```console
$ sudo -u prometheus /usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries \
    --web.listen-address="localhost:9090"
```
Output should look something like this. Press Ctrl + C to exit.

```
level=info ts=2021-08-04T16:18:42.042Z caller=main.go:981 msg="Loading configuration file" filename=/etc/prometheus/prometheus.yml
level=info ts=2021-08-04T16:18:42.042Z caller=main.go:1012 msg="Completed loading of configuration file" filename=/etc/prometheus/prometheus.yml totalDuration=708.063µs remote_storage=3.096µs web_handler=719ns query_engine=1.658µs scrape=94.392µs scrape_sd=59.705µs notify=41.158µs notify_sd=22.063µs rules=2.437µs
level=info ts=2021-08-04T16:18:42.043Z caller=main.go:796 msg="Server is ready to receive web requests."
```

Create a systemd service file to store the service config which tells systemd to run Prometheus as the prometheus user, with the configuration file located in the /etc/prometheus/prometheus.yml directory, and to store its data in the /var/lib/prometheus directory.

```console
$ sudo nano /etc/systemd/system/prometheus.service
```

Paste the following into the file. Exit and save.

```ini
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
    --web.console.libraries=/etc/prometheus/console_libraries \
    --web.listen-address="localhost:9090"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

Reload systemd to reflect the changes.

```console
$ sudo systemctl daemon-reload
```

And then start the service with the following command and check the status to make sure it’s running correctly.

```console
$ sudo systemctl start prometheus
$ sudo systemctl status prometheus
```

Output should look something like this.

```
● prometheus.service - Prometheus
     Loaded: loaded (/etc/systemd/system/prometheus.service; disabled; vendor p>
     Active: active (running) since Wed 2021-08-04 12:20:56 EDT; 4s ago
   Main PID: 12061 (prometheus)
      Tasks: 11 (limit: 18440)
     Memory: 19.6M
     CGroup: /system.slice/prometheus.service
             └─12061 /usr/local/bin/prometheus --config.file /etc/prometheus/pr>

Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
Aug 04 12:20:56 remy-MINIPC-PN50 prometheus[12061]: level=info ts=2021-08-04T16>
```

If you did everything right, it should say active (running) in green. If not then go back and repeat the steps to fix the problem. Press Q to quit.
Lastly, enable Prometheus to start on boot.

```console
$ sudo systemctl enable prometheus
```

## Installing Grafana

We will use the [Install from APT repository](https://grafana.com/docs/grafana/latest/installation/debian/#install-from-apt-repository) installation guide from Grafana. A benefit of using this method is that it creates the service for you and it uses APT to easily keep Grafana up-to-date.

Install the prerequisites.

```console
$ sudo apt update -y
$ sudo apt install -y apt-transport-https software-properties-common wget
```

Import Grafana PGP key.

```console
$ wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```

Add Grafana OSS repository for stable releases.

```console
$ echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```

Install Grafana from the APT repository.

```console
$ sudo apt update
$ sudo apt install grafana
```

Open the Grafana configuration file.

```console
$ sudo nano /etc/grafana/grafana.ini
```

Search for the following section.

```ini
[server]
# Protocol (http, https, h2, socket)
;protocol = http

# The ip address to bind to, empty will bind to all interfaces
;http_addr =
```

Modify the configuration file by removing the semicolon (`;`) in front of `http_addr` and by adding `localhost` after the equal sign (`=`). It should look like this. Exit and save.

```ini
[server]
# Protocol (http, https, h2, socket)
;protocol = http

# The ip address to bind to, empty will bind to all interfaces
http_addr = localhost
```

Reload systemd to reflect the changes.

```console
$ sudo systemctl daemon-reload
```

And then start the service with the following command and check the status to make sure it’s running correctly.

```console
$ sudo systemctl start grafana-server
$ sudo systemctl status grafana-server
```

Output should look something like this.

```
● grafana-server.service - Grafana instance
     Loaded: loaded (/lib/systemd/system/grafana-server.service; disabled; vend>
     Active: active (running) since Wed 2021-08-04 12:59:12 EDT; 4s ago
       Docs: http://docs.grafana.org
   Main PID: 13876 (grafana-server)
      Tasks: 12 (limit: 18440)
     Memory: 31.2M
     CGroup: /system.slice/grafana-server.service
             └─13876 /usr/sbin/grafana-server --config=/etc/grafana/grafana.ini>

Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
Aug 04 12:59:13 remy-MINIPC-PN50 grafana-server[13876]: t=2021-08-04T12:59:13-0>
```

If you did everything right, it should say active (running) in green. If not then go back and repeat the steps to fix the problem. Press Q to quit.
Lastly, enable Grafana to start on boot.

```console
$ sudo systemctl enable grafana-server
```

## Accessing Grafana and adding your dashboards

(TODO)

## Adding your Ethereum clients

(TODO)

## Security risks

Adding Prometheus, Node exporter and Grafana with this configuration comes with a few additional security risks for your machine.

The first risk comes from the tools themselves. There might be some security issues with them that I am not aware of which might compromise your machine to some malicious actors. A great way to prevent such risk is to keep your system updated. Keeping Grafana updated should be somewhat easy as it was installed with APT. Executing those commands should keep all your system packages updated including Grafana.

```console
$ sudo apt update
$ sudo apt upgrade
```

Keeping Prometheus and Node exporter updated will require more efforts. You will need to monitor new stable releases and whether they include severe or critical bug fixes. To update to a new version, you will need to download the latest stable release, extract the archive, copy the binaries to their expected location and restart these services. The process and the instructions to download the new version, extract the archive and copy the binaries is exactly the same one mentioned at the beginning of the [Installing Node exporter](#installing-node-exporter) section and at the beginning of the [Installing Prometheus](#installing-prometheus) section.

To restart the Node exporter service after you updated its binary, use this command.

```console
$ sudo systemctl restart node_exporter
```

To restart the Prometheus service after you updated its binary, use this command.

```console
$ sudo systemctl restart prometheus
```

You can find all the Prometheus releases and their changelog on https://github.com/prometheus/prometheus/releases . You can find all the Node exporter releases and their changelog on https://github.com/prometheus/node_exporter/releases .

The second risk comes from the additional attack surface that these tools are creating. One of this attack surface is the HTTP servers they are adding and the ports on which they are listening. This guide configured them to only listen on your localhost interface meaning that they cannot be accessed from any other machine on a network. You would have to have malicious processes or actors connecting to these tools from your machine to access your private data for instance. A good way to prevent this risk is to limit the running processes, run only trusted processes, limit who can connect to the machine and only allow trusted people connecting to your machine.

If you want to access Grafana and your dashboards from a remote machine on your local network or from the internet, you could simply use [an SSH tunnel](https://www.tunnelsup.com/how-to-create-ssh-tunnels/) ([with PuTTY on Windows](https://www.ibm.com/support/pages/ssh-tunneling-putty) or [natively on Windows 10](http://woshub.com/ssh-tunnel-port-forward-windows/)).

There might be other kind of risks associated with those tools and this configuration, but I think these two are the main ones.

## What's next?

You might want to add *alerting* to your setup. If so, check out my other [guide on how to do alerting for a validator on low resources with Prometheus and PagerDuty](alerting.md).

## Support

If you have any question or if you need additional support, make sure to get in touch with the ethstaker community on:

* Discord: [discord.gg/e84CFep](https://discord.gg/e84CFep)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)

## Credits

Based on [Somer Esat's guide](https://someresat.medium.com/guide-to-staking-on-ethereum-2-0-ubuntu-pyrmont-lighthouse-a634d3b87393).