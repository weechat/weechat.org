# -*- coding: utf-8 -*-
# This file is auto-generated after changes in database, DO NOT EDIT!

from django.utils.translation import gettext_lazy

_i18n_doc_security = [
    gettext_lazy("/set irc.network.colors_receive off"),
    gettext_lazy("Buffer overflow when decoding IRC colors in strings."),
    gettext_lazy("Buffer overflow when removing quotes in DCC filename."),
    gettext_lazy("Buffer overflows in build of strings."),
    gettext_lazy("Crash when receiving special chars in IRC messages."),
    gettext_lazy("Create a trigger (with WeeChat >= 1.1): /trigger add irc_dcc_quotes modifier \"irc_in_privmsg\" \"${arguments} =~ ^[^ ]+ :${\\x01}DCC SEND ${\\x22} \" \"/.*//\""),
    gettext_lazy("Date/time conversion specifiers are expanded after replacing buffer local variables in name of log files. In some cases, this can lead to an error in function strftime and a crash caused by the use of an uninitialized buffer."),
    gettext_lazy("Do not use command /notify with nicks containing formatting chars like \"%\"."),
    gettext_lazy("Do not use irc protocol in relay plugin."),
    gettext_lazy("Missing verifications in SSL certificate, which allows man-in-the-middle attackers to spoof an SSL chat server via an arbitrary certificate."),
    gettext_lazy("Remove/unload all scripts calling function hook_process (for maximum safety)."),
    gettext_lazy("Turn off option \"irc.network.send_unknown_commands\" or do not use formatting chars like \"%\" when sending unknown commands to server."),
    gettext_lazy("Uncontrolled format string in API function infobar_printf."),
    gettext_lazy("Uncontrolled format string when IRC commands are redirected by relay plugin. If the output or redirected command contains formatting chars like \"%\", this can lead to a crash of WeeChat."),
    gettext_lazy("Uncontrolled format string when sending IRC \"ison\" command for nicks monitored with command /notify."),
    gettext_lazy("Uncontrolled format string when sending unknown IRC command to server (if option \"irc.network.send_unknown_commands\" is on)."),
    gettext_lazy("Unload the logger plugin: /plugin unload logger"),
    gettext_lazy("Untrusted command for function hook_process could lead to execution of commands, because of shell expansions (so the problem is only caused by some scripts, not by WeeChat itself)."),
]
