# base-dash-framework

A buildable Dash framework including an API, scheduled jobs, and a simple UI.

Contact SMIMAT for help on usage.

## Installation

To make best use of this, you will need your own virtual machine. VS Code is strongly recommended for easiest use.

Follow these steps:
  - SSH into your virtual machine
  - type 'git clone git@github.com:ch-robinson-internal/base-dash-framework.git <your_app_name_here>'
  - Navigate into this folder and work on your code from here. VS Code Remote Explorer is the easiest way to work with this

## Standing up the App

Once navigated into your folder, there are three easy options.
  - type 'make build' to stand up the app on your VM at port 3000
  - type 'make restart' after you have changed your code to see it go into effect
  - type 'make logs' to see a readout of any errors, or of any print statements you've added into your code

## Modifying the framework

You are free to modify this as you wish. If you want to turn this into its own project, please start a new repo and push your modified code there. You will not be able to push any changes to this repo.

If you do not need any particular part of the app, there are instructions in main/app.py on how to remove the unnecessary components.


