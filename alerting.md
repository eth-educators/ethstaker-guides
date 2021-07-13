# Guide on how to do alerting on low resources with Prometheus and Healthchecks.io

If you are already using Prometheus with Node Exporter to monitor your system, it might be interesting to add Alertmanager and some rules in there to receive alerts when your machine is low on resources (low available disk space, low available RAM, high CPU usage, etc) so you can inspect and correct an issue before it's too late. A common issue for which alerting is very useful and that many validators are likely to face is low remaining disk space because of the clients' databases growth and the need to do some pruning to control that growth.

This guide will show you step by step how to do alerting. It will assume you are using a modern linux distribution with systemd (like Ubuntu 20.04). It will also use Healthchecks.io as a easy way to integrate with different messaging services (Email, SMS, Discord, Slack, Signal, Telegram, etc). I'm not sponsored nor affiliated with Healthchecks.io, but I like what they are doing.

## Setup an account and a check on Healthchecks.io

Create a free account on https://healthchecks.io/ . Reuse the initial *My First Check* check or add a new check. Name it "Low Resources". Change the schedule to:

* Period: 1 week
* Grace Time: 15 minutes

Adjust the notification methods for that check. By default it will only send notifications to the email address you used to create your account. You can add more messaging services by clicking on the *Integrations* element in the main menu at the top.

Go back to your check and copy the ping url somewhere so you can easily reuse it later. It should look like `https://hc-ping.com/<long string of random letters and numbers separated by dashes>` .

## Installing Alertmanager

These steps will install Alertmanager as a systemd service. 

Create the alertmanager user.

```
$ sudo useradd --no-create-home --shell /bin/false alertmanager
```

Create the directories with proper ownership.

```
$ sudo mkdir /etc/alertmanager
$ sudo mkdir /var/lib/alertmanager
$ sudo chown -R alertmanager:alertmanager /etc/alertmanager
$ sudo chown -R alertmanager:alertmanager /var/lib/alertmanager
```

Download the latest version from https://prometheus.io/download/ . As of this date, the latest version is 0.22.2 .

```
$ wget https://github.com/prometheus/alertmanager/releases/download/v0.22.2/alertmanager-0.22.2.linux-amd64.tar.gz
```

Verify that the SHA256 Checksum as shown on https://prometheus.io/download/ is the same as the file we just downloaded.

```
$ sha256sum alertmanager-0.22.2.linux-amd64.tar.gz
```

Extract the archive.

```
$ tar xvf alertmanager-0.22.2.linux-amd64.tar.gz
```

Copy the binaries to the following locations and set ownership.

```
$ sudo cp alertmanager-0.22.2.linux-amd64/alertmanager /usr/local/bin/
$ sudo cp alertmanager-0.22.2.linux-amd64/amtool /usr/local/bin/
$ sudo chown alertmanager:alertmanager /usr/local/bin/alertmanager
$ sudo chown alertmanager:alertmanager /usr/local/bin/amtool
```

Remove the download leftovers.

```
$ rm -rf alertmanager-0.22.2.linux-amd64
$ rm alertmanager-0.22.2.linux-amd64.tar.gz
```

Setup the Alertmanager configuration file. Open the YAML config file for editing.

```
$ sudo nano /etc/alertmanager/alertmanager.yml
```

Paste the following into the file taking care to **replace the placeholder healthchecks.io ping url by your real ping url** that you created earlier with the added `/fail` at the end. Exit and save the file.

```
route:
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 1h
  receiver: 'healthchecks.io'

receivers:
- name: 'healthchecks.io'
  webhook_configs:
  - url: 'https://hc-ping.com/<long id placeholder>/fail'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']
```

Set ownership for the config file.

```
$ sudo chown alertmanager:alertmanager /etc/alertmanager/alertmanager.yml
```

Setup the Alertmanager systemd service. Open the service definition file.

```
$ sudo nano /etc/systemd/system/alertmanager.service
```

Paste the following into the file. Exit and save the file.

