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

Output should look something like this.

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

This base rules file has 3 rules which you can adjust by modifying the `expr` field's value.

1. The first rule will alert you when you have less than around 80GB (81920000000 bytes) of available disk space on your `/` mount continuously for 1 minute. If your filesystem and your partitions are configured in a different way where you want to check for a different mount, you will have to change that `expr` field. If you have direct access to your prometheus web interface (often at `http://<machine ip>:9090`), you can execute the `node_filesystem_avail_bytes` query to view all possible mounts and their current free space. You can also view your current mounts and their free space by running the `$ df -h` command.
2. The second rule will alert you when you have less than around 1GB (1024000000 bytes) of free RAM to be used by your processes continuously for 1 minute. If your machine is consistently using almost all of your available RAM, you might want to lower that 1GB (1024000000 bytes) threshold value in that `expr` field.
3. The third rule will alert you when your CPU cores are used for more than 90% of their processing power continuously for 5 minutes.

Set ownership for the config file. If your prometheus service is running under an account that is not `prometheus`, adjust accordingly.

```
$ sudo chown prometheus:prometheus /etc/prometheus/alert_rules.yml
```

Restart your prometheus service and check the status to make sure it's running correctly. If your prometheus service is not configured to run using systemd with the `prometheus.service` name, adjust accordingly.

```
$ sudo systemctl restart prometheus.service
$ sudo systemctl status prometheus.service
```

Output should look something like this.

```
● prometheus.service - Prometheus
     Loaded: loaded (/etc/systemd/system/prometheus.service; enabled; vendor pr>
     Active: active (running) since Tue 2021-07-13 01:36:01 UTC; 6s ago
   Main PID: 83685 (prometheus)
      Tasks: 12 (limit: 18405)
     Memory: 125.4M
     CGroup: /system.slice/prometheus.service
             └─83685 /usr/local/bin/prometheus --config.file /etc/prometheus/pr>

Jul 13 01:36:01 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
Jul 13 01:36:02 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
Jul 13 01:36:02 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
Jul 13 01:36:02 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
Jul 13 01:36:02 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
Jul 13 01:36:02 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
Jul 13 01:36:02 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
Jul 13 01:36:02 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
Jul 13 01:36:02 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
Jul 13 01:36:02 testsystem prometheus[83685]: level=info ts=2021-07-13T01:36:>
```

If you did everything right, it should say active (running) in green. If not then go back and repeat the steps to fix the problem. Press Q to quit.

## Testing your rules

Time to test some of these rules. Here is an example to test your *Available disk space* rule. First, check how much space you have left on your disk.

```
$ df -h
```

You should see something like this.

```
Filesystem                         Size  Used Avail Use% Mounted on
udev                               7.5G     0  7.5G   0% /dev
tmpfs                              1.6G  1.7M  1.6G   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv  915G  438G  431G  51% /
tmpfs                              7.6G     0  7.6G   0% /dev/shm
tmpfs                              5.0M     0  5.0M   0% /run/lock
tmpfs                              7.6G     0  7.6G   0% /sys/fs/cgroup
/dev/nvme0n1p2                     976M  108M  801M  12% /boot
/dev/nvme0n1p1                     511M  7.9M  504M   2% /boot/efi
/dev/loop1                          56M   56M     0 100% /snap/core18/1944
/dev/loop0                         100M  100M     0 100% /snap/core/11316
/dev/loop2                         9.2M  9.2M     0 100% /snap/canonical-livepatch/99
/dev/loop3                          32M   32M     0 100% /snap/snapd/10707
/dev/loop4                          70M   70M     0 100% /snap/lxd/19188
/dev/loop5                          33M   33M     0 100% /snap/snapd/12398
/dev/loop6                          68M   68M     0 100% /snap/lxd/20326
/dev/loop7                          56M   56M     0 100% /snap/core18/2074
tmpfs                              1.6G     0  1.6G   0% /run/user/1000
```

Here, we can see that the main mount is `/`. It has around 431GB of available disk space. If you want to test the 80GB limit we set in the alerting rules, we can create a dummy file that is 400GB in size with this command.

```
$ fallocate -l 400G largespacer.img
```

That will leave us only around 31GB of available disk space. Waiting around 2 minutes should trigger the alert on Healthchecks.io and you should receive an email with the alert details.

Once your test is done, you can remove the dummy file with this command.

```
$ rm largespacer.img
```

## Resetting the check on Healthchecks.io

Once the alert is resolved, Alertmanager will call the ping url once more to say it is resolved but the check will remain in a failed state. You can manually reset it on https://healthchecks.io/ by going into the details of your check and by clicking on the *Ping Now!* button.

Healthchecks.io is more suited for monitoring cron jobs and similar periodic processes. This use of Healthchecks.io is somewhat contrived since we are mostly interested by its ability to easily forward our alerts through their nice integrations. Healthchecks.io will expect a periodic successful call to the check we created so we will provide one with these steps.

Setup the Healthchecks.io Low Resources systemd service. Open the service definition file.

```
$ sudo nano /etc/systemd/system/healthcheckslowresources.service
```

Paste the following into the file taking care to **replace the placeholder healthchecks.io ping url by your real ping url** that you created earlier. Exit and save the file.

```
[Unit]
Description=Healthchecks.io Low Resources
Wants=healthcheckslowresources.timer

[Service]
Type=oneshot
ExecStart=curl -m 10 --retry 5 https://hc-ping.com/<long id placeholder>

[Install]
WantedBy=multi-user.target
```

Setup the Healthchecks.io Low Resources systemd timer. Open the timer definition file.

```
$ sudo nano /etc/systemd/system/healthcheckslowresources.timer
```

Paste the following into the file. Exit and save the file.

```
[Unit]
Description=Healthchecks.io Low Resources timer
Requires=healthcheckslowresources.service

[Timer]
Unit=healthcheckslowresources.service
OnCalendar=weekly

[Install]
WantedBy=timers.target
```

Reload systemd to reflect the changes.

```
$ sudo systemctl daemon-reload
```

Start and enable the Healthchecks.io Low Resources systemd timer.

```
$ sudo systemctl start healthcheckslowresources.timer
$ sudo systemctl enable healthcheckslowresources.timer
```

This timer will call and reset your *Low Resources* check every week which is what is expected from the schedule we configured earlier.

That's it. That should give you some good alerting foundation. There is a lot more you can do with such setup but we will leave that as an exercise to the reader.

## Support

If you have any question or if you need additional support, make sure to get in touch with the ethstaker community on:

* Discord: [discord.gg/e84CFep](https://discord.gg/e84CFep)
* Reddit: [reddit.com/r/ethstaker](https://www.reddit.com/r/ethstaker/)