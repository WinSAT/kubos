# WinSAT-1 Gateway

This Gateway interacts with Major Tom using the Gateway API and the WinSAT-1 Satellite which responds to commands, generates telemetry, and uplinks/downlinks files.

Most of the information and resources here have been taken from the [Demo Python Gateway](https://github.com/kubos/example-python-gateway) and modified for our use with WinSAT-1.

## Gateway Package

This demo gateway uses the [Major Tom Gateway Package](https://pypi.org/project/majortom-gateway/).

## Local Setup

Clone locally to use it with Major Tom.

Requires Python 3.6+ and package requirements are in `requirements.txt`. Install with the command:

```pip3 install -r requirements.txt```

## Major Tom Setup

A Gateway has already been created in Major Tom for the WinSAT-1 satellite. Login to Major Tom and
navigate to the Gateway. Once there you'll need the __Authentication Token__ to connect the demo gateway.

## Connect the Gateway

Run the following command to connect to Major Tom:

```python3 run.py {MAJOR-TOM-HOSTNAME} {YOUR-GATEWAY-AUTHENTICATION-TOKEN}```

For Example:

```python3 run.py app.majortom.cloud 4b1273101901225a9d3df4882884b26e139cdeb49d2c1a50a51baf66c3a42623```

Once you run this, should should see Major Tom respond with a `hello` message:

```2019-08-19 12:04:46,151 - major_tom.major_tom - INFO - Major Tom says hello: {'type': 'hello', 'hello': {'mission': 'Demo'}}```

## What does this Demo Satellite do?

Now that you've connected the gateway, the command definitions defined here will be automatically loaded in for WinSAT-1 satellite. 
You can now issue those commands to the satellite through the connected Gateway.

To find these commands, go to Major Tom under mission WinSAT and find WinSAT-1 in the Satellites Menu.

Clicking on it will take you to its commanding page, and you can fire away!

The next step will be to integrate this setup with actual satellite hardware.