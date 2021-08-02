from dataclasses import dataclass
from typing import List

from services.packs import get_pack, get_pack_questions
from models.models import Question, Pack


class QuestionsEnded(Exception):
    ...


@dataclass
class QuestionAnswer:
    question: str
    answer: str


class Interview:

    def __init__(self, chat_id: int, pack_id: int):
        self.chat_id: int = chat_id
        self.pack: Pack = get_pack(pack_id)
        self.questions: List[Question] = get_pack_questions(pack_id)
        self.question_answers: List[QuestionAnswer] = []

    def save_answer(self, answer_file_id: str) -> None:
        #TODO: Достать id файла вопроса
        question_answer: QuestionAnswer = QuestionAnswer(question="", answer=answer_file_id)
        self.question_answers.append(question_answer)

    def get_next_question(self) -> str:
        # проверка не закончились ли вопросы
        if len(self.question_answers) == len(self.questions):
            raise QuestionsEnded
        else:
            return self.questions[len(self.question_answers)]

    def get_file_ids(self) -> List[str]:
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
