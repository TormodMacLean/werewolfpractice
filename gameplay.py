import random
from collections import Counter
import Tkinter


# # Code to add widgets will go here...
# top.mainloop()
#
# __author__ = 'tmaclean'
#
# # gui classes
# class simpleapp_wx(wx.Frame):
#     def __init__(self,parent,id,title):
#         wx.Frame.__init__(self,parent,id,title)
#         self.parent = parent
#
# class simpleapp_tk(Tkinter.Tk):
#     def __init__(self,parent):
#         Tkinter.Tk.__init__(self,parent)
#         self.parent = parent
#
#
# this is the basic Character class I'm using, defined so can have a name for UI and be humans or werewolves
class Character(object):
    def __init__(self, name, species):
        self.name = name
        self.species = species


# the arrays and globals
villagers = []
accused = []
remaining = []
deadname = ""
gameStatus = 1


# todo check if names are unique
# sets the number of players and their names
def setup():
    global population
    global name
    while True:
        try:
            population = int(raw_input("How many players are there?"))
            if population < 5:
                print "This is too few players for a game of werewolf. Please enter a number higher than 4."
                continue
        except ValueError:
            print "You have not entered a number. Please enter a number higher than 4."
        break
    for person in range(population):
        while True:
            name = raw_input("What is the name of player " + str(person + 1) + "?")
            if name == "":
                print "Player's name must not be blank."
                continue
            else:
                break
        person = Character(name, "human")
        villagers.append(person)
    for player in random.sample(villagers, 2):
        player.species = "wolf"
    for player in villagers:
        print player.name + " you are a " + player.species


# functions for running the game
def vote(question, eligible=None):
    while True:
        accused[:] = []
        for member in villagers:
            if not eligible or member.species == eligible:
                while True:
                    choice = raw_input(member.name + question)
                    if not any(choice in candidate.name for candidate in villagers) or choice == "":
                        print choice + " is not the name of a living player. Please choose again."
                        continue
                    else:
                        accused.append(choice)
                        break
        sacrifice = Counter(accused)
        deathrow = sacrifice.most_common()
        (key, value) = deathrow[0]
        global deadname
        deadname = key
        if len(deathrow) > 1:
            (key2, value2) = deathrow[1]
            if value2 == value:
                print "The vote is tied. Please vote again."
                continue
        for victim in villagers:
            if victim.name == deadname:
                global deadspecies
                deadspecies = victim.species
                villagers.remove(victim)
        break


def day():
    print "day breaks and the village awakens"
    if deadname != "":
        print deadname + " has been eaten by wolves!"
    vote(", who do you think is the werewolf?")
    print deadname + " has been executed. " + deadname + " was a " + deadspecies
    victory()


def night():
    print "Night falls and everyone goes to sleep."
    print "The werewolves awaken."
    vote(", who do you choose as your victim?", "wolf")
    victory()


def victory():
    for x in villagers:
        remaining.append(x.species)
    if remaining.count("wolf") == len(villagers) or remaining.count("human") == len(villagers):
        print remaining[0] + " victory"
        global gameStatus
        gameStatus = 0
    remaining[:] = []


# the actual running of the game
setup()
while gameStatus > 0:
    day()
    if gameStatus > 0:
        night()
