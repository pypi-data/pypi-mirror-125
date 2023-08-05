# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from ..base.pageobject_  import BasePageObject, WebDriverWait, EC
import pinyin
# from configini_crw import *
from cinirw.cinirw_ import *
import os
from ...director.misc_ import secit

class VisitFlowObject(BasePageObject):

    __visit_loc = (By.ID, "sb_form_q")
    __btn_loc = (By.ID, "sb_form_go")

    __visit_loc_pass_ = (By.ID, "inputPassword")
    __visit_loc_email_ = (By.ID, "inputEmail")
    __btn_loc_css_ = (By.CSS_SELECTOR, "body > div > div > div > section > div > form > div.control-group.margin-b > div > button")


    map_input_localvalueID = (By.ID, 'localvalue')
    map_click_localsearchID = (By.ID, 'localsearch')
    map_click_selectorCSS = (By.CSS_SELECTOR, '#no_0')
    map_get_selectorXPATH = (By.XPATH, '//*[@id="no_0"]/p')
    map_get_cityID = (By.ID, 'curCity')


    def fetch_text_(self, visittype):
        fetched_ = self.locate_element(*visittype)
        return fetched_

    def scan_g_class_(self, visittype):
        ''' Locate Scan G '''
        g_class_ = self.locate_element(*visittype)
        g_class_x_loc_ = (By.CSS_SELECTOR, 'text')
        x = g_class_.find_elements_by_css_selector('text')
        print()
        if (len(x) > 0):
            for y in x:
                print(y.text)
                print(y.get_attribute('x'))
                #print(dir(y))

    def select_ui_class_(self, visittype, Internet):
        ''' Locate Select UI LI '''
        ui_class_ = self.locate_element(*visittype)
        t = ui_class_.find_elements_by_xpath('li')
        if (len(t) > 0):
            for u in t:
                # print(u.get_attribute('data-value'))
                if (Internet == u.get_attribute('data-value')):
                    u.click()
                    break

    def scan_ui_class_(self, visittype):
        ''' Locate Scan UI LI '''
        ui_class_ = self.locate_element(*visittype)
        t = ui_class_.find_elements_by_xpath('li')
        if (len(t) > 0):
            for u in t: # print(u.get_attribute('class'))
                print(u.get_attribute('data-value'))

    def btn_dclick_visittype_(self, visittype):
        ''' Locate Button '''
        FlowBtn = self.locate_element(*visittype)
        FlowBtn.click()
        FlowBtn.click()

    def btn_click_visittype_(self, visittype):
        ''' Locate Button '''
        FlowBtn = self.locate_element(*visittype)
        FlowBtn.click()

    def flow_content_visittype_(self, content, visittype):
        FlowContent = self.locate_element(*visittype)
        FlowContent.send_keys(content)

    def flow_content(self, content):
        ''' Locate Input '''
        FlowContent = self.locate_element(*self.__visit_loc)
        FlowContent.send_keys(content)

    def btn_click(self):
        ''' Locate Button '''
        FlowBtn = self.locate_element(*self.__btn_loc_css_)
        FlowBtn.click()

    def flow_content_pass_(self, content):
        ''' Locate Input '''
        FlowContent = self.locate_element(*self.__visit_loc_pass_)
        FlowContent.send_keys(content)

    def flow_content_email_(self, content):
        ''' Locate Input '''
        FlowContent = self.locate_element(*self.__visit_loc_email_)
        FlowContent.send_keys(content)



def visitVersa_():
    Versa = VisitFlowObject()
    Versa.visit("https://172.17.21.1/versa/login/")
    # BSearch.flow_content_pass_("Linshi@123")
    # BSearch.flow_content_email_("Linshi")
    visit_loc_pass_ = (By.ID, "inputPassword")
    visit_loc_email_ = (By.ID, "inputEmail")
    Versa.flow_content_visittype_("Linshi@123", visit_loc_pass_)
    Versa.flow_content_visittype_("Linshi", visit_loc_email_)
    Versa.btn_click()
    Versa.quit()


def visitBing_():
    Bing = VisitFlowObject()
    Bing.visit("https://cn.bing.com/")
    # BSearch.flow_content("tsunx")
    # BSearch.btn_click()
    visit_loc = (By.ID, "sb_form_q")
    btn_loc = (By.ID, "sb_form_go")
    Bing.flow_content_visittype_("Python Selenium", visit_loc)
    Bing.btn_click_visittype_(btn_loc)
    Bing.quit()


