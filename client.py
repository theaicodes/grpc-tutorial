import sys
import os
import json
import time
from glob import glob
import concurrent
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import threading
from urllib.parse import urlparse

# importing gRPC stuff
import grpc
# import grpc.aio as aio
import grpcFiles.aiServer_pb2 as aIModelServer
import grpcFiles.aiServer_pb2_grpc as aIModelServer_grpc

def pingServer():
    address = '127.0.0.1'
    port = '4002'
    with grpc.insecure_channel('%s:%s' % (address, port)) as channel:
        stub = aIModelServer_grpc.AIModelServerStub(channel)
        try:
            req = aIModelServer.pingMsg(msg = 'ping')
            start = time.time()
            response = stub.ping(req)
            end = time.time()
            # print time from start time to end time
            print('[%s] [Ping] [Msg: %s] [Time: %s Sec]' % (threading. get_ident(), response.msg, round(end-start, 5)))
        except Exception as e:
            print(e)

#? INFO: Upload an article to the server
def processInstance(article, content):
    print('[%s] [path] %s' % (threading. get_ident(), article))
    address = '127.0.0.1'
    port = '4002'
    with grpc.insecure_channel('%s:%s' % (address, port)) as channel:
        stub = aIModelServer_grpc.AIModelServerStub(channel)
        data = {
            'title': article,
            'content': content
        }
        try:
            req = aIModelServer.RequestExample(**data)
            response = stub.processInstance(req)
            print(response.msg)
            print('[%s] [Processing | Done!] [title: %s] [MSG: %s]' % (threading. get_ident(), article, response.msg))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    tests = {
        'ping' : False,
        'processInstance' : True
    }
    #test pinging the server
    if tests['ping']:
        pingServer()
    if tests['processInstance']:
        processInstance('test', 'test')