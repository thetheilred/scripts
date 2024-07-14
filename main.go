package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os/exec"
	"strconv"
)

type Response struct {
	OK    bool
	Error string
}

var passwordGeneratorCmd = flag.String("password-generator", "/home/roman/src/scripts/password-generator.py", "Provide password generator executable")
var port = flag.String("port", "80", "Provide port to listen on")

func main() {
	flag.Parse()
	http.HandleFunc("/v1/password", func(w http.ResponseWriter, r *http.Request) {
		lengthStrParam := r.URL.Query().Get("length")
		countStrParam := r.URL.Query().Get("count")
		var length, count int = 8, 1
		var err error
		if lengthStrParam != "" {
			length, err = strconv.Atoi(lengthStrParam)
			if err != nil {
				json.NewEncoder(w).Encode(Response{OK: false, Error: fmt.Sprintf("Query parameter `length` is invalid: %s", err.Error())})
				return
			}
		}
		if countStrParam != "" {
			count, err = strconv.Atoi(countStrParam)
			if err != nil {
				json.NewEncoder(w).Encode(Response{OK: false, Error: fmt.Sprintf("Query parameter `count` is invalid: %s", err.Error())})
			}
		}
		cmd := exec.Command(*passwordGeneratorCmd, "--length", fmt.Sprintf("%d", length), "--count", fmt.Sprintf("%d", count))
		res, err := cmd.Output()
		if err != nil {
			json.NewEncoder(w).Encode(Response{OK: false, Error: fmt.Sprintf("Error: %s\nStdout: %s\nStderr: %s", err.Error(), cmd.Stdout, cmd.Stderr)})
		}
		fmt.Fprintf(w, "%s", string(res))
	})
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", *port), nil))
}
