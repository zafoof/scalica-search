from concurrent import futures
import redis
import Stemmer
import time
import search_pb2
import search_pb2_grpc
import grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Search(search_pb2_grpc.SearchServicer):
	def search(self, request, context):
		r = redis.Redis(
    		host='54.197.8.84',
    		port=6379)
		stemmer = Stemmer.Stemmer("english")
		post = request.text
		inp = post.split(" ")
		for word in inp:
			word = stemmer.stemWord(word)
			out = r.sunion(inp)
		return search_pb2.SearchReply(post_id = out)


def main():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))	
	search_pb2_grpc.add_SearchServicer_to_server(Search(), server)
	server.add_insecure_port('[::]:22221')
	server.start()
	try:
		while True:
			time.sleep(_ONE_DAY_IN_SECONDS)
	except KeyboardInterrupt:
		server.stop(1)

if __name__ == '__main__':
	main()
