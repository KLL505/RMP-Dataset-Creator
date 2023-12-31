"""
ratemyprofessor

RateMyProfessor API
An extremely basic web scraper for the RateMyProfessor website.

:copyright: (c) 2021 Nobelz
:license: Apache 2.0, see LICENSE for more details.
"""
import requests
import re
import json
import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from .professor import Professor
from .school import School

class RateMyProfApi:


    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "json/header.json"), 'r') as f:
            self.headers = json.load(f)

    def save_object(self, obj, filename):
        with open(filename, 'wb') as outp:  # Overwrites any existing file.
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


    def get_school_by_name(self, school_name: str):
        """
        Gets a School with the specified name.

        This only returns 1 school name, so make sure that the name is specific.
        For instance, searching "Ohio State" will return 6 schools,
        but only the first one will return by calling this method.

        :param school_name: The school's name.
        :return: The school that match the school name. If no schools are found, this will return None.
        """
        schools = self.get_schools_by_name(school_name)
        if schools:
            return schools[0]
        else:
            return None


    def get_schools_by_name(self, school_name: str):
        """
        Gets a list of Schools with the specified name.

        This only returns up to 20 schools, so make sure that the name is specific.
        For instance, searching "University" will return more than 20 schools, but only the first 20 will be returned.

        :param school_name: The school's name.
        :return: List of schools that match the school name. If no schools are found, this will return an empty list.
        """
        school_name.replace(' ', '+')
        url = "https://www.ratemyprofessors.com/search/schools?q=%s" % school_name
        page = requests.get(url)
        data = re.findall(r'"legacyId":(\d+)', page.text)
        school_list = []

        for school_data in data:
            try:
                school_list.append(School(int(school_data)))
            except ValueError:
                pass
        
        return school_list


    def get_professor_by_school_and_name(self, college: School, professor_name: str):
        """
        Gets a Professor with the specified School and professor name.

        This only returns 1 professor, so make sure that the name is specific.
        This returns the professor with the most ratings.
        For instance, searching "Smith" using the School of Case Western Reserve University will return 5 results,
        but only one result will be returned.

        :param college: The professor's school.
        :param professor_name: The professor's name.
        :return: The professor that matches the school and name. If no professors are found, this will return None.
        """
        professors = self.get_professors_by_school_and_name(college, professor_name)
        max_professor = None

        for prof in professors:
            if max_professor is None or max_professor.num_ratings < prof.num_ratings:
                max_professor = prof

        return max_professor


    def get_professors_by_school_and_name(self, college: School, professor_name: str):
        """
        Gets a list of professors with the specified School and professor name.

        This only returns up to 20 professors, so make sure that the name is specific.
        For instance, searching "Smith" with a school might return more than 20 professors,
        but only the first 20 will be returned.

        :param college: The professor's school.
        :param professor_name: The professor's name.
        :return: List of professors that match the school and name. If no professors are found,
                this will return an empty list.
        """
        # professor_name.replace(' ', '+')

        # use selenium to expand page till all profesor visable then scrap all professor ids from the hrefs on 
        # each teacher card of class "TeacherCard__StyledTeacherCard-syjs0d-0" to get list of Ids to scrape professor data

        professor_list = []
        if professor_name == "":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_extension(".\\API\\uBlock.crx")
            driver = webdriver.Chrome()
            url = 'https://www.ratemyprofessors.com/search/professors/%s?q=*' % (college.id)
            driver.get(url)

            def show_more_button_exists():
                try:
                    return driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[4]/button').is_displayed()
                except:
                    return False
                
            def close_ad_button_exists():
                try:
                    return driver.find_element(By.XPATH, '//*[@id="bx-close-inside-1177612"]').is_displayed()
                except:
                    return False
                
                
                
            cookies_button = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/button")
            cookies_button.click()

            while show_more_button_exists() or close_ad_button_exists():
                if(show_more_button_exists()):
                    show_more_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Show More')]")
                    show_more_button.click()
                if(close_ad_button_exists()):
                    close_ad_button = driver.find_element(By.XPATH, '//*[@id="bx-close-inside-1177612"]')
                    close_ad_button.click()
                time.sleep(1)

            teacher_cards = driver.find_elements(By.CLASS_NAME, "TeacherCard__StyledTeacherCard-syjs0d-0")
            print("professors found: ", len(teacher_cards))
            data = []
            for card in teacher_cards:
                href = card.get_attribute('href')
                professor_id = href.replace("https://www.ratemyprofessors.com/professor/", "")
                data.append(professor_id)
            
            driver.quit()
            fileName = 'Professors_%s.pk1' % (college.id)


        else:
            url = 'https://www.ratemyprofessors.com/search/professors/%s?q=%s' % (college.id, professor_name)
            page = requests.get(url)
            data = re.findall(r'"legacyId":(\d+)', page.text)

        for professor_data in data:
            try:
                professor_list.append(Professor(int(professor_data)))
            except ValueError:
                pass

        if professor_name == "":
            self.save_object(professor_list, fileName)
        return professor_list
