import nltk
nltk.download('stopwords')
from concurrent import futures
from nltk.corpus import stopwords
import redis
import Stemmer
import time
import index_pb2
import index_pb2_grpc
import grpc
import re

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Indexer(index_pb2_grpc.IndexerServicer):
	def index(self, request, context):
		r = redis.Redis(
    		host='54.197.8.84',
    		port=6379)
		stemmer = Stemmer.Stemmer("english")
		post = request.text
		post_id = int(request.post_id)
		inp = post.split(" ")
		filt_inp = [word for word in inp if word not in stopwords.words('english')]
		for word in filt_inp:
			strippedword = re.sub("[^a-zA-Z]", "", word)
			stemmedword = stemmer.stemWord(strippedword)
			r.sadd(stemmedword, post_id)
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
