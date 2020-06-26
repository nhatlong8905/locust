'''
Created on Jun 15, 2020

@author: nhat.phan
'''
#import json
# import itertools
# from logging.handlers import RotatingFileHandler
# import socket
import logging
import gevent
from locust import HttpUser, TaskSet, task
from locust.env import Environment
from locust.stats import stats_printer
from locust.log import setup_logging

# def append_file_logger():
#     root_logger = logging.getLogger()
#     log_format = "%(asctime)s.%(msecs)03d000 [%(levelname)s] {0}/%(name)s : %(message)s".format(socket.gethostname())
#     formatter = logging.Formatter(log_format, '%Y-%m-%d %H:%M:%S')
#     file_handler = RotatingFileHandler('./locust.log', maxBytes=5 * 1024 * 1024, backupCount=3)
#     file_handler.setFormatter(formatter)
#     file_handler.setLevel(logging.INFO)
#     root_logger.addHandler(file_handler)    
# 
# append_file_logger()
# counter = itertools.count()
setup_logging("INFO", None)
class UserBehavior(TaskSet):
    def __init__(self, parent):
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
        
class User(HttpUser):
    host= "http://lgus3034-2k12:5555"
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 2000
    HttpUser
        
#setup Enviroment and Runner
env = Environment(user_classes=[User])
env.create_local_runner()
 
#start a webUI
env.create_web_ui("localhost",8089)
 
# start a greenlet that periodically outputs the current stats
gevent.spawn(stats_printer(env.stats))
 
# start the test
env.runner.start(1000, hatch_rate=100)
 
# in 60 seconds stop the runner
gevent.spawn_later(60, lambda: env.runner.quit())
 
# wait for the greenlets
env.runner.greenlet.join()
 
# stop the web server for good measures
env.web_ui.stop()















