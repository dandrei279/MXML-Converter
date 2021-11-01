import argparse
from hr import HR
from question import Question
from xml.dom import minidom

if __name__ == "__main__":
    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='input', help='input file')
    parser.add_argument('-o', '--output', type=str, dest='output', help='output file', default='questions.xml')
    parser.add_argument('-f', '--format', type=str, default='hr', dest='file_format', choices=['hr'])

    # Parse and print the results
    args = parser.parse_args()

    # create a HR converter
    if args.file_format == 'hr':
        parser = HR()

    file = open(args.input, 'r')

    hr_questions = []
    hr_question = ""
    for line in file:
        hr_question += line
        if line == "\n":
            hr_questions.append(hr_question)
            hr_question = ""

    # add last question
    hr_questions.append(hr_question)
    
    xml = minidom.Document()
    quiz = xml.createElement('quiz')
    xml.appendChild(quiz)

    for hr_question in hr_questions:
        parser.load_question(hr_question, xml, quiz)

    output_file = open(args.output, 'w')

    output_file.write(xml.toprettyxml(indent="\t"))