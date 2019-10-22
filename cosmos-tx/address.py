#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
import bech32
from ecdsa import SigningKey, SECP256k1


def generate_wallet():
    privkey = SigningKey.generate(curve=SECP256k1)
    privkey_hex = privkey.to_string().encode("hex")
    return {
        "private_key": privkey_hex,
        "public_key": privkey_to_pubkey(privkey_hex),
        "address": privkey_to_address(privkey_hex),
    }


def privkey_to_pubkey(privkey_hex):
    privkey_bytes = privkey_hex.decode("hex")
    privkey = SigningKey.from_string(privkey_bytes, curve=SECP256k1)
    pubkey = privkey.get_verifying_key()
    pubkey_bytes = pubkey.to_string()
    if ord(pubkey_bytes[63]) % 2 == 0:
        pubkey_bytes = "\x02" + pubkey_bytes[0:32]
    else:
        pubkey_bytes = "\x03" + pubkey_bytes[0:32]
    pubkey_hex = pubkey_bytes.encode("hex")
    return pubkey_hex


def pubkey_to_address(pubkey_hex):
    pubkey_bytes = pubkey_hex.decode("hex")
    s = hashlib.new("sha256", pubkey_bytes).digest()
    r = hashlib.new("ripemd160", s).digest()
    return bech32.bech32_encode("cosmos", bech32.convertbits(r, 8, 5))


def privkey_to_address(privkey_hex):
    pubkey_hex = privkey_to_pubkey(privkey_hex)
    return pubkey_to_address(pubkey_hex)


if __name__ == "__main__":
    # print generate_wallet()

    print privkey_to_pubkey("1ed27f39a70e6dfda0b4aac40b830e25bfe644477f3a61e62371611c683544aa")
    print pubkey_to_address("02a0ebf78f928723ee4fed610115263a33e49492502b6ead39e61481d6d5b096c6")
    print privkey_to_address("1ed27f39a70e6dfda0b4aac40b830e25bfe644477f3a61e62371611c683544aa")

