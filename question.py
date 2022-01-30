from xml.dom import minidom

class Question:
    def __init__(self, xml, quiz):
        self.xml = xml
        self.quiz = quiz
        self.tags = []
        self.answers = []
        self.correct_answers = []
        self.question = ""
        self.name = ""

    def setQuestion(self, raw_question):
        question = raw_question.replace("\n", " <br> ")
        self.question = question
        # self.name = question[0:28] + "..."

    def addAnswer(self, answer, correct=False):
        if correct:
            self.correct_answers.append(len(self.answers))
        self.answers.append(answer)

    def addTag(self, tag):
        self.tags.append(tag)

    def singleAnswer(self):
        return len(self.correct_answers) == 1

    def toXML(self):
        # <question> ... </question>
        question = self.xml.createElement('question')
        question.setAttribute('type', 'multichoice')
        self.quiz.appendChild(question)

        defaultgrade = self.xml.createElement('defaultgrade')
        question.appendChild(defaultgrade)

        _defaultgrade = self.xml.createTextNode('1.0000000')
        defaultgrade.appendChild(_defaultgrade)

        penalty = self.xml.createElement('penalty')
        question.appendChild(penalty)

        _penalty = self.xml.createTextNode('0.3333333')
        penalty.appendChild(_penalty)

        hidden = self.xml.createElement('hidden')
        question.appendChild(hidden)

        _hidden = self.xml.createTextNode('0')
        hidden.appendChild(_hidden)

        single = self.xml.createElement('single')
        question.appendChild(single)

        _single = self.xml.createTextNode(str(self.singleAnswer()).lower())
        single.appendChild(_single)

        # <name> ... </name>
        name = self.xml.createElement('name')
        question.appendChild(name)

        text = self.xml.createElement('text')
        name.appendChild(text)

        _name = self.xml.createTextNode(self.name)
        text.appendChild(_name)

        # <questiontext> ... </questiontext>
        questiontext = self.xml.createElement('questiontext')
        questiontext.setAttribute('format', 'html')
        question.appendChild(questiontext)

        text = self.xml.createElement('text')
        questiontext.appendChild(text)

        _questiontext = self.xml.createTextNode(self.question)
        text.appendChild(_questiontext)

        # <tags> ... </tags>
        tags = self.xml.createElement('tags')
        question.appendChild(tags)

        for self_tag in self.tags:
            tag = self.xml.createElement('tag')
            tags.appendChild(tag)

            text = self.xml.createElement('text')
            tag.appendChild(text)

            _tag = self.xml.createTextNode(self_tag)
            text.appendChild(_tag)

        for i in range(len(self.answers)):
            # <answer> ... </answer>
            
            # compute points for answer
            fraction = 0
            if i in self.correct_answers:
                fraction = 100. / len(self.correct_answers)
            
            answer = self.xml.createElement('answer')
            answer.setAttribute('fraction', str(fraction))
            question.appendChild(answer)

            text = self.xml.createElement('text')
            answer.appendChild(text)

            _answer = self.xml.createTextNode(self.answers[i])
            text.appendChild(_answer)

        return question
    
    def toString(self):
        return self.toXML().toprettyxml(indent="\t")
