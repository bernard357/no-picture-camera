# The No-picture Camera project

Raspberry Pi with camera and OpenCV, a better solution than CCTV

![smart-video-counter](docs/media/smart-video-counter.png)

Read [instructions to setup a standalone camera](docs/setup.standalone.md), including OpenCV, the scanning software, the InfluxDB database and the Grafana dashboard, all on the same Raspberry PI.

If you have multiple boards, then consider [instructions to connect smart cameras over LoRa](docs/setup.lora.md). All cameras will run OpenCV, and one Raspberry Pi will act as a central datastore, with InfluxDB and Grafana, so that you can enjoy cameras data from a single pane of glass.



