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

# download_mode = "N/A"
# website_load_delay = 10

# while True
#     download_mode = input("Enter your download mode (\"MANUAL\" or \"AUTOMATIC\") ")
#     print("Manual mode is better for unstable or slow wifi.")
#     print("Automatic mode is better for stable and consistent wifi.")
#     if download_mode == "AUTOMATIC":
#         website_load_delay == int(input("How long would you like the website load delay to be (in seconds)? (default=10): "))

driver = webdriver.Chrome()
driver.get(f'https://repl.it/login?goto=%2Fstudent%2Fclassrooms%2F{classroom_id}')

print("Please login to repl.it through the popup window")

while True:
    if driver.current_url == f'https://repl.it/student/classrooms/{classroom_id}':
        print("Successfully logged in!")
        break

print("Mainpage is loading...")

loaded_status = input(f'Press ENTER once the webpage has finished loading (the mainpage): ')

def open_assignment(i: int):
    try:
        assignment_element = driver.find_element_by_xpath(f'//*[@id="classroomsPage"]/div[3]/div[3]/div/div[2]/div/div[2]/div[{i}]')
        assignment_element.click()
        print(f'Opened assignment #{i}')
    except:
        time.sleep(1)
        open_assignment()

def get_text(i: int):
    try:
        text_element = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[2]/section[1]/div/section[1]/div[3]/div/div[1]/div[2]')
        text = text_element.text
        print(f'Got text #{i}')
    except:
        time.sleep(1)
        get_text()

for i in range(1, num_assigments+1):
    open_assignment(i)
    get_text(i)
    driver.get(f'https://repl.it/login?goto=%2Fstudent%2Fclassrooms%2F{classroom_id}')