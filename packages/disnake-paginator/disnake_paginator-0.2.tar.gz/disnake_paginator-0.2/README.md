# disnake-paginator
A module containing paginators for disnake

## Examples
```py
async def ping_command(inter):
	paginator = disnake_paginator.ButtonPaginator(title="Pong", segments=["Hello", "World"], color=0x00ff00)
	await paginator.start(inter)

```

```py
async def on_message(message):
	if message.content == "!ping":
		paginator = disnake_paginator.ButtonPaginator(title="Pong", segments=["This is", "a message"])
		await paginator.start(disnake_paginator.wrappers.MessageInteractionWrapper(message))
```

