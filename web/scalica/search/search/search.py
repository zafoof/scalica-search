import grpc
import search_pb2
import search_pb2_grpc
_TIMEOUT_SECONDS = 10

def search(text):
  	channel = grpc.insecure_channel('localhost:22221')
	stub = search_pb2_grpc.SearchStub(channel)
	request = search_pb2.SearchRequest(text=text)
	response = stub.search(request, _TIMEOUT_SECONDS)
 	print response
	return response
