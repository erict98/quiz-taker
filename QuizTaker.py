from selenium import webdriver
import time


if __name__ == '__main__':
    def search(element, correct, incorrect):
        question_num = 0
        for item in element:
            # Retrieves information for the question
            question = item.find_element_by_xpath('.//div[@class="text"]').find_element_by_xpath('.//div[@class="answers"]')

            # Stores all the answers in a list
            answers_text = question.text.split("\n")[1:]

            # Stores all the answers in a list as accessible web data
            answers_choices = question.find_elements_by_xpath('.//div[@class="answer"]')

            # Iterates through all possible choices for a particular question
            answers_num = 0
            for option in answers_choices:
                input = option.find_element_by_xpath('.//label[@class="answer_row"]').find_element_by_xpath('.//span[@class="answer_input"]')

                try:
                    input.find_element_by_css_selector("input[type='checkbox']")
                    break
                finally:
                    pass
                if (correct[question_num]) and (correct[question_num] == answers_text[answers_num]):
                    input.find_element_by_css_selector("input[type='radio']").click()
                    break
                elif answers_text[answers_num] not in incorrect[question_num]:
                    input.find_element_by_css_selector("input[type='radio']").click()
                    break
                answers_num += 1
            question_num += 1
        # Automatically submits assignment
        driver.find_element_by_xpath('.//button[@id="submit_quiz_button"]').click()

    def check(element, correct, incorrect):
        question_num = 0
        for item in element:
            # Checks if the answer was incorrect
            wrong = True
            if len(item.find_elements_by_xpath('.//div[contains(@class, "incorrect")]')) == 0:
                wrong = False

            # Retrieves information for the question
            question = item.find_element_by_xpath('.//div[@class="text"]').find_element_by_xpath('.//div[@class="answers"]')

            # Stores all the answers in a list
            answers_text = question.text.lstrip().split("\n  ")

            # Stores all the answers in a list as accessible web data
            answers_choices = question.find_element_by_xpath('.//div[@class="answers_wrapper"]').find_elements_by_xpath('.//div[contains(@id,"answer")]')

            # Iterates through all the answers of the given question and only explores if that answer was marked
            answers_num = 0
            for answer in answers_choices:
                input = answer.find_element_by_xpath('.//div[@class="select_answer answer_type"]').find_element_by_xpath('.//input[@class="question_input"]')

                if input.get_attribute("checked") == 'true':
                    if wrong:
                        incorrect[question_num].append(answers_text[answers_num])
                    else:
                        correct[question_num] = answers_text[answers_num]
                answers_num += 1
            question_num += 1
        return correct, incorrect

    driver = webdriver.Firefox()
    url = input('Enter url: ')
    driver.get(url)

    input('Enter any key to start the script')
    element = driver.find_elements_by_xpath('.//div[@class="quiz_sortable question_holder "]')
    correct = [None] * len(element)
    incorrect = [[] for _ in range(len(element))]

    correct_answers = 0
    while correct_answers != len(correct):
        try:
            driver.find_element_by_xpath('.//a[@id="take_quiz_link"]').click()
        finally:
            pass
        try:
            time.sleep(1)  # Depends on the loading speed of the page
            element = driver.find_elements_by_xpath('.//div[@class="quiz_sortable question_holder "]')
            search(element, correct, incorrect)
        finally:
            pass

        time.sleep(1)
        element = driver.find_elements_by_xpath('.//div[@class="quiz_sortable question_holder "]')
        correct_answers = len(correct) - correct.count(None)
