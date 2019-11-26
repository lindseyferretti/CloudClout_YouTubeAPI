from __future__  import print_function
import boto3
import json
import os, sys
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import requests

CLUSTER_ENDPOINT = os.environ['CLUSTER_ENDPOINT']
CLUSTER_PORT = os.environ['CLUSTER_PORT']

def run_sample_gremlin_websocket(event):
    print('running gremlin websocket code')
    remoteConn = DriverRemoteConnection('ws://' + CLUSTER_ENDPOINT + ":" + CLUSTER_PORT + '/gremlin','g')
    graph = Graph()
    g = graph.traversal().withRemote(remoteConn)
    
    myList = g.V().hasLabel('Tag').has('title', event["tag"]).out().out().values('title').toList()
    myList = list(filter(lambda x: x != event["tag"], myList))
    remoteConn.close()
    return myList

def lambda_handler(event, context):
    print(event)
    print('hello from lambda handler')

    ## run gremlin query
    if CLUSTER_ENDPOINT and CLUSTER_PORT:
        results = run_sample_gremlin_websocket(event)
    else:
        print("provide CLUSTER_ENDPOINT and CLUSTER_PORT environment varibles")

    response = {
        'statusCode': 200,
        'body': 'Lambda success!'
    }
    return json.dumps(results)


