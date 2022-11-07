# Why this Project ?

This project was made to track the progress of our college group for practicing Leetcode problems. Everyone needs to mandatorily solve 4 problems every week, and every solve will then be recorded in [this](https://docs.google.com/spreadsheets/d/1l9VE4AvIkeMqtuDuZ6qW5SKEP84F45DKnKTT6_ZvRKo/edit?usp=sharing) Google Sheet

# How we achieved it ?

We use selenium to scrape every user profile and check for questions submitted in the last 5 hours. The fresh questions are then updated to the Google sheet using Google API. The python script is ran every hour or two depending upon the time of the day using Github Actions.
