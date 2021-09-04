# This file is auto-generated after changes in database, DO NOT EDIT!

"""Translations for doc/security."""

# flake8: noqa
# pylint: disable=line-too-long,too-many-statements

from django.utils.translation import gettext_noop


def __i18n_doc_security():
    """Translations for doc/security."""
    gettext_noop("/set irc.network.colors_receive off")
    gettext_noop("Buffer overflow when a new IRC message 005 is received with longer nick prefixes.")
    gettext_noop("Buffer overflow when decoding IRC colors in strings.")
    gettext_noop("Buffer overflow when receiving a malformed IRC message 324 (channel mode).")
    gettext_noop("Buffer overflow when removing quotes in DCC filename.")
    gettext_noop("Buffer overflows in build of strings.")
    gettext_noop("Crash when decoding a malformed websocket frame in relay plugin.")
    gettext_noop("Crash when receiving a malformed IRC message 352 (WHO).")
    gettext_noop("Crash when receiving special chars in IRC messages.")
    gettext_noop("Create a trigger (with WeeChat >= 1.1): /trigger add irc_dcc_quotes modifier \"irc_in_privmsg\" \"${arguments} =~ ^[^ ]+ :${\\x01}DCC SEND ${\\x22} \" \"/.*//\"")
    gettext_noop("Date/time conversion specifiers are expanded after replacing buffer local variables in name of log files. In some cases, this can lead to an error in function strftime and a crash caused by the use of an uninitialized buffer.")
    gettext_noop("Do not use command /notify with nicks containing formatting chars like \"%\".")
    gettext_noop("Do not use irc protocol in relay plugin.")
    gettext_noop("Either: remove all relays, unload relay plugin or secure relay to allow only some trusted IP addresses (option relay.network.allowed_ips).")
    gettext_noop("Missing verifications in SSL certificate, which allows man-in-the-middle attackers to spoof an SSL chat server via an arbitrary certificate.")
    gettext_noop("Remove/unload all scripts calling function hook_process (for maximum safety).")
    gettext_noop("Turn off option \"irc.network.send_unknown_commands\" or do not use formatting chars like \"%\" when sending unknown commands to server.")
    gettext_noop("Uncontrolled format string in API function infobar_printf.")
    gettext_noop("Uncontrolled format string when IRC commands are redirected by relay plugin. If the output or redirected command contains formatting chars like \"%\", this can lead to a crash of WeeChat.")
    gettext_noop("Uncontrolled format string when sending IRC \"ison\" command for nicks monitored with command /notify.")
    gettext_noop("Uncontrolled format string when sending unknown IRC command to server (if option \"irc.network.send_unknown_commands\" is on).")
    gettext_noop("Unload the logger plugin: /plugin unload logger")
    gettext_noop("Untrusted command for function hook_process could lead to execution of commands, because of shell expansions (so the problem is only caused by some scripts, not by WeeChat itself).")
