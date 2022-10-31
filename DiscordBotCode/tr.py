from urllib.request import urlopen
import json
import random


class Trivia:
    # The super cool constructor for the trivia questions.
    # This will set up the trivia stuff.
    # Later, implement some parameters to allow different link generations.
    def __init__(self):
        self.questions = self.loadQuestions()
        self.answers = self.getAnswers()
        self.correctAnswer = self.questions["correct_answer"]

    # Generate Link
    # Parameters:
    #   category:
    #       The category for the trivia question (string)
    #   difficulty:
    #       The difficulty level for the trivia question (string)
    # Description:
    #   Generates a link for opentb's trivia API.
    def generateLink(self, category, difficulty):
        pass

    # Load Questions
    # Parameters:
    #   link:
    #       A link generated from generateLink (if one is provided).
    # Output:
    #   A dictionary containing the question data.
    # Description:
    #   Uses the Trivia API to fetch a question, and converts it to a dictionary.
    def loadQuestions(self):
        url = "https://opentdb.com/api.php?amount=1"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        theQuestions = json.loads(html)
        return theQuestions["results"][0]

    # Get Answers
    # Output:
    #   An array of the answers, in shuffled order.
    # Description:
    #   Fetches the questions from the dictionary, and returns them in a randomized order.
    def getAnswers(self):
        answers = [self.questions["correct_answer"]]
        for i in range(len(self.questions["incorrect_answers"])):
            answers.append(self.questions["incorrect_answers"][i])
        random.shuffle(answers)

        self.answerNumber = answers.index(self.questions["correct_answer"]) + 1

        return answers

    # Format Question
    # Description:
    #   Prints formatted trivia questions to the console.
    #   In the future, change this to work with the Discord bot's output stuff.
    def formatQuestion(self):
        print(self.questions["category"])
        print(self.questions["question"])
        for i in range(len(self.answers)):
            print(str(i+1) + ": " + self.answers[i])
    
    # Check Answer
    # Parameters:
    #   answerNum:
    #       The given number associated with the question.
    # Description:
    #   Checks if the user's given answer is correct.
    def checkAnswer(self, answerNum):
        if answerNum == self.answerNumber:
            print("You're winner!")
        else:
            print("Incorrect. The right answer was " + self.questions["correct_answer"])

if __name__ == "__main__":
    superCoolTrivia = Trivia()
    superCoolTrivia.formatQuestion()
    answerInput = int(input())
    superCoolTrivia.checkAnswer(answerInput)
