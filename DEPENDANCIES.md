# Ubuntu 16.04, L4T, Tegra TX2

## Dependancies
* ZMQ
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