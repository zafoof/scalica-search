# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import index_pb2 as index__pb2


class IndexerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.index = channel.unary_unary(
        '/index.Indexer/index',
        request_serializer=index__pb2.IndexPostRequest.SerializeToString,
        response_deserializer=index__pb2.IndexPostReply.FromString,
        )


class IndexerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def index(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_IndexerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'index': grpc.unary_unary_rpc_method_handler(
          servicer.index,
          request_deserializer=index__pb2.IndexPostRequest.FromString,
          response_serializer=index__pb2.IndexPostReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'index.Indexer', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
