import math
import requests
from two1.wallet import Wallet, exceptions
from two1.bitcoin.utils import bytes_to_str, hex_str_to_bytes
from two1.bitcoin.crypto import PublicKey
from two1.bitcoin.script import Script

wallet = Wallet()
SRV_ACCT = 'signing'

class wallet_helper():
   def payout_pubkey(self):
      pubkey = wallet.get_payout_public_key(SRV_ACCT)
      return pubkey

   def payout_pubkey_str(self):
      pubkey_str = bytes_to_str(self.payout_pubkey().compressed_bytes).upper()
      return pubkey_str

   def create_contract(self, wager):
      two1_home = PublicKey.from_hex(wager.home_pubkey)
      two1_away = PublicKey.from_hex(wager.away_pubkey)
      two1_server = PublicKey.from_hex(wager.server_pubkey)

      public_keys = [two1_server.compressed_bytes, two1_home.compressed_bytes, two1_away.compressed_bytes]
      redeem_script = Script.build_multisig_redeem(2, public_keys)

      data = {
         'script_address': redeem_script.address(),
         'script_hex': redeem_script.to_hex()
      }

      return data

   def usd_to_satoshi(self, owe, usd_num):
      x = (owe / usd_num) * 100000000
      return math.ceil(x)

   def rec_fee():
      url = "https://bitcoinfees.21.co/api/v1/fees/recommended"
      r = requests.get(url)
      if r.status_code == 200:
         return r.json()
      else:
         return { 'fastestFee': 50 }
