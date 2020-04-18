import sys
import time

print("Repl.it Downloader - a tool for downloading all files from a repl.it classroom")

try:
    from selenium import webdriver
except:
    print("ERROR: Please install selenium using the command 'pip install selenium'")
    sys.exit()

classroom_id = input("Enter your classroom id (6 digit number): ")
num_assigments = input("Please enter the number of assignments: ")

driver = webdriver.Chrome()
driver.get(f'https://repl.it/login?goto=%2Fstudent%2Fclassrooms%2F{classroom_id}'')

print("Please login to repl.it through the popup window")

while True:
    if driver.current_url == f'https://repl.it/student/classrooms/{classroom_id}'':
        print("Successfully logged in!")
        break

print("Webpage is loading...")

loaded_status = input("Type anything here once the webpage has finished loading: ")

for i in range(1, num_assigments+1):
    element = driver.find_element_by_xpath(f'//*[@id="classroomsPage"]/div[3]/div[3]/div/div[2]/div/div[2]/div[{i}]')
    element.click()