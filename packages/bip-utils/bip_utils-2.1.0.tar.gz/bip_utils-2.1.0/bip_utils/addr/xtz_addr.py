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

"""Module for Tezos address computation."""

# Imports
from enum import Enum, unique
from typing import Any, Union
from bip_utils.addr.iaddr_encoder import IAddrEncoder
from bip_utils.addr.utils import AddrUtils
from bip_utils.base58 import Base58Encoder
from bip_utils.ecc import IPublicKey
from bip_utils.utils.misc import CryptoUtils


@unique
class XtzAddrPrefixes(Enum):
    """Enumerative for Tezos address prefixes."""

    TZ1 = b"\x06\xa1\x9f"
    TZ2 = b"\x06\xa1\xa1"
    TZ3 = b"\x06\xa1\xa4"


class XtzAddrConst:
    """Class container for Tezos address constants."""

    # Digest length in bytes
    DIGEST_BYTE_LEN: int = 20


class XtzAddr(IAddrEncoder):
    """
    Tezos address class.
    It allows the Tezos address generation.
    """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, IPublicKey],
                  **kwargs: Any) -> str:
        """
        Get address in Tezos format.

        Args:
            pub_key (bytes or IPublicKey): Public key bytes or object
            **kwargs: Not used

        Other Parameters:
            prefix (XtzAddrPrefixes): Address prefix

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not ed25519
        """

        # Get and check address type
        prefix = kwargs["prefix"]
        if not isinstance(prefix, XtzAddrPrefixes):
            raise TypeError("Address type is not an enumerative of XtzAddrPrefixes")

        # Get public key
        pub_key_obj = AddrUtils.ValidateAndGetEd25519Key(pub_key)

        # Compute Blake2b and encode in Base58 with checksum
        blake = CryptoUtils.Blake2b(pub_key_obj.RawCompressed().ToBytes()[1:],
                                    digest_size=XtzAddrConst.DIGEST_BYTE_LEN)
        return Base58Encoder.CheckEncode(prefix.value + blake)
