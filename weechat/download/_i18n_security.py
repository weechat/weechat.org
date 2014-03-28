# This file is auto-generated after changes in database, DO NOT EDIT!

from django.utils.translation import gettext_lazy

_i18n_download_security = [
    gettext_lazy("/set irc.network.colors_receive off"),
    gettext_lazy("Buffer overflow when decoding IRC colors in strings."),
    gettext_lazy("Buffer overflows in build of strings."),
    gettext_lazy("Crash when receiving special chars in IRC messages."),
    gettext_lazy("Do not use command /notify with nicks containing formatting chars like \"%\"."),
    gettext_lazy("Do not use irc protocol in relay plugin."),
    gettext_lazy("Missing verifications in SSL certificate, which allows man-in-the-middle attackers to spoof an SSL chat server via an arbitrary certificate."),
    gettext_lazy("Remove/unload all scripts calling function hook_process (for maximum safety)."),
    gettext_lazy("Turn off option \"irc.network.send_unknown_commands\" or do not use formatting chars like \"%\" when sending unknown commands to server."),
    gettext_lazy("Uncontrolled format string in API function infobar_printf."),
    gettext_lazy("Uncontrolled format string when IRC commands are redirected by relay plugin. If the output or redirected command contains formatting chars like \"%\", this can lead to a crash of WeeChat."),
    gettext_lazy("Uncontrolled format string when sending IRC \"ison\" command for nicks monitored with command /notify."),
    gettext_lazy("Uncontrolled format string when sending unknown IRC command to server (if option \"irc.network.send_unknown_commands\" is on)."),
    gettext_lazy("Untrusted command for function hook_process could lead to execution of commands, because of shell expansions (so the problem is only caused by some scripts, not by WeeChat itself)."),
]
