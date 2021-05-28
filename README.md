# BanBot
A bot that can "ban" users from a Discord server. However, instead of banning them, their access to all channels is revoked, apart from the predefined Ban Appeal channel. The bot also scans all new users and catches anyone attempting to evade the ban.

# Commands
!config #channel - will set up the provided channel as the ban appeal channel, create a "Banned" role, and remove access for the role from all text and voice channels apart from the appeal channel
!ban @user <reason> - removes all the user's roles and gives them the Banned role. DMs them the reason, or, if no reason is given, a notification that they have been banned and may appeal.
