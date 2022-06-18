# Bitmex_HFT

The goal of this project is to explore the market microstructure of Bitcoin traded on BitMEX. 


# Change-log:
Notes for Visualizations.ipynb:
I changed upper and lower price-rage to for example
upper = 20000
lower = 15000

Changed to BTCUSD_ob from tick_store ticker output one cell above
(library.list_symbols())
df = library.read('BTCUSD_ob')

I imported also:
from pandas.plotting import register_matplotlib_converters

Run from jupyter notebook and installed all packages again from jupyer notebook

## 1. Dependencies 
First, dependencies must be installed to run any of the code.

Eventually: !pip3 install numpy==1.20.0 --force-reinstall

Pip install:
```

Using Ubuntu:

MongoDB
sudo apt-get mongo (mongo-org didnt worked for me)
Websocket
Bitmex-ws
pip3 install bitmex-ws
Pandas
Arctic
!pip3 install git+https://github.com/man-group/arctic.git
Test: from arctic import Arctic
Json (already installed in ubuntu)

```

If mongodb makes problems; try installing using docker:
docker --version
sudo apt-get remove docker docker-engine docker.io (if needed)
sudo apt-get update
sudo apt install docker.io

Than:
sudo docker pull mongo
sudo docker run -d -p 27017:27017 mongo
pip install arctic

Test:
from arctic import Arctic

## 2. Data
Next, the data is collected and stored in a Arctic Tick Database by running main.py. 
This includes two libraries, one for trades and another for quotes.

## 3. Analysis
The Orderbook is recreated and visualized in the Visualizations jupyter notebook which is what was used for Part 1 of the [article](https://www.linkedin.com/pulse/bitcoin-hft-part-1-data-ob-visualizations-jan-gobeli/?trackingId=s0KMD41VR3a%2B1%2FzlazznvA%3D%3D).


## 4. References

* [Limit Order Book Visualizations](http://parasec.net/transmission/order-book-visualisation/) by Phil Stubbings

* [Visualizing Bitcoin Order Book](https://rickyhan.com/jekyll/update/2017/09/24/visualizing-order-book.html) by Ricky Han
