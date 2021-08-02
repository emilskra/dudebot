from services.packs import get_pack
from models.models import QuestionAnswer


class QuestionsEnded(Exception):
    ...


class Interview:

    def __init__(self, chat_id: int, pack_id: int):
        self.chat_id = chat_id
        self.pack = get_pack(pack_id)
        self.question_answers = []
        self.state = 0

    def save_answer(self, answer_file_id: str) -> str:
        question_answer = QuestionAnswer(answer=answer_file_id)
        self.question_answers.append(question_answer)

        # вопросы закончились
        if len(self.question_answers) == len(self.pack.questions):
            raise QuestionsEnded
        else:
            return self.question_answers[self.state].question

    def get_file_ids(self) -> list:
        """
        Собирает интервью с интро и аутро файлом
        :return: список id файлов
        """

        files_ids = []

        intro = self.pack.intro
        if intro:
            files_ids.append(intro)

        # последовательно добавим вопрос - ответ
        for question_answer in self.question_answers:
            files_ids.append(question_answer.question)
            files_ids.append(question_answer.answer)

        outro = self.pack.outro
        if outro:
            files_ids.append(outro)

        return files_ids
