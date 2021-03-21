#!/bin/sh

mkdir -p /opt/docker-object-classification &&
  chmod 777 /opt/docker-object-classification &&
  mkdir -p /opt/docker-object-classification/input-images &&
  chmod 777 /opt/docker-object-classification/input-images &&
  mkdir -p /opt/docker-object-classification/classifier-logs &&
  chmod 777 /opt/docker-object-classification/classifier-logs &&
  touch /opt/docker-object-classification/classifier-logs/classifier.log || exit
