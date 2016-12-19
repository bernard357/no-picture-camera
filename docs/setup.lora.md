# LoRa setup

On this page you will find instructions to install two Raspberry Pi connected over LoRa.

One Raspberry Pi is setup as a smart camera. It features:
- a Raspberry camera, of course,
- the scanning software powered by OpenCV,
- a Chistera Pi shield for LoRa communications

Another Raspberry Pi is setup as datastore. It features:
- a Chistera Pi shield for LoRa communications,
- the InfluxDB database,
- the Grafana web dashboard

![architecture](media/architecture.lora.png)

Note that this architecture supports multiple cameras. Real-time data is consolidated wirelessly on a single visual dashboard.

## Install LoRa shield

Each Raspberry Pi is communicating over LoRa. In this design you will add a Chistera Pi shield to every device.
After power on you activate serial communications with the shield:

```
sudo raspi-config
```

Then select `9 - Advanced Options` then `A5 - SPI`. Confirm your choice and exit the configuration tool.

## Install camera software

Connect over SSH to each target Raspberry Pi and apply following commands:

```
sudo mkdir -p /opt
cd /opt
sudo git clone https://github.com/bernard357/smart-video-counter.git
sudo chmod 0777 -R /opt/smart-video-counter
cd smart-video-counter
pip install -r requirements.txt
cd source
```

You will immediately change the id of each camera to ensure that it is unique:

```
sudo nano config.py
```

The camera id will be transmitted with counter values, and appear in the
database and reports. You should avoid spaces and special punctuation characters.

![config.py](media/config.py.png)

Save changes with `Ctl-O` and exit the editor with `Ctl-X`.

## Install LoRa sender software

Get the source of the software, and compile it, with following commands:

```
cd /opt
sudo git clone https://github.com/bernard357/lora_chisterapi.git
sudo chmod 0777 -R /opt/lora_chisterapi
cd lora_chisterapi
cp examples/uds_sender.cpp src/main.cpp
make
```

If the compilation went fine, then we will configure and run a service that will run
in the background and send data to LoRa:

```
sudo cp examples/uds_chisterapi.service.example /etc/systemd/system/chisterapi.service
sudo chmod 664 /etc/systemd/system/chisterapi.service
sudo systemctl enable /etc/systemd/system/chisterapi.service
sudo systemctl start chisterapi.service
sudo systemctl status chisterapi.service
```

![systemctl.status.uds_sender](media/systemctl.status.uds_sender.png)

## Install the scanner service

Install the scanner service with following commands:

```
sudo cp /opt/smart-video-counter/scripts/smart-video-counter.service.example /etc/systemd/system/smart-video-counter.service
sudo chmod 664 /etc/systemd/system/smart-video-counter.service
```

Now you can enable the new service, start it, and get feedback:

```
sudo systemctl enable /etc/systemd/system/smart-video-counter.service
sudo systemctl start smart-video-counter.service
sudo systemctl status smart-video-counter.service
```

If everything went fine, the system should report a successful start:

![systemctl.status.smart-video-counter](media/systemctl.status.smart-video-counter.png)

That's it for the camera itself. Now we move to the datastore.

## Install datastore software

Connect over SSH to the Raspberry Pi used for datastore and apply following commands:

```
sudo mkdir -p /opt
cd /opt
sudo git clone https://github.com/bernard357/smart-video-counter.git
sudo chmod 0777 -R /opt/smart-video-counter
cd smart-video-counter
pip install -r requirements.txt
cd source
```

## Install InfluxDB to store data

