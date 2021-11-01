from xml.dom import minidom

class Question:
    def __init__(self, question):
        self.question = question
        self.name = question[0:20]
        self.tags = []
        self.answers = []
        self.correct_answers = []

    def addAnswer(self, answer, correct=False):
        if correct:
            self.correct_answers.append(len(self.answers))
        self.answers.append(answer)

    def addTag(self, tag):
        self.tags.append(tag)

    def singleAnswer(self):
        return len(self.correct_answers) == 1

    def toString(self):
        xml = minidom.Document()

        # <question> ... </question>
        question = xml.createElement('question')
        question.setAttribute('type', 'multichoice')
        xml.appendChild(question)

        defaultgrade = xml.createElement('defaultgrade')
        question.appendChild(defaultgrade)

        _defaultgrade = xml.createTextNode('1.0000000')
        defaultgrade.appendChild(_defaultgrade)

        penalty = xml.createElement('penalty')
        question.appendChild(penalty)

        _penalty = xml.createTextNode('0.3333333')
        penalty.appendChild(_penalty)

        hidden = xml.createElement('hidden')
        question.appendChild(hidden)

        _hidden = xml.createTextNode('0')
        hidden.appendChild(_hidden)


        single = xml.createElement('single')
        question.appendChild(single)

        _single = xml.createTextNode(str(self.singleAnswer()).lower())
        single.appendChild(_single)

        # <name> ... </name>
        name = xml.createElement('name')
        question.appendChild(name)

        text = xml.createElement('text')
        name.appendChild(text)

        _name = xml.createTextNode(self.name)
        text.appendChild(_name)

        # <questiontext> ... </questiontext>
        questiontext = xml.createElement('questiontext')
        questiontext.setAttribute('format', 'html')
        question.appendChild(questiontext)

        text = xml.createElement('text')
        questiontext.appendChild(text)

        _questiontext = xml.createTextNode(self.question)
        text.appendChild(_questiontext)

        # <tags> ... </tags>
        tags = xml.createElement('tags')
        question.appendChild(tags)

        for self_tag in self.tags:
            tag = xml.createElement('tag')
            tags.appendChild(tag)

            text = xml.createElement('text')
            tag.appendChild(text)

            _tag = xml.createTextNode(self_tag)
            text.appendChild(_tag)

        for i in range(len(self.answers)):
            # <answer> ... </answer>
            
            # compute points for answer
            fraction = 0
            if i in self.correct_answers:
                fraction = 100. / len(self.correct_answers)
            
            answer = xml.createElement('answer')
            answer.setAttribute('fraction', str(fraction))
            question.appendChild(answer)

            text = xml.createElement('text')
            answer.appendChild(text)

            _answer = xml.createTextNode(self.answers[i])
            text.appendChild(_answer)

        return question.toprettyxml(indent ="\t") 
