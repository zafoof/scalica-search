#!/bin/bash

until ${web/scalica/rpc_search/index/wrapper.sh}; do
	echo "Indexer crashed. Restarting"
done
