#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import base64
import requests
import decimal
import math


def get_account_balance(acct_addr, url="http://node01.ip.sx:1317/bank/balances"):
    url = "%s/%s" % (url, acct_addr)
    resp = requests.get(url=url, timeout=30)
    objs = json.loads(resp.content)
    acct_balance = 0
    for obj in objs:
        if obj.get("denom") == "uatom":
            acct_balance = int(obj.get("amount"))
            break
    acct_balance = decimal.Decimal(acct_balance) / decimal.Decimal(math.pow(10, 6))
    return acct_balance


def get_account_info(acct_addr, node_url="http://node01.ip.sx:26657"):
    data_obj = {"Address":acct_addr}
    req_obj = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "abci_query",
            "params": {
                "data": base64.b16encode(json.dumps(data_obj)),
                "height": "0",
                "path": "custom/acc/account",
                "prove": False
            }
        }
    resp = requests.post(url=node_url, json=req_obj, timeout=30)
    resp_data_obj = base64.b64decode(resp.json().get("result").get("response").get("value"))
    return json.loads(resp_data_obj)


if __name__ == "__main__":
    print get_account_balance("cosmos1s30lpz2y40tmv8hqd9jdwl5hjua4danekymzq2")
    print get_account_info("cosmos1s30lpz2y40tmv8hqd9jdwl5hjua4danekymzq2")



