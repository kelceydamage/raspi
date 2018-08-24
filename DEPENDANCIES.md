# Ubuntu 16.04, L4T, Tegra TX2

## Dependancies
* ZMQ
* ujson
* Cython
* SMBus2
* RPi.GPIO

## Optional
* Bokeh
** Used for monitoring features

### Development Environment
```bash
sudo apt-get update && sudo apt-get install perl wheel python3-setuptools python3-dev \
	python3-pip build-essential libzmq3-dev
```

### Virtual Environment
```bash
pip3 install virtualenv
virtualenv -p $(which python3) myenv
source myenv/bin/activate
```

### Installing ujson
```bash
pip install ujson
```

### Installing ZMQ
```bash
pip install pyzmq
```

### Installing Cython
```bash
pip install cython
```

### Installing SMBus2
```bash
pip install smbus2
```

### Installing RPi.GPIO
```bash
pip install RPi.GPIO
```

### Apt package alternates
```bash
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
sudo apt-get install python-rpi.gpio
```

# Centos7

### Development Environment & Core
```
sudo yum install python36u-pip python36u-devel python36u-setuptools
sudo yum install zeromq-devel-4.1.4-5.el7.x86_64 zeromq-4.1.4-5.el7.x86_64
```

### Virtual Environment
```bash
pip3.6 install virtualenv
virtualenv -p $(which python3.6) python36
source python36/bin/activate
```
