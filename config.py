#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/YukkiChatBot >.
#
# This file is part of < https://github.com/TeamYukki/YukkiChatBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiChatBot/blob/master/LICENSE >
#
# All rights reserved.
#

from os import getenv

from dotenv import load_dotenv

load_dotenv()

# Get it from my.telegram.org
API_ID = int(getenv("API_ID", "6"))
API_HASH = getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")

## Get it from @Botfather in Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", "5438498886:AAE4Ce_7yv3WjuCI1ANkM84gCNdjaTHlhCg")

# SUDO USERS
SUDO_USER = list(
    map(int, getenv("SUDO_USER", "5542739158").split())
)  # Input type must be interger

# ADMIN USERS
ADMIN_USER = list(
    map(int, getenv("ADMIN_USER", "5542739158 5520828938 817088672").split())
)  # Input type must be interger

# You'll need a Private Group ID for this.
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1001581035936"))

# Message to display when someone starts your bot
PRIVATE_START_MESSAGE = getenv(
    "PRIVATE_START_MESSAGE",
    "Hello! Welcome to SasteMemes Bot Send only dark/dank memes if you caught sending cringe memes you will be blocked from the bot",
)

# Database to save your chats and stats... Get MongoDB:-  https://notreallyshikhar.gitbook.io/yukkimusicbot/deployment/mongodb#4.-youll-see-a-deploy-cloud-database-option.-please-select-shared-hosting-under-free-plan-here
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://meme:meme@cluster0.fohmge4.mongodb.net/?retryWrites=true&w=majority")
