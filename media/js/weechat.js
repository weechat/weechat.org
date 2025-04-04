// SPDX-FileCopyrightText: 2003-2025 Sébastien Helleu <flashcode@flashtux.org>
//
// SPDX-License-Identifier: GPL-3.0-or-later

function set_cookie(key, value, path, ttl_days) {
    var d = new Date();
    d.setTime(d.getTime() + (ttl_days * 24 * 60 * 60 * 1000));
    document.cookie = key + "=" + value + "; path=" + path + "; expires=" + d.toUTCString();
}

function toggle(id, display) {
    document.getElementById(id).style.display = display;
}
