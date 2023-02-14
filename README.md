[![Scraper](https://github.com/Caffeinated-Typists/Leetcode-Automations/actions/workflows/scrape.yml/badge.svg?branch=main)](https://github.com/Caffeinated-Typists/Leetcode-Automations/actions/workflows/scrape.yml)

# Why this Project ?

This project was made to track the progress of our college group for practicing Leetcode problems. Everyone needs to mandatorily solve 4 problems every week, and every solve will then be recorded in [this](https://docs.google.com/spreadsheets/d/1l9VE4AvIkeMqtuDuZ6qW5SKEP84F45DKnKTT6_ZvRKo/edit?usp=sharing) Google Sheet

# How we achieved it ?

We use selenium to scrape every user profile and check for questions submitted in the last 1 hours. The fresh questions are then updated to the Google sheet using Google API. The python script is executed every 15 minutes using Github Actions.
