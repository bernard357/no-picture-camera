# Frequently asked questions

## About project governance

### Where is this project coming from?

The No-picture Camera project emerged from the Urban Moves Hackathon 2016 that was sponsored by Nokia in Paris area.

### Is this software available to anyone?

Yes. The software and the documentation have been open-sourced from the outset, so that it can be useful to the global community that enjoys Raspberry, OpenCV, IoT, LoRa and the like. The No-picture Camera project is based on the [Apache License](https://www.apache.org/licenses/LICENSE-2.0).

### Do you accept contributions to this project?

Yes. There are multiple ways for end-users and for non-developers to [contribute to this project](contributing.md). For example, if you hit an issue, please report it at GitHub. This is where we track issues and report on corrective actions.

And if you know [how to clone a GitHub project](https://help.github.com/articles/cloning-a-repository/), we are happy to consider [pull requests](https://help.github.com/articles/about-pull-requests/) with your modifications. This is the best approach to submit additional reference configuration files, or updates of the documentation, or even evolutions of the python code.

## About project design

### What is needed to deploy a No-picture Camera?

Everything you need can be installed on a single Raspberry Pi device:
* the camera itself
* the scanning software powered by OpenCV
* the InfluxDB database
* the Grafana web dashboard

Read [instructions to setup a standalone camera](setup.standalone.md), including OpenCV, the scanning software, the InfluxDB database and the Grafana dashboard, all on the same Raspberry PI.

If you have multiple boards, then consider [instructions to connect smart cameras over LoRa](setup.lora.md). All cameras will run OpenCV, and one Raspberry Pi will act as a central datastore, with InfluxDB and Grafana, so that you can enjoy cameras data from a single pane of glass.

