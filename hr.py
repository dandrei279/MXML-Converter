from parser import Parser
from question import Question
import re

class HR(Parser):
    def parseQuestion(self, question, questionText):
        current_pos = 0
        # set question text
        questionMatch = re.search('^((.|\n)+?)(\n[+-])', questionText[current_pos:])
        questiontext = questionMatch.group(1)
        question.setQuestion(questiontext)

        current_pos += len(questiontext) + 1

        # add answers
        while True:
            _answer = re.search('^([+-](.|\n[^+\-\n%])+)', questionText[current_pos:])
            if _answer:
                answer = _answer.group(0)
                question.addAnswer(answer[2:], answer[0] == '+')
                current_pos += len(answer) + 1
            else:
                break

    def parseTags(self, question, questionText):
        current_pos = 0

        # add tags
        while True:
            _tag = re.search('^([\w\s]+)(;|$)', questionText[current_pos:])
            if _tag:
                tag = _tag.group(1)
                question.addTag(tag)
                current_pos += len(tag) + 1
            else:
                break

    def load_question(self, input, xml, quiz):
        question = Question(xml, quiz)

        # extract tags
        tagsBlock = re.search('(%tags%\n)((.|\n)*)(\n%~tags%)', input)
        tagsText = tagsBlock.group(2)
        self.parseTags(question, tagsText)

        # extract question and answers
        questionBlock = re.search('(%question%\n)((.|\n)*)(\n%~question%)', input)
        questionText = questionBlock.group(2)
        self.parseQuestion(question, questionText)

        # extract general feedback (if any)
        feedbackBlock = re.search('(%feedback%\n)((.|\n)*)(\n%~feedback%)', input)
        if feedbackBlock:
            feedback = feedbackBlock.group(2)
            question.setFeedback(feedback)

        return question.toXML()
