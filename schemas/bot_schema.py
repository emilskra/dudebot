import enum


class InterviewButtons(str, enum.Enum):
    END = 'завершить'
    REPEAT = 'заново'


class BotTexts(str, enum.Enum):
    WELCOME = 'привет! я возьму у тебя интервью'
    START = 'отлично, я буду присылать вопрос, а ты мне отвечай голосовым сообщением'
    CHOOSE_PACK = 'выбери пак:'
    WAIT = 'подожди, я соберу в один файл'
    END = 'готово, лови'
    ERROR = 'не понял'
