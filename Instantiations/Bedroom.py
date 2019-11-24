from Utility.Room import Room
from Utility.Item import *
from Utility.Interactions import *

bunnyExamine = ["You go over to the bunny and cage and you notice some cucumbers bagged up on the side, with a "
                "paper note "
                "from your nanny reminding you not to eat the cucumbers. As if you would forget that you were deathly "
                "allergic to cucumbers… You can do with the cucumbers what you please, although your poor bunny sounds "
                "like he's really hungry."]
bunnyPickup = "Against all rules of the theory of human interaction with cute fluffy small animals, " \
              "you ignore your starving bunny and pick him up in his cage."
bunnyInteractText = {0: "You do something to interact with the bunny"}
bunnyInteraction = Interaction(0, bunnyInteractText)
bunny = Item("bunny", bunnyExamine, bunnyPickup, bunnyInteraction, True)

booksExamine = ["There are three books on your bookshelf. Your stepmother took away all your others when"
                "she caught you reading them late at night, so there's not much left now. \nHansel and Gretel: Man,"
                "you really want some cookies\nA heavily abridged encyclopedia: You definitely haven't fed your "
                "bunny some of the pages\nWheelock's Latin: A book in some foreign language by someone named R. S. Enic."
                "What a weird name."]
booksPickup = "You grab the three books from the bookshelf."
bookInteractText = {0: "You are so desperate to take your mind off of cookies that you start reading the encyclopedia, "
                       "but quickly realize your mistake. Who wants to read that?",
                    1: "Reading the books didn't distract you from the thought of cookies before, but maybe you can "
                       "try again... Nope, still didn't work."}
bookInteraction = Interaction(1, bookInteractText)
books = Item("books", booksExamine, booksPickup, bookInteraction, True)

globeExamine = ["Your real mother gave this globe to you as a birthday present just a few weeks before she died. On it,"
                " you can still see the faded circles on the places you and her and father planned to visit on your "
                "trip around the world."]
globePickup = "You pick up the globe rather awkwardly."
globeInteractText = {0: "You spin the globe absent-mindedly. Nothing happens."}
globeInteraction = Interaction(0, globeInteractText)
globe = Item("globe", globeExamine, globePickup, globeInteraction, True)

rockingHorseExamine = ["You always wanted a real horse, but father always said that you couldn't take care of one."
                       "Instead he got you this rocking horse. It's too small for you now."]
rockingHorsePickup = "You struggle to lift up the wooden horse, but you eventually get a good grip."
rockingHorseInteractText = {0: "You try to sit on the rocking horse, but it's much too small for you, and you quickly"
                               "get off for fear of breaking it."}
rockingHorseInteraction = Interaction(0, rockingHorseInteractText)
rockingHorse = Item("rocking horse", rockingHorseExamine, rockingHorsePickup, rockingHorseInteraction, True)

door = Door("door", "bedroom", "hallway", False)

bedroom = Room("bedroom", [bunny, books, globe, rockingHorse, door], "You are in your own bedroom.", [])
