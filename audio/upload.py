import asyncio

import aiogram
import json
import os

bot = aiogram.Bot(os.getenv("TOKEN"))
admin_id = os.getenv("ADMIN_ID")
base_dir = os.path.dirname(os.path.abspath(__file__)) + '/voices'
packs = [
    "GQ",
    "кремниевая долина",
    "странные вопросы",
]


async def upload():
    sent_voices = []
    intro = ""
    outro = ""

    for pack_name in packs:
        print(pack_name)
        for file in os.listdir(base_dir + '/' + pack_name + "/"):
            question = open(base_dir + '/' + pack_name + "/" + file, mode="rb")
            voice_message = await bot.send_voice(admin_id, question)
            file_id = voice_message.voice.file_id
            if file.find("intro") >= 0:
                intro = file_id
            elif file.find("outro") >= 0:
                outro = file_id
            else:
                sent_voices.append(file_id)

            print(file, file_id)
        pack = {
            "questions.json": sent_voices,
            "intro": intro,
            "outro": outro
        }

        print(json.dumps(pack))
        sent_voices.clear()
        print("\n")


if __name__ == '__main__':
    asyncio.run(upload())
