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

"""Module for Stellar address computation."""

# Imports
from enum import IntEnum, unique
from typing import Any, Union
from bip_utils.addr.iaddr_encoder import IAddrEncoder
from bip_utils.addr.utils import AddrUtils
from bip_utils.ecc import IPublicKey
from bip_utils.utils.base32 import Base32Encoder
from bip_utils.utils.misc import ConvUtils, CryptoUtils


@unique
class XlmAddrTypes(IntEnum):
    """Enumerative for Stellar address types."""

    PUB_KEY = 6 << 3
    PRIV_KEY = 18 << 3


class XlmAddr(IAddrEncoder):
    """
    Stellar address class.
    It allows the Stellar address generation.
    """

    @staticmethod
    def EncodeKey(pub_key: Union[bytes, IPublicKey],
                  **kwargs: Any) -> str:
        """
        Get address in Stellar format.

        Args:
            pub_key (bytes or IPublicKey): Public key bytes or object
            **kwargs: Not used

        Other Parameters:
            addr_type (XlmAddrTypes): Address type

        Returns:
            str: Address string

        Raises:
            ValueError: If the public key is not valid
            TypeError: If the public key is not ed25519
        """

        # Get and check address type
        addr_type = kwargs["addr_type"]
        if not isinstance(addr_type, XlmAddrTypes):
            raise TypeError("Address type is not an enumerative of XlmAddrTypes")

        # Get public key
        pub_key_obj = AddrUtils.ValidateAndGetEd25519Key(pub_key)
        payload = ConvUtils.IntegerToBytes(addr_type) + pub_key_obj.RawCompressed().ToBytes()[1:]

        # Compute checksum
        checksum = ConvUtils.ReverseBytes(CryptoUtils.XModemCrc(payload))
        # Encode to base32
        return Base32Encoder.EncodeNoPadding(payload + checksum)
