from concurrent import futures
import redis
import Stemmer
import time
import index_pb2
import index_pb2_grpc
import grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Indexer(index_pb2_grpc.IndexerServicer):
	def index(self, request, context):
		r = redis.Redis(
    		host='localhost',
    		port=6379)
		stemmer = Stemmer.Stemmer("english")
		post = request.text
		post_id = request.post_id
		inp = post.split(" ")
		for word in inp:
			word = stemmer.stemWord(word)
			r.lpush(word, post_id)
		return index_pb2.IndexPostReply(text = "DONE")


def main():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))	
	index_pb2_grpc.add_IndexerServicer_to_server(Indexer(), server)
	server.add_insecure_port('[::]:22222')
	server.start()
	try:
		while True:
			time.sleep(_ONE_DAY_IN_SECONDS)
	except KeyboardInterrupt:
		server.stop(1)

if __name__ == '__main__':
	main()
