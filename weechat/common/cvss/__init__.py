# Copyright (c) 2016 Red Hat, Inc.
# Author: Stanislav Kontar, Red Hat Product Security
# License: LGPLv3+

# Copy of the "cvss" Python package version 3.6, with CVSS 3 and CVSS 4
# support only: https://github.com/RedHatProductSecurity/cvss
#
# Changes from the original package: removed CVSS 2 and interactive mode.

from .cvss3 import CVSS3
from .cvss4 import CVSS4
from .exceptions import CVSS3Error, CVSS4Error, CVSSError

__version__ = "3.6"
