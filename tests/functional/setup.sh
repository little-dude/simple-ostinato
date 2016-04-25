#!/bin/sh

setup() {
    ip link add vostinato0 type veth peer name vostinato1
    ip link set vostinato0 up
    ip link set vostinato1 up
    drone > drone.logs 2>&1
}

teardown() {
    ip link set vostinato0 down
    ip link set vostinato1 down
    ip link del vostinato0
    killall drone
}

set -x
if [ "$1" = "setup" ] ; then
    setup
else
    teardown
fi
