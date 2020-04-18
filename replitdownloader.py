import sys
import time

print("Repl.it Downloader - a tool for downloading all files from a repl.it classroom")

try:
    from selenium import webdriver
except:
    print("ERROR: Please install selenium using the command 'pip install selenium'")
    sys.exit()

classroom_id = str(input("Enter the classroom id: "))

driver = webdriver.Chrome()
driver.get(f"https://repl.it/login?goto=%2Fstudent%2Fclassrooms%2F{classroom_id}")

# email_box = driver.find_element_by_name("username")
# email_box.send_keys(email)

# time.sleep(2)

print("Please login to repl.it through the popup window")

logged_in = False

while True:
    if driver.current_url == "https://repl.it/student/classrooms/177470" and not logged_in:
        print("Successfully logged in!")