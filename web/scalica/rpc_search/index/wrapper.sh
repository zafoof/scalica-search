#!/bin/bash

until ${python web/scalica/rpc_search/index/index_service.py}; do
	echo "Indexer crashed. Restarting"
done
