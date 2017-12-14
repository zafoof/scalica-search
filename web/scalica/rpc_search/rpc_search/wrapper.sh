#!/bin/bash

until ${python web/scalica/rpc_search/rpc_search/search_service.py}; do
	echo "Search service crashed. Restarting"
done
