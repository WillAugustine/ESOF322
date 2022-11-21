from urllib.request import urlopen
import json
import random
import html

class Trivia:
    # The super cool constructor for the trivia questions.
    # This will set up the trivia stuff.
    # Later, implement some parameters to allow different link generations.
    def __init__(self, cat="none", dif="none"):
        self.categories = {
            "general": 9,
            "books": 10,
            "film": 11,
            "music": 12,
            "musicals": 13,
            "television": 14,
            "videogames": 15,
            "boardgames": 16,
            "science": 17,
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
            "anime": 31,
            "cartoons": 32
        }
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
        if category in self.categories:
            thisCategory = "&category=" + str(self.categories[category])
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
        returnQuestions = theQuestions["results"][0]
        return returnQuestions

    # Get Answers
    # Output:
    #   An array of the answers, in shuffled order.
    # Description:
    #   Fetches the questions from the dictionary, and returns them in a randomized order.
    def getAnswers(self):
        answers = [self.questions["correct_answer"]]
        for i in range(len(self.questions["incorrect_answers"])):
            answers.append(html.unescape(self.questions["incorrect_answers"][i]))
        random.shuffle(answers)

        self.answerNumber = answers.index(self.questions["correct_answer"]) + 1

        return answers

    # Format Question
    # Description:
    #   Prints formatted trivia questions to the console.
    #   In the future, change this to work with the Discord bot's output stuff.
    def formatQuestion(self):
        qArray = []
        qArray.append(html.unescape(self.questions["category"]))
        qArray.append(html.unescape(self.questions["question"]))
        for i in range(len(self.answers)):
            qArray.append(str(i+1) + ": " + html.unescape(self.answers[i]))
        return qArray
    
    # Check Answer
    # Parameters:
    #   answerNum:
    #       The given number associated with the question.
    # Description:
    #   Checks if the user's given answer is correct.
    def checkAnswer(self, answerNum):
        if answerNum == self.answerNumber:
            return True
        else:
            return False
    
    # Return Answer
    # Description:
    #   Returns the string for the correct answer.
    #   Use this if someone answers the trivia question incorrectly.
    def returnAnswer(self):
        return self.questions["correct_answer"]
    
    # Show Categories
    # Description:
    #   Returns an array of strings for the valid trivia categories.
    def showCategories(self):
        returnCategories = []
        for keys in self.categories:
            returnCategories.append(keys)
        return returnCategories
    
    # GetQuestionCount
    # Description:
    #   Returns the number of questions.
    def getQuestionCount(self):
        if self.questions["type"] == "multiple":
            return 4
        else:
            return 2

if __name__ == "__main__":
    superCoolTrivia = Trivia()
    questionList = superCoolTrivia.formatQuestion()
    for i in questionList:
        print (i)
    answerInput = int(input())
    print(superCoolTrivia.checkAnswer(answerInput))
    