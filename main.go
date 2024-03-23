package main

import (
  "fmt"
  "os"
  "log"
  "github.com/otiai10/gosseract/v2"
)

type ImageData struct {
  name string
  text string
}

func main() {
  entries, err := os.ReadDir("./images/")

  if err != nil {
    log.Fatal(err)
  }

  for _, e := range entries {
    fmt.Println(e.Name())
  }

	client := gosseract.NewClient()
	defer client.Close()
	client.SetImage("./images/Step2.jpg")
	text, err := client.Text()
  if err != nil {
    log.Fatal(err)
  }
	fmt.Println(text)
}

