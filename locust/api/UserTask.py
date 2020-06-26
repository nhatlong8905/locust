'''
Created on Jun 15, 2020

@author: nhat.phan
'''
import logging
from locust import HttpUser
from locust.user.task import TaskSet, task

class UserBehavior(TaskSet):
    def __init__(self,parent):
        super(UserBehavior, self).__init__(parent)
        self.token = ""
        self.headers = {}
 
    def on_start(self):
        self.token = self.login()
        self.headers = {'Authorization': 'Token ' + self.token,'Content-Type' : 'application/json'}
         
    def login(self):
        response = self.client.post("/rest/Token", data={'user':'admin', 'password':'kratos'})
        logging.info("response= "+ response.text)
        return response.text
 
    @task(1)
    def getListServer(self):
        a = self.client.get("/rest/Server/Server",headers=self.headers)
        logging.info("getListServer= "+ a.text)
    
    @task(1)
    def getListSecurity(self):
        a = self.client.get("/rest/Security",headers=self.headers)
        logging.info("getListSecurityUser= "+ a.text)
        
    @task(1)
    def getListNode(self):
        a = self.client.get("/rest/Node",headers=self.headers)
        logging.info("getListNode= "+ a.text)
    def on_stop(self):
        TaskSet.on_stop(self)
class UserTask(HttpUser):
    def on_start(self):
        HttpUser.on_start(self)
    def on_stop(self):
        HttpUser.on_stop(self)
    host= "http://lgus3034-2k12:5555"
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 2000
        