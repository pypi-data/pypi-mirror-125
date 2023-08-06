<p align="center">
    <img src="https://raw.githubusercontent.com/RatherBland/Quantel/master/docs/img/quantel.png">
</p>
<p align="center">
    <em>Official Python Library for the Quantel Finance API</em>
</p>
<p align="center">
    <a href="https://travis-ci.com/ratherbland/quantel" target="_blank">
        <img src="https://travis-ci.com/ratherbland/quantel.svg?branch=master" alt="Build Status">
    </a>
<a href="https://www.codefactor.io/repository/github/ratherbland/quantel" target="_blank">
    <img src="https://www.codefactor.io/repository/github/ratherbland/quantel/badge" alt="CodeFactor" />
</a>
<a href="https://app.codecov.io/gh/RatherBland/Quantel" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/ratherbland/Quantel" alt="Coverage">
</a>
<a href="https://pepy.tech/project/quantel" target="_blank">
    <img src="https://pepy.tech/badge/quantel" alt="Downloads">
</a>
</p>

---

**Website**: <a target="_blank" href="https://quantel.io">quantel.io </a>

**Documentation**: <a target="_blank" href="https://quantel.io/docs/python">quantel.io/docs/python </a>

**Blog Posts**: <a href="https://medium.com/@ratherbland/the-most-powerful-python-finance-library-youve-never-heard-of-f13f2cdfcc9a"> The Most Powerful Python Finance Library You’ve Never Heard Of </a>

**Source Code**: <a href="https://github.com/ratherbland/Quantel">ratherbland/Quantel </a>

**Get API Key**: <a href="http://links.quantel.io/getstarted">links.quantel.io/getstarted </a>

## Table of Contents

- [Overview](#overview)
- [Support For Major Exchanges.](#support-for-major-exchanges)
- [Setup](#setup)
  * [Requirements](#requirements)
  * [Installation](#installation)
- [Examples](#examples)
  * [Basic Example](#basic-example)
  * [Multiple Symbol Example](#multiple-symbol-example)
  * [International Example](#international-example)
  * [Asynchronous Example](#asynchronous-example)
- [License](#license)
- [Contact](#contact)


## Overview

Quantel is a powerful financial data and insights API. It provides easy access to world-class financial information. Quantel goes beyond just financial statements, giving users valuable information like insider transactions, major shareholder transactions, share ownership, peers, and so much more.

Some features of Quantel:

- **Fast**: Data is retrieved through API endpoints instead of web scraping. Additionally, asynchronous requests can be utilized with simple configuration
- **Simple**: Data for multiple symbols can be retrieved with simple one-liners
- **Lightweight**: Minimal reliance on third party packages
- **Powerful**: 40+ years of historical financial data for almost 25k thousand companies across the globe


## Support For Major Exchanges.
**Americas**
* NASDAQ
* New York Stock Exchange (NYSE)
* Toronto Stock Exchange (TSX)

**Asia Pacific**
* Australian Stock Exchange (ASX)
* Hong Kong Stock Exchange (HKEX)
* National Indian Stock Exchange (NSE)

**Europe**
* German Electronic Exchange (XETRA)
* EuroNext (ENX)
* London Stock Exchange (LSE)
* Moscow Stock Exchange (MOEX)
* Oslo Stock Exchange (OSE)
* Swiss Stock Exchange (SIX)


## Setup

### Requirements

Python 3.6+

- [Requests](https://requests.readthedocs.io/en/master/) - The elegant and simple HTTP library for Python, built for human beings.
- [Aiohttp](https://docs.aiohttp.org/en/stable/) - Asynchronous HTTP Client/Server for asyncio and Python.

### Installation

```bash
pip install quantel
```

## Examples

### Basic Example


```python
from quantel import Quantel

# Authenticate with the API
qt = Quantel(api_key="<quantel-api-key>")

# Instantiate the ticker class
goog = qt.ticker('goog')

# Retrieve company profile
goog.profile()
```

### Multiple Symbol Example

The `ticker` class also makes it easy to retrieve data for a list of symbols with the same API. Simply pass a list of symbols as the argument to the `ticker` class.

```python
from quantel import Quantel

qt = Quantel(api_key="<quantel-api-key>")

symbols = ['fb', 'aapl', 'amzn', 'nflx', 'goog']

faang = qt.ticker(symbols)

faang.profile()
```


### International Example

Quantel supports the majority of international exchanges. Read more about what data is supported by which exchanges at [quantel.io/docs/](https://quantel.io/docs)

```python
from quantel import Quantel

qt = Quantel(api_key="<quantel-api-key>")

symbols = ['DHER.DE', 'CBA.AX', 'DNB.OL', 'NESN.SW', 'ULVR.L', 'SHOP.TO', 'EDF.PA', ' RELIANCE.NS']

international = qt.ticker(symbols)

international.balance_sheet()
```

### Asynchronous Example

It really is that simple. Set `asynchronous=True` when instantiating the ticker class.

```python
from quantel import Quantel

qt = Quantel(api_key="<quantel-api-key>")

goog = qt.ticker('goog', asynchronous=True)

goog.profile()
```

## License

This project is licensed under the terms of the MIT license.


## Contact
Questions can be raised directly via <a href="mailto:guy@quantel.io">guy@quantel.io</a>