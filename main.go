package main

import (
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	// Create the app
	a := app.New()
	w := a.NewWindow("Hello Sanskar")

	// Create content
	label := widget.NewLabel("Hello World!")
	label.Alignment = fyne.TextAlignCenter
	
	btn := widget.NewButton("Click Me", func() {
		label.SetText("Welcome to Go on Android!")
	})

	// Layout
	w.SetContent(container.NewVBox(
		label,
		btn,
	))

	w.ShowAndRun()
}