def visitLinkAvailability_(tenant):
    Versa = VisitFlowObject()
    Versa.visit("https://211.152.44.186/versa/login")
    visit_loc_pass_ = (By.ID, "inputPassword")
    visit_loc_email_ = (By.ID, "inputEmail")
    Versa.flow_content_visittype_("Versa#21viacloud", visit_loc_pass_)
    Versa.flow_content_visittype_("Administrator", visit_loc_email_)
    Versa.btn_click()

    # visit Analytics
    # //*[@id="menuContainer"]/li[6]/a
    visit_loc_analytics_ = (By.XPATH, r'//*[@id="menuContainer"]/li[6]/a')
    Versa.btn_click_visittype_(visit_loc_analytics_)

    # visit Sites
    # #left-nav-analytics-sd-wan > li:nth-child(1) > a > span
    visit_loc_sites_ = (By.CSS_SELECTOR, '#left-nav-analytics-sd-wan > li:nth-child(1) > a > span')
    Versa.btn_click_visittype_(visit_loc_sites_)

    # visit Link Availability
    # //*[@id="2"]/a
    visit_loc_LA_ = (By.XPATH, '//*[@id="2"]/a')
    Versa.btn_dclick_visittype_(visit_loc_LA_)

    # visit Tenant
    # //*[@id="1"]/div/div/span
    # visit_loc_Tn_ = (By.XPATH, '//*[@id="1"]/div/div/span')
    # Versa.btn_click_visittype_(visit_loc_Tn_)
    # Select(driver.find_element_by_id('vlanData_0-0_networkName')).select_by_visible_text('Internet')
    # //*[@id="1"]/div/div/ul
    # #\31  > div > div > span
    # //*[@id="1"]/div/div/span

    # search by tenant
    visit_loc_searchbytenant_ = (By.XPATH, '//*[@id="1"]/div/div/span')
    Versa.btn_click_visittype_(visit_loc_searchbytenant_)
    visit_loc_tenants_ = (By.CSS_SELECTOR, '.typeahead.typeahead-long.dropdown-menu')
    ## Versa.scan_ui_class_(visit_loc_tenants_)
    #Versa.select_ui_class_(visit_loc_tenants_, "Customer-YiMeng")
    #Versa.select_ui_class_(visit_loc_tenants_, "Customer-JinQiaoZhen")
    Versa.select_ui_class_(visit_loc_tenants_, tenant)

    # tenant LA detail
    visit_loc_LA_devices_ = (By.CSS_SELECTOR, 'g.highcharts-axis-labels.highcharts-xaxis-labels')
    print("-- The Result -- \n")
    Versa.scan_g_class_(visit_loc_LA_devices_)
    # #highcharts-4w1hxf8-1540 > svg > g.highcharts-axis-labels.highcharts-xaxis-labels > text:nth-child(2)
    Versa.quit()

@secit()
def visitAPIMAP(cmaddress):
    Map = VisitFlowObject()
    Map.visit("http://api.map.baidu.com/lbsapi/getpoint/index.html")
    Map.flow_content_visittype_(cmaddress, VisitFlowObject.map_input_localvalueID)
    Map.btn_click_visittype_(VisitFlowObject.map_click_localsearchID)
    Map.btn_click_visittype_(VisitFlowObject.map_click_selectorCSS)
    points2 = Map.fetch_text_(VisitFlowObject.map_get_selectorXPATH)
    # print(points2.text.split("\n"))
    if (2 == len(points2.text.split("\n"))):
        device_address, device_location = points2.text.split("\n")
    else:
        device_address, device_phone, device_location = points2.text.split("\n")
    # device_location_str, device_locations = device_location.split(('：').decode("utf8","ignore"))
    device_location_str, device_locations = device_location.split(u"：")
    longitude, latitude = device_locations.split(",")
    print("latitude: ", latitude)
    print("longitude: ", longitude)
    #
    # fetched cmaddress
    device_addresses_str, device_addresses = device_address.split(u"：")
    print(device_addresses_str)
    print(device_addresses)
    currentAddrPinyin = ""
    for item in device_addresses:
        currentAddrPinyin += pinyin.get(item, format = 'strip')[:].capitalize()
        # print(item)
        # subCurrentAddrPinyin = pinyin.get(item, format = 'strip')[:].capitalize()
        # currentAddrPinyin += subCurrentAddrPinyin
    print(currentAddrPinyin)
    #
    # fetch city
    # currentCity = driver.find_element_by_id('curCity')
    currentCity = Map.fetch_text_(VisitFlowObject.map_get_cityID)
    currentCityText = str(currentCity.text)
    currentCityPinyin = pinyin.get(currentCityText, format = 'strip')[:-3].capitalize()
    print(currentCity.text)
    print(currentCityPinyin)
    # save the fetched
    ROOT = '..\\Devices'
    # pathd_put = ".\\" + ROOT + "\\" + "config_devices_pst_" + device_address + ".ini"
    pathd_put = '.{}{}{}config_branch_locinfo_{}_.ini'.format(os.sep, ROOT, os.sep, device_address)
    print(pathd_put)
    UpdateConfigIni = WriteConfigIni(pathd_put)
    UpdateConfigIni.addConfigSection("LocationInformation")
    UpdateConfigIni.putConfigValue("LocationInformation", "ChineseMadrineAddress", device_address)
    UpdateConfigIni.putConfigValue("LocationInformation", "Address1", str(currentAddrPinyin))
    # 2020.1.13 xpinyin
    UpdateConfigIni.putConfigValue("LocationInformation", "city", str(currentCityPinyin))
    UpdateConfigIni.putConfigValue("LocationInformation", "country", "CHINA")
    UpdateConfigIni.putConfigValue("LocationInformation", "Latitude", latitude)
    UpdateConfigIni.putConfigValue("LocationInformation", "Longitude", longitude)
    #
    Map.quit()









            




