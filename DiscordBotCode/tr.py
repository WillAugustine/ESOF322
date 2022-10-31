from urllib.request import urlopen
import json
import random

categories = {
    "general": 9,
    "books": 10,
    "film": 11,
    "music": 12,
    "musicals and theatres": 13,
    "television": 14,
    "video games": 15,
    "board games": 16,
    "science and nature": 17,
    "computers": 18,
    "mathematics": 19,
    "mythology": 20,
    "sports": 21,
    "geograpy": 22,
    "history": 23,
    "politics": 24,
    "art": 25,
    "celebrities": 26,
    "animals": 27,
    "vehicles": 28,
    "comics": 29,
    "gadgets": 30,
    "anime and manga": 31,
    "cartoons and animations": 32
}

class Trivia:
    # The super cool constructor for the trivia questions.
    # This will set up the trivia stuff.
    # Later, implement some parameters to allow different link generations.
    def __init__(self, cat="none", dif="none"):
        self.url = self.generateLink(cat, dif)
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
        if category in categories:
            thisCategory = "&category=" + str(categories[category])
        else:
            thisCategory = ""
        if difficulty != "none":
            thisDifficulty = "&difficulty=" + difficulty
        else:
            thisDifficulty = ""
        genLink = "https://opentdb.com/api.php?amount=1" + thisCategory + thisDifficulty
        print (genLink)
        return genLink

    # Load Questions
    # Parameters:
    #   link:
    #       A link generated from generateLink (if one is provided).
    # Output:
    #   A dictionary containing the question data.
    # Description:
    #   Uses the Trivia API to fetch a question, and converts it to a dictionary.
    def loadQuestions(self):
        url = self.url
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
    superCoolTrivia = Trivia("anime and manga", "easy")
    superCoolTrivia.formatQuestion()
    answerInput = int(input())
    superCoolTrivia.checkAnswer(answerInput)