```
[Unit]
Description=Alertmanager
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=alertmanager
Group=alertmanager
Restart=always
RestartSec=5
ExecStart=/usr/local/bin/alertmanager \
    --config.file /etc/alertmanager/alertmanager.yml \
    --storage.path /var/lib/alertmanager/
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

Reload systemd to reflect the changes.

```
$ sudo systemctl daemon-reload
```

Start the service and check the status to make sure it's running correctly.

```
$ sudo systemctl start alertmanager.service
$ sudo systemctl status alertmanager.service
```

Output should look something like this:

```
● alertmanager.service - Alertmanager
     Loaded: loaded (/etc/systemd/system/alertmanager.service; enabled; vendor >
     Active: active (running) since Mon 2021-07-12 22:12:06 UTC; 1s ago
   Main PID: 81779 (alertmanager)
      Tasks: 9 (limit: 18405)
     Memory: 22.3M
     CGroup: /system.slice/alertmanager.service
             └─81779 /usr/local/bin/alertmanager --config.file /etc/alertmanage>

Jul 12 22:12:06 testsystem systemd[1]: Started Alertmanager.
Jul 12 22:12:06 testsystem alertmanager[81779]: level=info ts=2021-07-12T22:1>
Jul 12 22:12:06 testsystem alertmanager[81779]: level=info ts=2021-07-12T22:1>
Jul 12 22:12:06 testsystem alertmanager[81779]: level=info ts=2021-07-12T22:1>
Jul 12 22:12:06 testsystem alertmanager[81779]: level=info ts=2021-07-12T22:1>
Jul 12 22:12:06 testsystem alertmanager[81779]: level=info ts=2021-07-12T22:1>
Jul 12 22:12:06 testsystem alertmanager[81779]: level=info ts=2021-07-12T22:1>
Jul 12 22:12:06 testsystem alertmanager[81779]: level=info ts=2021-07-12T22:1>
Jul 12 22:12:06 testsystem alertmanager[81779]: level=info ts=2021-07-12T22:1>
```

If you did everything right, it should say active (running) in green. If not then go back and repeat the steps to fix the problem. Press Q to quit.

Enable the Alertmanager service to start on boot.

```
$ sudo systemctl enable alertmanager.service
```

## Configuring Prometheus to use Alertmanager

Edit your prometheus configuration file. It's likely in `/etc/prometheus/prometheus.yml`. If not, adjust accordingly.

```
$ sudo nano /etc/prometheus/prometheus.yml
```

Make sure you have the following sections in that configuration file. You might already have part of it in comments. If so, just remove the related comments and paste this in there. This section is often located before the `scrape_configs` section.

```
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - localhost:9093
rule_files:
  - "alert_rules.yml"
```

## Adding alerting rules

Setup the rules for alerting. Open the rules file.

```
# sudo nano /etc/prometheus/alert_rules.yml
```

Paste the following base rules into the file. Exit and save the file.

```
groups:
- name: alert_rules
  rules:
  - alert: Available_disk_space_too_low
    expr: node_filesystem_avail_bytes{mountpoint="/"} <= 81920000000
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: Available disk space below 80GB
  - alert: Available_memory_too_low
    expr: node_memory_MemAvailable_bytes <= 1024000000
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: Available memory below 1GB
  - alert: CPU_usage_too_high
    expr: 100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) >= 90
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: CPU usage above 90%
```

This base rules file has 3 rules which you can adjust by using the `expr` field.

1. The first rule will alert you when you have less than around 80GB (81920000000 bytes) of available disk space on your `/` mount continuously for 1 minute. If your filesystem and your partitions are configured in a different way where you want to check for a different mount, you will have to change that `expr` field. If you have direct access to your prometheus web interface (often at http://<machine ip>:9090), you can execute the `node_filesystem_avail_bytes` query to view all possible mounts and their current free space. You can also view your current mounts and their free space by running the `$ df -h` command.
2. The second rule will alert you when you have less than around 1GB (1024000000 bytes) of free RAM to be used by your processes continuously for 1 minute. If your machine is consistently using almost all of your available RAM, you might want to lower that 1GB (1024000000 bytes) value in that `expr` field.
3. The third rule will alert you when your CPU cores are used for more than 90% of their processing power continuously for 5 minutes.

Set ownership for the config file. If your prometheus service is running under an account that is not `prometheus`, adjust accordingly.

```
$ sudo chown prometheus:prometheus /etc/prometheus/alert_rules.yml
```

Restart your prometheus service. If you prometheus service is not configured using systemd with the prometheus.service name, adjust accordingly.

```
$ sudo systemctl restart prometheus.service
```