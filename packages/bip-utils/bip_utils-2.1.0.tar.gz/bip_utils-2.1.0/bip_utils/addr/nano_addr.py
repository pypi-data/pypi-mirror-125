# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Module for Nano address computation."""

# Imports
from typing import Any, Union
from bip_utils.addr.iaddr_encoder import IAddrEncoder
from bip_utils.addr.utils import AddrUtils
from bip_utils.coin_conf import CoinsConf
from bip_utils.ecc import IPublicKey
from bip_utils.utils.base32 import Base32Encoder
from bip_utils.utils.misc import ConvUtils, CryptoUtils


class NanoAddrConst:
    """Class container for Nano address constants."""

    # Alphabet for base32
    BASE32_ALPHABET: str = "13456789abcdefghijkmnopqrstuwxyz"
    # Payload padding
    PAYLOAD_PAD: bytes = b"\x00\x00\x00"
    # Encoded padding length in bytes
    ENC_PAYLOAD_PAD_BYTE_LEN: int = 4
    # Digest length in bytes
    DIGEST_BYTE_LEN: int = 5


class NanoAddr(IAddrEncoder):
    """
    Nano address class.
    It allows the Nano address generation.
    """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, IPublicKey],
                  **kwargs: Any) -> str:
        """
        Get address in Nano format.

        Args:
            pub_key (bytes or IPublicKey): Public key bytes or object
            **kwargs: Not used

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not ed25519-blake2b
        """
        pub_key_obj = AddrUtils.ValidateAndGetEd25519Blake2bKey(pub_key)
        pub_key_bytes = pub_key_obj.RawCompressed().ToBytes()[1:]

        # Compute checksum
        checksum = ConvUtils.ReverseBytes(CryptoUtils.Blake2b(pub_key_bytes,
                                                              digest_size=NanoAddrConst.DIGEST_BYTE_LEN))
        # Encode to base32
        payload = NanoAddrConst.PAYLOAD_PAD + pub_key_bytes + checksum
        b32_enc = Base32Encoder.EncodeNoPadding(payload, NanoAddrConst.BASE32_ALPHABET)

        # Add prefix
        return CoinsConf.Nano.Params("addr_prefix") + b32_enc[NanoAddrConst.ENC_PAYLOAD_PAD_BYTE_LEN:]
