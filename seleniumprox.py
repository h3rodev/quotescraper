from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import re
from selenium.webdriver.common.proxy import *


class Testrobot2(unittest.TestCase):
    def setUp(self):

        myProxy = "http://149.215.113.110:70"

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            'ftpProxy': myProxy,
            'sslProxy': myProxy,
            'noProxy': ''})

        self.driver = webdriver.Firefox(proxy=proxy)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.ie/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_robot2(self):
        driver = self.driver
        driver.get(self.base_url + "/#gs_rn=17&gs_ri=psy-ab&suggest=p&cp=6&gs_id=ix&xhr=t&q=selenium&es_nrs=true&pf=p&output=search&sclient=psy-ab&oq=seleni&gs_l=&pbx=1&bav=on.2,or.r_qf.&bvm=bv.47883778,d.ZGU&fp=7c0d9024de9ac6ab&biw=592&bih=665")
        driver.find_element_by_id("gbqfq").clear()
        driver.find_element_by_id("gbqfq").send_keys("selenium")

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
