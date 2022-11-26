import sys
from concurrent import futures
import threading
import time
import json

import grpc
# import grpc.aio as aio
import grpcFiles.aiServer_pb2 as aIModelServer
import grpcFiles.aiServer_pb2_grpc as aIModelServer_grpc

with open('./config.json', 'r') as f:
    jsonData = f.read()
serverConfig = json.loads(jsonData)

class AIModelServer(aIModelServer_grpc.AIModelServerServicer):
    #? INFO: Initializing Article AIModelServer
    def __init__(self):
        print("[%s] Initializing AIModelServer configuration..." % (threading.get_ident()))
        self.model_cfg = serverConfig['aIModelServer']
        #self.model = ArticleAIModelServer(self.model_cfg)
        print("[%s] AIModelServer configuration loaded" % (threading.get_ident()))

    #? INFO: Process an article
    def processInstance (self, request, context):
        title = request.title
        content = request.content
        print('[%s] Processing article "%s"...' %(threading.get_ident(), title[:40]))
        start_time = time.time()
        try:
            pass
            #title, content = self.model.predict(title, content)
        except Exception as e:
            msg = '[{0}] Failure to spin article "{1}". Error: {2}'.format(
                threading.get_ident(), title[:40], e
            )
            print(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(msg)
            return aIModelServer.status(
                code = -1,
                msg = json.dumps({
                    'title': "Failure to spin article: " + title,
                    'content': msg
                })
            )
        print('[%s][%s] Article "%s" has been processed in %s seconds' %(time.ctime(), threading.get_ident(), title[:40], (time.time() - start_time)))
        return aIModelServer.status(
            code = 1,
            msg = json.dumps({
                'title': title,
                'content': content
            })
        )

    #? INFO: Pinging the Uploader to check if it is alive
    def ping(self, request, context):
        print('[%s] Ping...' %(threading.get_ident()))
        return aIModelServer.status(
            code = 1,
            msg = "Pong!"
        )

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=serverConfig['server']['max_workers']))
    aIModelServer_grpc.add_AIModelServerServicer_to_server(AIModelServer(), server)
    server.add_insecure_port("%s:%s" % (serverConfig['server']['address'], serverConfig['server']['port']))
    server.start()
    print("Article AIModelServer is running on %s:%s" % (serverConfig['server']['address'], serverConfig['server']['port']))
    try:
        while True:
            print("[%s] [AIModelServer: ON] [%s:%s] [Threads: %i]" % (time.ctime(), serverConfig['server']['address'], serverConfig['server']['port'], threading.active_count()))
            time.sleep(60)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        server.stop(0)

if __name__ == '__main__':
    server()