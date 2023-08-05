# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioridwell']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT==2.1.0',
 'aiohttp>=3.7.4,<4.0.0',
 'pytz>=2021.3,<2022.0',
 'titlecase>=2.3,<3.0']

setup_kwargs = {
    'name': 'aioridwell',
    'version': '2021.10.0',
    'description': 'A Python3, asyncio-based API for interacting with Ridwell waste recycling',
    'long_description': '# ♻️ aioridwell: A Python3, asyncio-based API for interacting with Ridwell\n\n[![CI](https://github.com/bachya/aioridwell/workflows/CI/badge.svg)](https://github.com/bachya/aioridwell/actions)\n[![PyPi](https://img.shields.io/pypi/v/aioridwell.svg)](https://pypi.python.org/pypi/aioridwell)\n[![Version](https://img.shields.io/pypi/pyversions/aioridwell.svg)](https://pypi.python.org/pypi/aioridwell)\n[![License](https://img.shields.io/pypi/l/aioridwell.svg)](https://github.com/bachya/aioridwell/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/aioridwell/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/aioridwell)\n[![Maintainability](https://api.codeclimate.com/v1/badges/9c1dcc1c991cecb06eda/maintainability)](https://codeclimate.com/github/bachya/aioridwell/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\n`aioridwell` is a Python 3, asyncio-friendly library for interacting with\n[Ridwell](https://ridwell.com) to view information on upcoming recycling pickups.\n\n- [Installation](#installation)\n- [Python Versions](#python-versions)\n- [Usage](#usage)\n- [Contributing](#contributing)\n\n# Installation\n\n```python\npip install aioridwell\n```\n\n# Python Versions\n\n`aioridwell` is currently supported on:\n\n* Python 3.8\n* Python 3.9 \n* Python 3.10\n\n# Usage\n\n## Creating and Using a Client\n\nThe `Client` is the primary method of interacting with the API:\n\n```python\nimport asyncio\n\nfrom aioridwell import async_get_client\n\n\nasync def main() -> None:\n    client = await async_get_client("<EMAIL>", "<PASSWORD>")\n    # ...\n\n\nasyncio.run(main())\n```\n\nBy default, the library creates a new connection to the API with each coroutine. If\nyou are calling a large number of coroutines (or merely want to squeeze out every second of runtime savings possible), an\n[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection\npooling:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom aiowatttime import Client\n\n\nasync def main() -> None:\n    async with ClientSession() as session:\n        client = await async_get_client("<EMAIL>", "<PASSWORD>", session=session)\n        # ...\n\n\nasyncio.run(main())\n```\n\n## Getting Accounts\n\nGetting all accounts associated with this email address is easy:\n\n```python\nimport asyncio\n\nfrom aioridwell import async_get_client\n\n\nasync def main() -> None:\n    client = await async_get_client("<EMAIL>", "<PASSWORD>")\n\n    accounts = await client.async_get_accounts()\n    # >>> {"account_id_1": RidwellAccount(...), ...}\n\n\nasyncio.run(main())\n```\n\nThe `RidwellAccount` object comes with some useful properties:\n\n* `account_id`: the Ridwell ID for the account\n* `address`: the address being serviced\n* `email`: the email address on the account\n* `full_name`: the full name of the account owner\n* `phone`: the phone number of the account owner\n* `subscription_id`: the Ridwell ID for the primary subscription\n* `subscription_active`: whether the primary subscription is active\n\n## Getting Pickup Events\n\nGetting pickup events associated with an account is easy, too:\n\n```python\nimport asyncio\n\nfrom aioridwell import async_get_client\n\n\nasync def main() -> None:\n    client = await async_get_client("<EMAIL>", "<PASSWORD>")\n\n    accounts = await client.async_get_accounts()\n    for account in accounts.values():\n        events = await account.async_get_pickup_events()\n        # >>> [RidwellPickupEvent(...), ...]\n\n        # You can also get just the next pickup event from today\'s date:\n        next_event = await account.async_get_next_pickup_event()\n        # >>> RidwellPickupEvent(...)\n\n\nasyncio.run(main())\n```\n\nThe `RidwellPickupEvent` object comes with some useful properties:\n\n* `pickup_date`: the date of the pickup (in `datetime.date` format)\n* `pickups`: a list of `RidwellPickup` objects\n* `state`: either `initialized` (not scheduled for pickup) or `scheduled`\n\nLikewise, the `RidwellPickup` object comes with some useful properties:\n\n* `category`: the category of the pickup (`standard`, `rotating`, or `add_on`)\n* `name`: the name of the item being picked up\n* `offer_id`: the Ridwell ID for this particular offer\n* `priority`: the pickup priority\n* `product_id`: the Ridwell ID for this particular product\n* `quantity`: the amount of the product being picked up\n\n### Calculating a Pickup Event\'s Esimated Cost\n\nCalculating the estimated cost of a pickup event is, you guessed it, easy:\n\n```python\nimport asyncio\n\nfrom aioridwell import async_get_client\n\n\nasync def main() -> None:\n    client = await async_get_client("<EMAIL>", "<PASSWORD>")\n\n    accounts = await client.async_get_accounts()\n    for account in accounts.values():\n        events = await account.async_get_pickup_events()\n        event_1_cost = await events[0].async_get_estimated_cost()\n        # >>> 22.00\n\n\nasyncio.run(main())\n```\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/aioridwell/issues)\n  or [initiate a discussion on one](https://github.com/bachya/aioridwell/issues/new).\n2. [Fork the repository](https://github.com/bachya/aioridwell/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `script/test`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/aioridwell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
