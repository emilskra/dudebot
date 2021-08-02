import telebot, os, json

bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode=None)

MYID = os.getenv("MYID")
PACK_ID = 1

PACK_NAME = "GQ"
#PACK_NAME = "кремниевая долина"

sent_voices = []
intro = ""
outro = ""

for file in os.listdir(PACK_NAME + "/"):
    question = open(PACK_NAME + "/" + file, mode="rb")
    file_id = bot.send_voice(MYID, question).voice.file_id
    if file.find("intro") >= 0:
        intro = file_id
    elif file.find("outro") >= 0:
        outro = file_id
    else:
        sent_voices.append(file_id)

pack = {
    "questions": sent_voices,
    "intro": intro,
    "outro": outro
}

print(json.dumps(pack))

