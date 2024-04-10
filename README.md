# UOCIS322 - Project 3 Annagram Game


# Descriptions


## Application


This is a simple webpage game in which a user is prompted with a list of words and a jumble of letters with which to make the words. In order to win the user must type three words from the list that can be made using the letters provided in the jumble. When the user enters a word, the program will let the user know if the input was correct and if the user has won the game.



## Algorithm

There is no submit button as submits are done after each key press. If the user has typed a word from the list that can not be made with the letters then then a message will appear letting them know. If the user has typed a word not on the list or one already caught (in other words an invalid word) then a corresponding message will appear. If the user typed a correct word then if it is not the final one needed it will appear at the bottom with the others already found, else the user will be redirected to the success page. The game is built using AJAX, flask, Javascript, JQuery, and python. 




# Instructions For Use


## Docker Compose
To run docker compose for this application first ascertain that you are in the correct directory, specifically the one that contains the Docker-compose file. From there proceed to make your Docker image by executing the command:


docker-compose up --build



Supposing everything went smoothly, your web application should now be up and running. 




# Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani. Completed by Ellison Schilling.

## Contact Address

ellisons@uoregon.edu 
