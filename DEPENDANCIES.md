# Ubuntu 16.04, L4T, Tegra TX2

## Dependancies
* ZMQ
* Cython

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
