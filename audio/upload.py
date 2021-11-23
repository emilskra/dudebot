import asyncio

import aiogram, os, json

bot = aiogram.Bot(os.getenv("TOKEN"))
admin_id = os.getenv("ADMIN_ID")
base_dir = os.path.dirname(os.path.abspath(__file__)) + '/voices'
packs = [
    "GQ",
    # "кремниевая долина",
]


async def upload():
    sent_voices = []
    intro = ""
    outro = ""

    for pack_name in packs:
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

            print(file_id)

    return sent_voices, intro, outro


if __name__ == '__main__':
    sent_voices, intro, outro = asyncio.run(upload())
    pack = {
        "questions": sent_voices,
        "intro": intro,
        "outro": outro
    }

    print(json.dumps(pack))
