#!/bin/bash
while true; do
  # Listen on port 8080 and respond with a simple HTML page
  { echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello, World!</h1>"; } | nc -l -p 8080
done

