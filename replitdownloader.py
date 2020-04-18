import sys
import time

print("replitdownloader - a tool for downloading all files from a repl.it classroom")

try:
    from selenium import webdriver
except:
    print("ERROR: Please install selenium using the command 'pip install selenium'")
    sys.exit()

classroom_id = str(input("Enter the classroom id: "))

driver = webdriver.Chrome()
driver.get(f"https://repl.it/student/classrooms/{classroom_id}")

# email_box = driver.find_element_by_name("username")
# email_box.send_keys(email)

# time.sleep(2)

