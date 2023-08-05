# Copyright (C) 2021 The InstanceLib Authors. All Rights Reserved.

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from typing import Union, Any

from ..instances import Instance
from ..typehints import KT

def to_key(instance_or_key: Union[KT, Instance[KT, Any, Any, Any]]) -> KT:
    """Returns the identifier of the instance if `instance_or_key` is an `Instance`
    or return the key if `instance_or_key` is a `KT`

    Parameters
    ----------
    instance_or_key : Union[KT, Instance]
        An implementation of `Instance` or an identifier typed variable

    Returns
    -------
    KT
        The identifer of the instance (or the input verbatim)
    """
    if isinstance(instance_or_key, Instance):
        return instance_or_key.identifier # type: ignore
    return instance_or_key