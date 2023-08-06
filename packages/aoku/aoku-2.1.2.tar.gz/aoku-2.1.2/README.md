# About
The Aoku.py library is a module with simplified functions through which anyone can create their own Discord bot.

Aoku.py Easy to learn and also does not have any complex functions

# Example

```py
from aoku import aokuBot

bot = aokuBot(
	intents = True,
	selfbot = False
)

bot.onReady("Bot is ready to use!")
bot.onMessage()

bot.newCommand(
	name = "!ping",
	code = "Pong! $pingms"
)

bot.newCommand(
	name = "!uptime",
	code = "Uptime: $uptime"
)

bot.start("BOT_TOKEN", selfbot = False)
```