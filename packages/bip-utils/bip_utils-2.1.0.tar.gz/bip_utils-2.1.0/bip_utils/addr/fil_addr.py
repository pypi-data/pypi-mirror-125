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

"""Module for Filecoin address computation."""

# Imports
from enum import IntEnum, unique
from typing import Any, Union
from bip_utils.addr.iaddr_encoder import IAddrEncoder
from bip_utils.addr.utils import AddrUtils
from bip_utils.coin_conf import CoinsConf
from bip_utils.ecc import IPublicKey
from bip_utils.utils.base32 import Base32Encoder
from bip_utils.utils.misc import ConvUtils, CryptoUtils


@unique
class FillAddrTypes(IntEnum):
    """Enumerative for Filecoin address types."""

    SECP256K1 = 1
    BLS = 3


class FilAddrConst:
    """Class container for Filecoin address constants."""

    # Alphabet for base32
    BASE32_ALPHABET: str = "abcdefghijklmnopqrstuvwxyz234567"
    # Digest length in bytes
    DIGEST_BYTE_LEN: int = 20
    # Checksum length in bytes
    CHECKSUM_BYTE_LEN: int = 4


class FilAddrUtils:
    """Class container for Filecoin address utility functions."""

    @staticmethod
    def EncodeKeyBytes(pub_key_bytes: bytes,
                       addr_type: FillAddrTypes) -> str:
        """
        Get address in Filecoin format from public key bytes.

        Args:
            pub_key_bytes (bytes)    : Public key bytes
            addr_type (FillAddrTypes): Address type

        Returns:
            str: Address string
        """
        # Get address type
        addr_type_str = chr(addr_type + ord("0"))
        addr_type_byte = ConvUtils.IntegerToBytes(addr_type)

        # Compute public key hash and checksum
        pub_key_hash = CryptoUtils.Blake2b(pub_key_bytes,
                                           digest_size=FilAddrConst.DIGEST_BYTE_LEN)
        checksum = CryptoUtils.Blake2b(addr_type_byte + pub_key_hash,
                                       digest_size=FilAddrConst.CHECKSUM_BYTE_LEN)
        # Encode to base32
        b32_enc = Base32Encoder.EncodeNoPadding(pub_key_hash + checksum, FilAddrConst.BASE32_ALPHABET)

        return CoinsConf.Filecoin.Params("addr_prefix") + addr_type_str + b32_enc


class FilSecp256k1Addr(IAddrEncoder):
    """
    Filecoin address class based on secp256k1 keys.
    It allows the Filecoin address generation.
    """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, IPublicKey],
                  **kwargs: Any) -> str:
        """
        Get address in Filecoin format.

        Args:
            pub_key (bytes or IPublicKey): Public key bytes or object
            **kwargs: Not used

        Returns:
            str: Address string

        Raised:
            ValueError: If the public key is not valid
            TypeError: If the public key is not secp256k1 or the address type is not valid
        """
        pub_key_obj = AddrUtils.ValidateAndGetSecp256k1Key(pub_key)
        pub_key_bytes = pub_key_obj.RawUncompressed().ToBytes()

        return FilAddrUtils.EncodeKeyBytes(pub_key_bytes, FillAddrTypes.SECP256K1)
