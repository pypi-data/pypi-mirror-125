# Pymetrc

**Only the Montana endpoints are tested at this time. Each state dictates the subset of features Metrc exposes. As such, this may not work as intended with other state API endpoints.**

This project is intended to provide abstraction and easy integration with the Metrc REST API. It provides easily digestible output for use with Pandas and data analysis, storage, etc.

AIOHTTP is used to make concurrent calls to the API as the time-based query limitations can make necessary many individual GET requests, especially when initializing a database with all packages, sales receipts, etc.

Currently, only GET endpoints are implemented. Once these are covered, POST and PUT functionality is planned.

## Installation

Pymetrc is available via pip:

```sh
pip install pymetrc
```

## Usage

Upon instantiation of a Metrc object, an initial GET request is made to populate the facility list stored by the object. These facilities are those the given user has access to. This does not currently guarantee that the given user has permission to access the endpoints specified -- this is planned for future implementations.

Date/time strings passed must be in ISO 8601 format.

It is ill-advised to use API keys directly in code. It is recommended to use environment variables or other more secure means to store your API credentials:

```py
import os

vendor_api_key = os.environ['METRC_VENDOR_API_KEY']
user_api_key = os.environ['METRC_USER_API_KEY']
```

### Employees

```py
from pymetrc import Metrc

state = 'mt'
m = Metrc(vendor_api_key, user_api_key, state)

data = m.get_basic("employees_v1")
```

### Packages

```py
from pymetrc import Metrc

state = 'mt'
m = Metrc(vendor_api_key, user_api_key, state)

data = m.get_last_modified("packages_v1_active", "D-12345", "2020-01-01T00:00:00+00:00", "2021-01-01T00:00:00+00:00")
```

This returns a list of dictionary objects, each representing an entity of the type requested. In the above example, we get back a list of packages.

### Sales Transactions

```py
from pymetrc import Metrc

state = 'mt'
m = Metrc(vendor_api_key, user_api_key, state)

data = m.get_sales_transactions("D-12345", "2020-01-01T00:00:00+00:00", "2021-01-01T00:00:00+00:00")
```

In the above example, we get a list of receipts each containing a sub-list of per-package transactions. Requesting sales transactions via Pymetrc prompts a request first for the sales receipts in this time period. The receipt ids are parsed and then the sales transactions can be queried using these ids. Sales receipts can be requested if only high-level sales information is needed.

## Technologies
- Python 3.7+
- [aiohttp](https://github.com/aio-libs/aiohttp)
- [tqdm](https://github.com/tqdm/tqdm)
