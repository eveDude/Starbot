**STARBOT**

AN EVE ONLINE ZKILLBOARD to DISCORD message forwarder.

It connects to the ZKillboard websocket stream,
and listens for specific Character, Corp or Ally killmails.
It then forwards links of these kills to Discord via webhook.

Written in Python, utilizing Docker (used to restart the bot on websocket-connection-abort/exit/general-failure, this -should- be improved)

*Configuration*

Edit starbot/starbot.ini.example and alter the following values:

* CORPS = 1,2,3,4  # comma seperated list of CORPS you want kills forwareded for
* ALLYS = 1,2,3,4  # comma seperated list of ALLYS you want kills forwareded for
* Webhook = "somelink" # Link to your discord webook, see https://support.discord.com/hc/en-us/articles/228383668

*Credits*

https://www.eveonline.com/


https://zkillboard.com/


https://github.com/MatthewATaylor/discord_notify


https://discord.com/



not affiliated with Signal Cartel
