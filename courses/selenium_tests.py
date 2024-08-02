# selenium_tests.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def test_course_creation():
    driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
    driver.get("http://localhost:8000/admin/")
    
    username_field = driver.find_element_by_name("username")
    password_field = driver.find_element_by_name("password")
    username_field.send_keys("admin")
    password_field.send_keys("password")
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(1)  # Wait for the page to load
    
    # Assuming there's an admin interface to add a course
    driver.get("http://localhost:8000/admin/courses/course/add/")
    
    name_field = driver.find_element_by_name("name")
    description_field = driver.find_element_by_name("description")
    name_field.send_keys("Selenium Course")
    description_field.send_keys("Selenium Description")
    description_field.send_keys(Keys.RETURN)
    
    time.sleep(1)  # Wait for the page to load
    
    # Verify the course was added
    driver.get("http://localhost:8000/admin/courses/course/")
    assert "Selenium Course" in driver.page_source
    
    driver.quit()

if __name__ == "__main__":
    test_course_creation()
