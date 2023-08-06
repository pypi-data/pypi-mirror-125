# WebCase Delivery API

SDK for Delivery's(Ukrainian logistics company) API.

## Installation

```sh
pip install wc-delivery-auto-sdk
```

## Usage

```python
from wc_delivery_auto.client import Client


delivery = Client()
# Getting cities list
cities = delivery.geo.cities.get_list()
```

## TODO

- [x] Geography catalog lookup methods.
- [_] Streets catalog lookup methods.
- [_] Warehouses catalog lookup methods.
- [_] Counterparty management methods.
- [_] Registries management methods.
- [_] Waybills management methods.
