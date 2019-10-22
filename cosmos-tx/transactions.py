#!/usr/bin/env python
# -*- coding: utf-8 -*-


import base64
import json
import hashlib
import requests
from ecdsa import SigningKey, SECP256k1
from address import privkey_to_address, privkey_to_pubkey
from account import get_account_info


class Transaction:
    def __init__(
        self,
        privkey,
        account_num,
        sequence,
        fee,
        gas,
        memo="",
        chain_id="cosmoshub-2",
        sync_mode="sync",
    ):
        self.privkey = privkey
        self.account_num = account_num
        self.sequence = sequence
        self.fee = fee
        self.gas = gas
        self.memo = memo
        self.chain_id = chain_id
        self.sync_mode = sync_mode
        self.msgs = []

    def add_atom_transfer(self, recipient, amount):
        self.msgs.append(
            {
                "type": "cosmos-sdk/MsgSend",
                "value": {
                    "from_address": privkey_to_address(self.privkey),
                    "to_address": recipient,
                    "amount": [{"denom": "uatom", "amount": str(amount)}],
                },
            }
        )

    def _get_sign_message(self):
        return {
            "chain_id": self.chain_id,
            "account_number": str(self.account_num),
            "fee": {"gas": str(self.gas), "amount": [{"amount": str(self.fee), "denom": "uatom"}]},
            "memo": self.memo,
            "sequence": str(self.sequence),
            "msgs": self.msgs,
        }

    def _sign(self):
        message_str = json.dumps(self._get_sign_message(), separators=(",", ":"), sort_keys=True)
        message_bytes = message_str.encode("utf-8")

        privkey = SigningKey.from_string(self.privkey.decode("hex"), curve=SECP256k1)
        signature_compact = privkey.sign(message_bytes, hashfunc=hashlib.sha256)

        signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
        return signature_base64_str

    def get_pushable_tx(self):
        pubkey = privkey_to_pubkey(self.privkey)
        base64_pubkey = base64.b64encode(pubkey.decode("hex")).decode("utf-8")
        pushable_tx = {
            "tx": {
                "msg": self.msgs,
                "fee": {
                    "gas": str(self.gas),
                    "amount": [{"denom": "uatom", "amount": str(self.fee)}],
                },
                "memo": self.memo,
                "signatures": [
                    {
                        "signature": self._sign(),
                        "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": base64_pubkey},
                        "account_number": str(self.account_num),
                        "sequence": str(self.sequence),
                    }
                ],
            },
            "mode": self.sync_mode,
        }
        return json.dumps(pushable_tx, separators=(",", ":"))

    def broadcast_tx(self, pushable_tx, url="http://node01.ip.sx:1317/txs"):
        resp = requests.post(url=url, data=pushable_tx)
        return resp.content


if __name__ == "__main__":
    acct_info = get_account_info("cosmos1s30lpz2y40tmv8hqd9jdwl5hjua4danekymzq2")
    account_num = acct_info.get("value").get("account_number")
    sequence = acct_info.get("value").get("sequence")

    tx = Transaction(
        privkey="",
        account_num=account_num,
        sequence=sequence,
        fee=50,
        gas=30000,
        memo="",
        chain_id="cosmoshub-2",
        sync_mode="sync",
    )
    tx.add_atom_transfer(recipient="cosmos1s30lpz2y40tmv8hqd9jdwl5hjua4danekymzq2", amount=1000)
    pushable_tx = tx.get_pushable_tx()
    print pushable_tx

    resp_content = tx.broadcast_tx(pushable_tx)
    print resp_content


