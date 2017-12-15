import grpc
import search_pb2
import search_pb2_grpc
_TIMEOUT_SECONDS = 10

def search(text):
  	channel = grpc.insecure_channel('54.172.21.215:22221')
	stub = search_pb2_grpc.SearchStub(channel)
	request = search_pb2.SearchRequest(text=text)
	response = stub.search(request, _TIMEOUT_SECONDS)
 	r = []
	for p in response.post_id:
		r.append(int(p))
	print r
	return r
