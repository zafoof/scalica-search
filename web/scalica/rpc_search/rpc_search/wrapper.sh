#!/bin/bash

until ${web/scalica/rpc_search/rpc_search/wrapper.sh}; do
	echo "Search service crashed. Restarting"
done
