# This file is auto-generated after changes in database, DO NOT EDIT!

"""Translations for doc/security."""

# flake8: noqa
# pylint: disable=line-too-long,too-many-statements

from django.utils.translation import gettext_noop


def __i18n_doc_security():
    """Translations for doc/security."""
    gettext_noop("A buffer overflow happens in base 32 encoding in evaluated expressions, where padding is made in the resulting string.")
    gettext_noop("A buffer overflow happens when a new IRC message 005 is received with longer nick prefixes.\n<br>\nNote: a \"normal\" IRC server should not send again a message 005 with new nick prefixes, so the problem should be limited to malicious IRC servers.")
    gettext_noop("A buffer overflow happens when decoding some IRC colors in strings.")
    gettext_noop("A buffer overflows happens in build of strings in different places.")
    gettext_noop("A crash happens when decoding a malformed websocket frame in relay plugin.\n<br>\nThis happens even if a password is set in relay plugin, the malformed websocket frame can be received before the authentication of the client.")
    gettext_noop("A crash happens when receiving some WeeChat internal color codes in IRC messages.")
    gettext_noop("API")
    gettext_noop("Access of uninitialized pointer")
    gettext_noop("After changing options <code>weechat.network.gnutls_ca_system</code> or <code>weechat.network.gnutls_ca_user</code>, you must restart WeeChat.")
    gettext_noop("After changing the options <code>weechat.network.gnutls_ca_system</code> or <code>weechat.network.gnutls_ca_user</code>, the TLS verification function is lost.\n<br>\nConsequently, any connection to a server with TLS is made without verifying the certificate, which could lead to a man-in-the-middle attack.\n<br>\nConnection to IRC servers with TLS is affected, as well as any connection a server made by a plugin or a script using the function hook_connect.")
    gettext_noop("An integer overflow can happen when looping over items in a list.\n<br>\nThis can only happen in rare conditions on 32 and 64-bit systems, as the list must contain more than 2,147,483,647 elements.\n<br>\nOn 16-bit systems, this happens with a list that contains more than 32,767 elements.")
    gettext_noop("An integer overflow happens when using numbers with 9 or more decimals in calculation of expression, for example: <code>/eval -n ${calc:0.123456789}</code>.")
    gettext_noop("An integer overflow may happen in base32 encode/decode functions.")
    gettext_noop("Buffer overflow in base 32 encoding in evaluated expressions.")
    gettext_noop("Buffer overflow in function util_parse_time when the received date/time has no date and a length of 117 or more chars.\n<br>\nIt can be an issue in IRC plugin, where the \"time\" tag received in IRC messages is parsed using this function.")
    gettext_noop("Buffer overflow in parsing of date/time.")
    gettext_noop("Buffer overflow in range of chars in evaluated expressions.")
    gettext_noop("Buffer overflow in syntax highlighting of evaluated expressions.")
    gettext_noop("Buffer overflow on malformed IRC message 324 (channel mode).")
    gettext_noop("Buffer overflow on new IRC message 005 with nick prefixes.")
    gettext_noop("Buffer overflow when receiving a DCC file.")
    gettext_noop("Buffer overflow when receiving a malformed IRC message 324 (channel mode).")
    gettext_noop("Buffer overflow when removing quotes in DCC filename.")
    gettext_noop("Buffer overflows in build of strings.")
    gettext_noop("Core")
    gettext_noop("Core, IRC")
    gettext_noop("Core, Plugins")
    gettext_noop("Crash in API function infobar_printf.")
    gettext_noop("Crash on IRC commands sent via Relay.")
    gettext_noop("Crash on malformed IRC message 352 (WHO).")
    gettext_noop("Crash on malformed websocket frame in relay plugin.")
    gettext_noop("Crash on nicks monitored with /notify.")
    gettext_noop("Crash on send of unknown commands to IRC server.")
    gettext_noop("Crash when decoding IRC colors.")
    gettext_noop("Crash when receiving WeeChat color codes in IRC messages.")
    gettext_noop("Crash when receiving a malformed IRC message 352 (WHO).")
    gettext_noop("Date/time conversion specifiers are expanded after replacing buffer local variables in name of log files. In some cases, this can lead to an error in function strftime and a crash caused by the use of an uninitialized buffer.")
    gettext_noop("Do not use command <code>/notify</code> with nicks containing formatting chars like \"%\".")
    gettext_noop("Due to insufficient check of TLS certificate in IRC plugin, man-in-the-middle attackers can spoof a server via an arbitrary certificate.")
    gettext_noop("IRC")
    gettext_noop("IRC, Plugins")
    gettext_noop("Improper certificate validation")
    gettext_noop("Improper input validation")
    gettext_noop("Integer Overflow or Wraparound")
    gettext_noop("Integer overflow happens in conversion of a version as string to an integer number, if the version is greater than 0x7FFFFFFF (127.255.255.255), so if the version is at least 0x80000000 (128.0.0.0).")
    gettext_noop("Integer overflow in base32 decode/encode functions.")
    gettext_noop("Integer overflow in conversion of version to an integer number.")
    gettext_noop("Integer overflow in loops on lists.")
    gettext_noop("Integer overflow with decimal numbers in calculation of expression.")
    gettext_noop("Logger")
    gettext_noop("Out-of-bounds read")
    gettext_noop("Out-of-bounds write")
    gettext_noop("Possible man-in-the-middle attack in TLS connection to IRC server.")
    gettext_noop("Possible man-in-the-middle attack in TLS connection to servers.")
    gettext_noop("Relay")
    gettext_noop("Remote execution of commands via scripts.")
    gettext_noop("Remove/unload all scripts calling the API function hook_process.")
    gettext_noop("Remove/unload all scripts calling the API function infobar_printf.")
    gettext_noop("Strings are built with uncontrolled format in API function infobar_printf.")
    gettext_noop("Strings are built with uncontrolled format when IRC commands are redirected by relay plugin. If the output or redirected command contains formatting chars like \"%\", this can lead to a crash of WeeChat.")
    gettext_noop("Strings are built with uncontrolled format when nicks containing \"%\" are monitored with command <code>/notify</code>.")
    gettext_noop("Strings are built with uncontrolled format when unknown IRC commands are sent to server, if option <code>irc.network.send_unknown_commands</code> is enabled.")
    gettext_noop("There are multiple ways to mitigate this issue:\n<ul>\n  <li>Rremove all relays, see: <code>/help relay</code></li>\n  <li>Unload relay plugin with command: <code>/plugin unload relay</code> and see: <code>/help weechat.plugin.autoload</code></li>\n  <li>Secure relay to allow only some trusted IP addresses, see: <code>/help relay.network.allowed_ips</code></li>\n</ul>")
    gettext_noop("There are multiple ways to mitigate this issue:\n<ul>\n  <li>Turn off option to send unknown commands: <code>/set irc.network.send_unknown_commands off</code></li>\n  <li>Do not use formatting chars like \"%\" when sending unknown commands to server.</li>\n</ul>")
    gettext_noop("Turn of handling of colors in incoming IRC messages:\n\n<p><pre><code>/set irc.network.colors_receive off</code></pre></p>")
    gettext_noop("Untrusted command for function hook_process could lead to execution of commands, because of shell expansions (so the problem is only caused by some scripts, not by WeeChat itself).")
    gettext_noop("Use of invalid pointer in build of log filename.")
    gettext_noop("With WeeChat ≥ 1.1, you can create a trigger:\n\n<p><pre><code>/trigger add fix_irc_352 modifier \"irc_in_352\" \"${arguments} =~ .* \\*$\" \"/.*//\"</code></pre></p>\n\nWith any older version, there is no simple mitigation, you must upgrade WeeChat.")
    gettext_noop("With WeeChat ≥ 1.1, you can create a trigger:\n\n<p><pre><code>/trigger add irc_dcc_quotes modifier \"irc_in_privmsg\" \"${arguments} =~ ^[^ ]+ :${\\x01}DCC SEND ${\\x22} \" \"/.*//\"</code></pre></p>\n\nWith any older version, there is no simple mitigation, you must upgrade WeeChat.")
    gettext_noop("You can remove all relays of type \"irc\", see <code>/help relay</code>.")
    gettext_noop("You can unload the logger plugin, thus stopping recording of all buffers: <code>/plugin unload logger</code>.")
