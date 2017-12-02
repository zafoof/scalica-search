import grpc
import index_pb2
import index_pb2_grpc
from inspect import getmembers
_TIMEOUT_SECONDS = 10

def index_post(post_id, text):
  	channel = grpc.insecure_channel('localhost:22222')
	stub = index_pb2_grpc.IndexerStub(channel)
	request = index_pb2.IndexPostRequest(post_id=post_id, text=text)
	response = stub.index(request, _TIMEOUT_SECONDS)
 	print response
