#This is taken from https://gist.github.com/muhammedfurkan/ff599af9e99802a2070bdef0577ff150 and fixed
import hashlib
import os
import random
import sys

from pyrogram import Client
from pyrogram.raw.functions.messages import GetDhConfig
from pyrogram.raw.functions.phone import RequestCall
from pyrogram.raw.types import PhoneCallProtocol

client = Client("my_account")

client.start()

def get_dh_config():
    class DH:
        def __init__(self, dh_config):
            self.p = int.from_bytes(dh_config.p, 'big')
            self.g = dh_config.g
            self.resp = dh_config
    x = GetDhConfig(version = 0, random_length = 256)
    return DH(client.send(x))


dh_config = get_dh_config()


class DynamicDict:
    def __setattr__(self, key, value):
        self.__dict__[key] = value


def get_rand_bytes(length=256):
    return bytes(x ^ y for x, y in zip(
        os.urandom(length), dh_config.resp.random
    ))


def integer_to_bytes(integer):
    return int.to_bytes(
        integer,
        length=(integer.bit_length() + 8 - 1) // 8,
        byteorder='big',
        signed=False
    )


def call_user(input_user):
    PROTOCOL = PhoneCallProtocol(min_layer=93, max_layer=93, library_versions = [""], udp_p2p=True)
    dhc = get_dh_config()
    state = DynamicDict()
    state.incoming = False
    state.user_id = input_user
    state.random_id = random.randint(0, 0x7fffffff - 1)
    state.g = dhc.g
    state.p = dhc.p
    state.a = 0
    while not (1 < state.a < state.p - 1):
        state.a = int.from_bytes(get_rand_bytes(), 'little')

    state.g_a = pow(state.g, state.a, state.p)
    state.g_a_hash = hashlib.sha256(integer_to_bytes(state.g_a)).digest()
    state.my_proto = PROTOCOL
    client.send(RequestCall(
        user_id=client.resolve_peer(state.user_id),
        random_id=state.random_id,
        g_a_hash=state.g_a_hash,
        protocol=state.my_proto))

call_user("@" + sys.argv[1])
