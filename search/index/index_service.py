import redis
import Stemmer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Indexer(scalica_pb2.BetaProcessorServicer):
	def index(post, post_id):
		r = redis.Redis(
    		host='localhost',
    		port=6379)
		stemmer = Stemmer.Stemmer("english")
		inp = post.split(" ")
		for word in inp:
			word = stemmer.stemWord(word)
			if r.get(word) is None:
				r.set(word, post_id)
			else:
				r.rpush(word, post_id)


def main():
	server = index_pb2.beta_create_Index_server(Indexer())
	server.add_insecure_port('[::]:22222')
	server.start()
	try:
		while True:
		time.sleep(_ONE_DAY_IN_SECONDS)
	except KeyboardInterrupt:
		server.stop(1)

if __name__ == '__main__':
	main()
