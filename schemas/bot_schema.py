import enum


class InterviewButtons(str, enum.Enum):
    END = 'завершить'
    REPEAT = 'заново'


class BotTexts(str, enum.Enum):
    WELCOME = 'Привет! Я возьму у тебя интервью'
    START = 'отлично, я буду присылать вопрос, а ты мне отвечай голосовым сообщением'
    CHOOSE_PACK = 'Выбери пак:'
    WAIT = 'подожди, я соберу в один файл'
    END = 'готово, лови'
    ERROR = 'не понял'
