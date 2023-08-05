
import time
from bs4 import BeautifulSoup
import xlsxwriter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ipra.Model.Robot.baseRobot import BaseRobot
import threading

class ManulifeRobot(BaseRobot):
    def __init__(self, policyList, frame, reportPath, inputPath):
        super().__init__(policyList, frame, reportPath, inputPath)
        self.logger.writeLogString('MANU-INIT','ROBOT INIT')
        self.maxPolicyListSize = len(policyList)
        self.workbook = xlsxwriter.Workbook(self.reportPath+'MANULIFE_report.xlsx')
        
        self.basicInfo_sheet = self.workbook.add_worksheet(name="General Information")
        self.basicInfo_sheet.write(0, 0, "Policy No.")

        self.logger.writeLogString('MANU-INIT','maxPolicyListSize:'+str(self.maxPolicyListSize))
        
        
    def waitingLoginComplete(self):
        self.logger.writeLogString('MANU-LOGIN','START LOGIN')
        self.browser.get("https://www.manutouch.com.hk/wps/portal/login?agent_type=BROKER")
        
        #wait until below show
        while not self.isLogin and not self.isStopped:
            try:
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[4]/div/ul[1]/li[2]/a/span")))
                self.isLogin=True  
            except:
                time.sleep(3)
        else:
            pass

        #open a dropdown menu
        self.browser.find_element_by_xpath("/html/body/div[1]/div[3]/div[4]/div/ul[1]/li[2]/a/span").click()
        
        #click to enter search page
        self.browser.find_element_by_xpath("/html/body/div[1]/div[3]/div[4]/div/ul[1]/li[2]/div/div/div[1]/h3[1]/a/span").click()


        if self.isLogin:
            self.frame.setStatusLableText("Logged in")
            self.logger.writeLogString('MANU-LOGIN','LOGIN COMPLETED')
    
    def scrapPolicy(self):
        #there is a frame wrapped the input field
        self.browser.switch_to.frame(0)
        for policy in self.policyList:
            if self.isStopped:
                return
            
            try:
                self.frame.setStatusLableText("Processing "+str(policy))
                self.logger.writeLogString('MANU','PROCESSING:'+str(policy))
                
                
                input = self.browser.find_element_by_xpath("/html/body/table/tbody/tr/td/div/form/div[2]/div/table/tbody/tr/td/div[4]/table[1]/tbody/tr/td/table[3]/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[4]/input")
                input.clear()
                input.send_keys(str(policy))
                
                self.browser.find_element_by_xpath("/html/body/table/tbody/tr/td/div/form/div[2]/div/table/tbody/tr/td/div[4]/table[1]/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/a[1]/img").click()
                self.browser.find_element_by_link_text(str(policy)).click()
                
                time.sleep(5)
                
                self.browser.switch_to.window(self.browser.window_handles[1])
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(str(self.reportPath+policy)+"_basic"+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()
                
                

                
            except:
                self.logger.writeLogString('MANU',str(policy)+" NOT FOUND")
                self.frame.setStatusLableText(policy+" is not found")
            finally:
                self.frame.setStatusLableText(policy+" completed")
                self.logger.writeLogString('MANU',str(policy)+" COPMLETED")
                self.frame.setStatusProgresValueByValue(1)
                self.browser.switch_to.window(self.browser.window_handles[0])
                self.browser.switch_to.default_content()
                self.buildReportQueue.append(policy)
                self.buildHeaderQueue.append(policy)
        pass


    def buildReport(self):
        self.buildReportThread = threading.Thread(target = self.__buildReport)
        self.buildReportThread.start()
        self.buildReportHeaderFullFlow()
        pass

    def buildReportOnly(self):
        self.buildReportThread = threading.Thread(target = self.__buildReportOnly)
        self.buildReportThread.start()
        self.buildReportHeaderHalfFlow()
        pass

    def buildReportHeaderFullFlow(self):
        self.buildHeaderThread = threading.Thread(target = self.__buildReportHeaderFullFlow)
        self.buildHeaderThread.start()
        pass
    
    def buildReportHeaderHalfFlow(self):
        self.buildHeaderThread = threading.Thread(target = self.__buildReportHeaderHalfFlow)
        self.buildHeaderThread.start()
        pass


    def __buildReportHeaderFullFlow(self):
        self.logger.writeLogString('MANU-HEADER','START BUILD HEADER FULLFLOW')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildHeaderQueue:
                self.logger.writeLogString('MANU-HEADER','POLICY NO.:{0}'.format(str(policy)))
                if self.isStopped:
                    return
                try:

                    self.__formatBasicInfoHeader(policy,self.basicInfo_sheet,self.reportPath)
                    #self.__formatScopeInfoHeader(policy,self.scope_sheet,self.reportPath)
                    #self.__formatValueHeader(policy,self.value_sheet,self.reportPath)
                    #self.__formatPaymentHeader(policy,self.value_payment,self.reportPath)
                        
                    #No error when building the header,break all loop and then stop this thread
                    policy_iteration = self.maxPolicyListSize + 1
                    self.logger.writeLogString('MANU-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                    break
                except FileNotFoundError:
                    self.logger.writeLogString('MANU-HEADER','FILE NOT FOUND')
                except Exception as ex:
                    self.logger.writeLogString('MANU-HEADER','EXCEPTION:'+str(ex))
                finally:
                    policy_iteration = policy_iteration + 1
                    if policy in self.buildHeaderQueue:
                        self.buildHeaderQueue.remove(policy)

    def __buildReportHeaderHalfFlow(self):
        self.logger.writeLogString('MANU-HEADER','START BUILD HEADER HALFFLOW')
        for policy in self.policyList:
            self.logger.writeLogString('MANU-HEADER','POLICY NO.:{0}'.format(str(policy)))
            if self.isStopped:
                return
            try:

                self.__formatBasicInfoHeader(policy,self.basicInfo_sheet,self.inputPath)
                #self.__formatScopeInfoHeader(policy,self.scope_sheet,self.inputPath)
                #self.__formatValueHeader(policy,self.value_sheet,self.inputPath)
                #self.__formatPaymentHeader(policy,self.value_payment,self.inputPath)
                    
                #No error when building the header,break all loop and then stop this thread
                self.logger.writeLogString('MANU-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                break
            except FileNotFoundError as ex:
                self.logger.writeLogString('MANU-HEADER','FILE NOT FOUND')
            except Exception as ex:
                self.logger.writeLogString('MANU-HEADER','EXCEPTION:'+str(ex))

    def __buildReport(self):
        self.logger.writeLogString('MANU-CONTENT','START BUILD REPORT')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildReportQueue:
                if self.isStopped:
                    return
                self.frame.setStatusLableText("Build Report "+str(policy))
                self.logger.writeLogString('MANU-CONTENT','POLICY NO.:{0}'.format(str(policy)))
                try:
                    pass
                    self.basicInfo_sheet.write(policy_iteration+1,0,str(policy))
                    #self.scope_sheet.write(policy_iteration+1,0,str(policy))
                    #self.value_sheet.write(policy_iteration+1,0,str(policy))
                    #self.value_payment.write(policy_iteration+1,0,str(policy))

                    thread_basicInfo = threading.Thread(target = self.__formatBasicInfo, args=[policy_iteration,policy,self.basicInfo_sheet,self.reportPath])
                    thread_basicInfo.start()

                    #thread_scopeInfo = threading.Thread(target = self.__formatScopeInfo, args=[policy_iteration,policy,self.scope_sheet,self.reportPath])
                    #thread_scopeInfo.start()

                    #thread_value = threading.Thread(target = self.__formatValue, args=[policy_iteration,policy,self.value_sheet,self.reportPath])
                    #thread_value.start()

                    #thread_payment = threading.Thread(target = self.__formatPayment, args=[policy_iteration,policy,self.value_payment,self.reportPath])
                    #thread_payment.start()

                except FileNotFoundError:
                    self.basicInfo_sheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                    self.frame.setStatusLableText("Build Report "+str(policy)+ " Not Found")
                    self.logger.writeLogString('MANU-CONTENT','FILE NOT FOUND')
                except Exception as ex:
                    self.basicInfo_sheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!"+str(ex))
                    self.frame.setStatusLableText("Build Report "+str(policy)+ " Failed")
                    self.logger.writeLogString('MANU-CONTENT','EXCEPTION:'+str(ex))
                finally:
                    thread_basicInfo.join()
                    #thread_scopeInfo.join()
                    #thread_value.join()
                    #thread_payment.join()
                    self.frame.setStatusProgresValueByValue(1)
                    policy_iteration = policy_iteration + 1
                    self.buildReportQueue.remove(policy)

        self.workbook.close()
        self.frame.setStatusLableText("Completed")
        self.logger.writeLogString('MANU-CONTENT','COPMLETED BUILD REPORT')

    def __buildReportOnly(self):
        self.logger.writeLogString('MANU-CONTENT','START BUILD REPORT OFFLINE MODE')
        for policy_iteration,policy in enumerate(self.policyList):
            if self.isStopped:
                return
            self.frame.setStatusLableText("Build Report "+str(policy))
            self.logger.writeLogString('MANU-CONTENT','POLICY NO.:{0}'.format(str(policy)))
            try:
                pass
                self.basicInfo_sheet.write(policy_iteration+1,0,str(policy))
                #self.scope_sheet.write(policy_iteration+1,0,str(policy))
                #self.value_sheet.write(policy_iteration+1,0,str(policy))
                #self.value_payment.write(policy_iteration+1,0,str(policy))
                
                #thread_basicInfo = threading.Thread(target = self.__formatBasicInfo, args=[policy_iteration,policy,self.basicInfo_sheet,self.inputPath])
                #thread_basicInfo.start()
                
                #thread_scopeInfo = threading.Thread(target = self.__formatScopeInfo, args=[policy_iteration,policy,self.scope_sheet,self.inputPath])
                #thread_scopeInfo.start()
                
                #thread_value = threading.Thread(target = self.__formatValue, args=[policy_iteration,policy,self.value_sheet,self.inputPath])
                #thread_value.start()
                
                #thread_payment = threading.Thread(target = self.__formatPayment, args=[policy_iteration,policy,self.value_payment,self.inputPath])
                #thread_payment.start()

            except FileNotFoundError:
                self.basicInfo_sheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                self.frame.setStatusLableText("Build Report "+str(policy)+ " Not Found")
                self.logger.writeLogString('MANU-CONTENT','FILE NOT FOUND')
            except Exception as ex:
                self.basicInfo_sheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!"+str(ex))
                self.frame.setStatusLableText("Build Report "+str(policy)+ " Failed")
                self.logger.writeLogString('MANU-CONTENT','EXCEPTION:'+str(ex))
            finally:
                #thread_basicInfo.join()
                #thread_scopeInfo.join()
                #thread_value.join()
                #thread_payment.join()
                self.frame.setStatusProgresValueByValue(2)

        self.workbook.close()
        self.frame.setStatusLableText("Completed")
        self.logger.writeLogString('MANU-CONTENT','COPMLETED BUILD REPORT OFFLINE MODE')

    def __formatBasicInfo(self,policy_iteration,policy,worksheet,path):
        file = open(path+policy+"_basic.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()
        
        
        
    def __formatBasicInfoHeader(self,policy,worksheet,path):
        file = open(path+policy+"_basic.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()