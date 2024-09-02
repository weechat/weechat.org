# WeeChat.org

<p align="center">
  <img src="https://weechat.org/media/images/weechat_logo_large.png" alt="WeeChat" />
</p>

[![CI](https://github.com/weechat/weechat.org/actions/workflows/ci.yml/badge.svg)](https://github.com/weechat/weechat.org/actions)

WeeChat.org is the website for WeeChat, the extensible chat client.

Homepage: [https://weechat.org/](https://weechat.org/)

## Install

### Dependencies

The following packages are **required**:

- python ≥ 3.7
- python-django ≥ 2.0
- python-pygments
- python-tz
- PostgreSQL.

### Deploy

Run the install script:

```bash
./bin/install.sh
```

Run Django server:

```bash
./test.sh
```

And just point your browser on [http://127.0.0.1:8000/](http://127.0.0.1:8000/), that's all!

> [!IMPORTANT]
> Default settings can be used for testing purposes but must be overridden for production,
see the file [settings_local.template](weechat/settings_local.template) for more information.

## Copyright

Copyright © 2003-2024 [Sébastien Helleu](https://github.com/flashcode)

This file is part of WeeChat.org.

WeeChat.org is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

WeeChat.org is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with WeeChat.org.  If not, see <https://www.gnu.org/licenses/>.
