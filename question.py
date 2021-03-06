from pygments import highlight
from pygments.lexers.c_cpp import CLexer
from pygments.lexers import guess_lexer
from pygments.formatters import ImageFormatter
from xml.dom import minidom

import re
import time

class Question:
    def __init__(self, xml, quiz):
        self.xml = xml
        self.quiz = quiz
        self.tags = []
        self.answers = []
        self.correct_answers = []
        self.question = ""
        self.name = ""
        self.feedback = ""

    def HTMLize(self, string):
        # Format code blocks and translate `\n` to `<br>`
        _code_block = re.search('(```\n)((.|\n)*)(```)', string)
        if _code_block:
            # get the code
            code_block = _code_block.group(2)

            # uniq file name for the image
            filename = 'code_{current_time}.png'.format(current_time = time.time())

            lexer = CLexer()
            # generate formatted code as PNG file
            with open(filename, "wb+") as f:
                f.write(highlight(code_block, lexer, ImageFormatter()))

            # use placeholder to embed code in questiontext
            string = string.replace(_code_block.group(0), "###_{filename}_###").format(filename = filename)

            # look for other code_sequence
            _code_block = re.search('(?:```)(.|\n)*(?:```)', string)
        return string.replace("\n", " <br> ")

    def setFeedback(self, feedback):
        self.feedback = self.HTMLize(feedback)

    def setQuestion(self, raw_question):
        question = self.HTMLize(raw_question)
        self.question = question

    def addAnswer(self, answer, correct=False):
        if correct:
            self.correct_answers.append(len(self.answers))
        self.answers.append(self.HTMLize(answer))

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

        # <questiontext> ... </questiontext>
        questiontext = self.xml.createElement('questiontext')
        questiontext.setAttribute('format', 'html')
        question.appendChild(questiontext)

        text = self.xml.createElement('text')
        questiontext.appendChild(text)

        self.hasAttachment = False
        self.filepath = ""
        
        file_placeholder = re.search('###_(.+)_###', self.question)
        if file_placeholder != None:
            # replace placeholder with HTML
            self.filepath = file_placeholder.group(1)
            self.filename = re.search('([\\w\.]*$)', self.filepath).group(0)

            self.hasAttachment = True
            
            html_class = 'class="img-fluid atto_image_button_text-bottom"'
            html_style = 'style="max-height:500px;max-width:500px;"'
            html_img_tag = '<img src="@@PLUGINFILE@@/{filename}" alt="img" {html_class} {html_style}>'.format(
                filename = self.filename,
                html_style = html_style,
                html_class = html_class
            )
            self.question = self.question.replace(file_placeholder.group(0), html_img_tag)
        
        self.name = self.question[0:28] + "..."

        _questiontext = self.xml.createTextNode(self.question)
        text.appendChild(_questiontext)

        if self.hasAttachment:

            file_attachment = self.xml.createElement('file')
            file_attachment.setAttribute('encoding', 'base64')
            file_attachment.setAttribute('name', self.filename)
            file_attachment.setAttribute('path', '/')
            questiontext.appendChild(file_attachment)

            import base64
            base64_file = base64.b64encode(open(self.filepath, 'rb').read())
            base64_file_string = base64_file.decode('utf8')

            file_content = self.xml.createTextNode(base64_file_string)
            file_attachment.appendChild(file_content)

            # remove generated images (code images)
            if re.search('code_[0-9]*\.[0-9]*\.png', self.filepath):
                import os
                os.remove(self.filepath)

        # <name> ... </name>
        name = self.xml.createElement('name')
        question.appendChild(name)

        text = self.xml.createElement('text')
        name.appendChild(text)

        _name = self.xml.createTextNode(self.name)
        text.appendChild(_name)

        if self.feedback:
            # <generalFeedback>
            generalfeedback = self.xml.createElement('generalfeedback')
            question.appendChild(generalfeedback)

            text = self.xml.createElement('text')
            generalfeedback.appendChild(text)
            _generalfeedback = self.xml.createTextNode(self.feedback)
            text.appendChild(_generalfeedback)

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
