# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgrest']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'pgrest',
    'version': '0.5.0',
    'description': 'PostgREST client for Python. This library provides an ORM interface to PostgREST.',
    'long_description': '# pgrest-client\n\nPostgREST client for Python. This library provides an ORM interface to PostgREST.\n\nFork of the supabase community Postgrest Client library for Python.\n\nStatus: **Unstable**\n\n## INSTALLATION\n\n### Requirements\n\n- Python >= 3.7\n- PostgreSQL >= 12\n- PostgREST >= 7\n\n### Local PostgREST server\n\nIf you want to use a local PostgREST server for development, you can use our preconfigured instance via Docker Compose.\n\n```sh\ndocker-compose up\n```\n\nOnce Docker Compose started, PostgREST is accessible at http://localhost:3000.\n\n## USAGE\n\n### Getting started\n\n```py\nimport asyncio\nfrom pgrest import Client\n\nasync def main():\n    async with Client("http://localhost:3000") as client:\n        r = await client.from_("countries").select("*").execute()\n        countries = r[0]\n\nasyncio.run(main())\n```\n\n### Create\n\n```py\nawait client.from_("countries").insert({ "name": "Việt Nam", "capital": "Hà Nội" }).execute()\n```\n\n### Read\n\n```py\nr = await client.from_("countries").select("id", "name").execute()\ncountries = r[0]\n```\n\n### Update\n\n```py\nawait client.from_("countries").eq("name", "Việt Nam").update({"capital": "Hà Nội"}).execute()\n```\n\n### Delete\n\n```py\nawait client.from_("countries").eq("name", "Việt Nam").delete().execute()\n```\n\n### General filters\n\n### Stored procedures (RPC)\n\n```py\nr = await client.rpc("hello_world").execute()\n```\n\n```py\nr = await client.rpc("echo_city", params={"name": "The Shire"}).execute()\n```\n\nAll above methods also have synchronous counterparts, under `pgrest._sync_client.SyncClient`.\n',
    'author': 'Anand Krishna',
    'author_email': 'anandkrishna2312@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anand2312/pgrest-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
