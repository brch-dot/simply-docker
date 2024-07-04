#!/bin/bash

set -e

echo "Initializing OVS database if not present..."
if [ ! -f /etc/openvswitch/conf.db ]; then
    echo "OVS database not found, creating new one..."
    ovsdb-tool create /etc/openvswitch/conf.db /usr/share/openvswitch/vswitch.ovsschema
else
    echo "OVS database already exists."
fi

echo "Starting OVS services..."
service openvswitch-switch start

echo "Waiting for OVS to be up..."
sleep 5

echo "Checking OVS status..."
ovs-vsctl show

echo "Running Mininet script..."
python3 /home/btsonev/docker2/mininet_script.py

tail -f /dev/null

