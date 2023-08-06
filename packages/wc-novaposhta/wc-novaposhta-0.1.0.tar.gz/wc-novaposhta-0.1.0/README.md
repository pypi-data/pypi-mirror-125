# WebCase Novaposhta API

SDK for Novaposhta's(Ukrainian logistics company) API.

## Installation

```sh
pip install wc-novaposhta
```

## Usage

```python
from wc_novaposhta.client import Client


novaposhta = Client('YOUR_API_KEY)
# Getting cities list
cities = novaposhta.geo.cities.get_list()
```

## TODO

- [x] Geography catalog lookup methods.
- [_] Streets catalog lookup methods.
- [_] Warehouses catalog lookup methods.
- [_] Counterparty management methods.
- [_] Registries management methods.
- [_] Waybills management methods.
- [_] Smaller catalogs lookup methods.
- [_] Printing forms management methods.
