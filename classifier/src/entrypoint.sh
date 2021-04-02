#!/bin/sh

mkdir -p /opt/object-classifier &&
  chmod 777 /opt/object-classifier &&
  mkdir -p /opt/object-classifier/input-images &&
  chmod 777 /opt/object-classifier/input-images &&
  mkdir -p /opt/object-classifier/classifier-logs &&
  chmod 777 /opt/object-classifier/classifier-logs &&
  touch /opt/object-classifier/classifier-logs/classifier.log || exit