[InfluxDB](https://www.influxdata.com/time-series-platform/influxdb/) is an open source database written in Go specifically to handle time series data with high availability and high performance requirements.

We install an InfluxDB database on Raspberry Pi with following commands:

```
sudo su
adduser influxdb
wget https://dl.influxdata.com/influxdb/releases/influxdb-1.1.1_linux_armhf.tar.gz
tar xvfz influxdb-1.1.1_linux_armhf.tar.gz
rm influxdb-1.1.1_linux_armhf.tar.gz
cp -rp influxdb-1.1.1-1/* /
chown -R influxdb:influxdb /var/lib/influxdb
chown -R influxdb:influxdb /var/log/influxdb
cp -n /usr/lib/influxdb/scripts/influxdb.service /etc/systemd/system/
systemctl enable influxdb.service
cp -n /usr/lib/influxdb/scripts/init.sh /etc/init.d/influxdb
chmod +x /etc/init.d/influxdb
insserv influxdb
service influxd start
service influxd status
```

If everything went fine, you could get positive feedback on the InfluxDB service:

![systemctl.status.influxdb](media/systemctl.status.influxdb.png)

## Configure the InfluxDB updater

Then we change the configuration of the system so that updates are sent to InfluxDB.
Uncomment the block referring to infludb.

```
nano config.py
```

![config.py.influxdb](media/config.py.influxdb.png)

## Install the updater service

The updater service handles measurements coming from cameras, and pushes them to an InfluxDB database.
Install the updater service with following commands:

```
sudo cp ../scripts/updater.service.example /etc/systemd/system/updater.service
sudo chmod 664 /etc/systemd/system/updater.service
```

Now you can enable the new service, start it, and get feedback:

```
sudo systemctl enable /etc/systemd/system/updater.service
sudo systemctl start updater.service
sudo systemctl status updater.service
```

If everything went fine, the system should report a successful start:

![systemctl.status.updater](media/systemctl.status.updater.png)

## Install LoRa receiver software

Get the source of the software, and compile it, with following commands:

```
cd /opt
sudo git clone https://github.com/bernard357/lora_chisterapi.git
sudo chmod 0777 -R /opt/lora_chisterapi
cd lora_chisterapi
cp examples/uds_receiver.cpp src/main.cpp
make
```

If the compilation went fine, then we will configure and run a service that will run
in the background and receive data from LoRa:

```
sudo cp examples/uds_chisterapi.service.example /etc/systemd/system/chisterapi.service
sudo chmod 664 /etc/systemd/system/chisterapi.service
sudo systemctl enable /etc/systemd/system/chisterapi.service
sudo systemctl start chisterapi.service
sudo systemctl status chisterapi.service
```

![systemctl.status.uds_receiver](media/systemctl.status.uds_receiver.png)

After some time we can verify the presence of data in the InfluxDB database:

```
influx
> show databases
> use smart-video-counter
> show series
> select * from "smart-counter"
```

If you have multiple lines of text, you can congratulate yourself!

```
> exit
```

## Install Grafana

[Grafana](http://grafana.org/) is an open source metric analytics & visualization suite. It is most commonly used for visualizing time series data for infrastructure and application analytics but many use it in other domains including industrial sensors, home automation, weather, and process control.

Currently there are multiple steps to install Grafana on Raspberry Pi, so let do that progressively:

```
# grafana data is a dependancy for grafana
sudo apt-get install -y fonts-font-awesome libjs-angularjs libjs-twitter-bootstrap
wget http://ftp.us.debian.org/debian/pool/main/g/grafana/grafana-data_2.6.0+dfsg-3_all.deb
sudo dpkg -i grafana-data_2.6.0+dfsg-3_all.deb
sudo apt-get install -f

sudo apt-get install -y golang-go golang-go-linux-arm golang-go.tools golang-src
wget http://ftp.us.debian.org/debian/pool/main/g/grafana/grafana_2.6.0+dfsg-3_armhf.deb
sudo dpkg -i grafana_2.6.0+dfsg-3_armhf.deb
sudo apt-get install -f
sudo systemctl start grafana-server.service
sudo systemctl status grafana-server.service
```

On successful start of the server, open a browser window and enter
the IP address of the raspberry Pi, followed by `:3000`.

This will display the login page of Grafana. From there you can authenticate with `admin` and `admin` then add a new data source and build a dashboard.

Click on the Grafana logo and then select Data Sources. Select a source of type InfluxDB and then pick up the database named `smart-video-counter`.

![grafana.data-source](media/grafana.data-source.png)

Then add a new dashboard and add one graph per measure: standing, moves, faces.

![grafana.graph](media/grafana.graph.png)
