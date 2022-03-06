from parser import Parser
from question import Question
import re

class HR(Parser):
    def load_question(self, input, xml, quiz):
        current_pos = 0
        # extract metadata
        metadata = re.search('^(.+?)\n', input).group(1)
        created_on = re.search('created_on:(.+?)(?=;)', metadata).group(0)
        difficulty = re.search('difficulty:([123]);', metadata).group(1)
        topic = re.search('topic:(.+?);', metadata).group(1)
        type_question = re.search('type:(.+?)$', metadata).group(1)

        # set difficulty according to Easy - Medium - Hard scale
        difficulties = ['Easy', 'Medium', 'Hard']
        difficulty = difficulties[int(difficulty) - 1]
        
        question = Question(xml, quiz)
        question.addTag(created_on)
        question.addTag(difficulty)
        question.addTag(topic)
        question.addTag(type_question)

        current_pos += len(metadata) + 1

        # add general feedback (if any)
        feedbackBlock = re.search('(%feedback%\n)((.|\n)*)(\n%~feedback%)', input[current_pos:])
        if feedbackBlock:
            feedback = feedbackBlock.group(2)
            question.setFeedback(feedback)
            current_pos += len(feedbackBlock.group(0)) + 1

        # set question text
        questionMatch = re.search('^((.|\n)+?)(\n[+-])', input[current_pos:])
        questiontext = questionMatch.group(1)
        question.setQuestion(questiontext)

        current_pos += len(questiontext) + 1

        # add answers
        while True:
            _answer = re.search('^([+-](.|\n[^+\-\n])+)', input[current_pos:])
            if _answer:
                answer = _answer.group(0)
                question.addAnswer(answer[2:], answer[0] == '+')
                current_pos += len(answer) + 1
            else:
                break

        return question.toXML()
