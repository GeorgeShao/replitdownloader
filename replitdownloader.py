import sys
import time

print("Repl.it Downloader - a tool for downloading all files from a repl.it classroom")

try:
    from selenium import webdriver
except:
    print("ERROR: Please install selenium using the command 'pip install selenium'")
    sys.exit()

classroom_id = input("Enter your classroom id (6 digit number): ")
num_assigments = int(input("Please enter the number of assignments: "))

driver = webdriver.Chrome()
driver.get(f'https://repl.it/login?goto=%2Fstudent%2Fclassrooms%2F{classroom_id}')

print("Please login to repl.it through the popup window")

while True:
    if driver.current_url == f'https://repl.it/student/classrooms/{classroom_id}':
        print("Successfully logged in!")
        break

print("Webpage is loading...")

loaded_status = input(f'Press enter once the webpage has finished loading (Assignment #1):')

for i in range(1, num_assigments+1):
    assignment_element = driver.find_element_by_xpath(f'//*[@id="classroomsPage"]/div[3]/div[3]/div/div[2]/div/div[2]/div[{i}]')
    assignment_element.click()
    loaded_status = input(f'Press enter once the webpage has finished loading (Assignment #{i}): ')
    text_element = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[2]/section[1]/div/section[1]/div[3]/div/div[1]/div[2]')
    text = text_element.text
    print(text)
    driver.get(f'https://repl.it/login?goto=%2Fstudent%2Fclassrooms%2F{classroom_id}')
    loaded_status = input(f'Press enter once the webpage has finished loading (Assignment #{i+1}): ')