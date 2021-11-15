import requests


def get_fees(which=None):
    fees = requests.get("https://mempool.space/api/v1/fees/recommended").json()
    return fees[which] if which else fees
