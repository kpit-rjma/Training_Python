# The following code was meant to be part of a larger game in which
# a user could have interactions with other characters.
# This has since become standalone side-code that can run on its own
# but has no goal.
import random
import os

# Sidequest Methodology
# Define a sidequest as a turn-based interaction between player & NPC
# TurnNumber: The turn number
# Characteristics: Dictionary of values containing data about stats,
# populated by a call.
class SideQuest:

	# The following is the initialization of the Sidequest object, originally meant to be a
	# new state for a larger game.
    def __init__(self):
        self.turnnumber = 0
        self.characteristics = {
            "Name": "???",
            # Health, values 10 to 300, can drop
            # MaxHealth, values 10 to 300 & immutable
            # Resolve, 1 to 20, based on Health
            # Power, 1 to 20, based on Resolve and health
            # Intelligence, 1 to 20, entirely random
        }

	# The following creates a Non-Player Character by generating the stats.
	# The algorithms used for generating stats help create easy-to-grasp stat associations
	# These stats generally range from 0 to 20, but sometimes -20 to 20 when an "antithesis"
    # of a stat is possible
    def populatecharacter(self):

        # Health can be between 10 and 300, by intervals of 10.
        self.characteristics["Health"] = (random.randint(1, 30) * 10)
        self.characteristics["MaxHealth"] = self.characteristics["Health"]

        # Resolve can be between 1 and 20, based on health
        average = (self.characteristics["MaxHealth"]//10 + random.randint(1, 20) + random.randint(1, 20))
        average = average//3
        self.characteristics["Resolve"] = average
        if self.characteristics["Resolve"] < 1:
            self.characteristics["Resolve"] = 1
        elif self.characteristics["Resolve"] > 20:
            self.characteristics["Resolve"] = random.randint(15, 20)

        # Power can be between 1 and 20, based loosely on Resolve and Health
        average = (self.characteristics["MaxHealth"]//10 + self.characteristics["Resolve"] + random.randint(1, 20))
        average = average//3
        self.characteristics["Power"] = average
        if self.characteristics["Power"] > 20:
            self.characteristics["Power"] = 20

        # Intelligence can be between 1 and 20, it is random.
        self.characteristics["Intelligence"] = random.randint(1, 20)

        # Aggro can be between -20 (attachment) and 20 (aggressive), based on many factors.
        average = (self.characteristics["Intelligence"] * -2) + 20
        averagedivider = 1
        # ^Aggro value established based on intelligence
        if self.characteristics["Health"] < self.characteristics["MaxHealth"]:
            average += random.randint(-20, 0)
            averagedivider += 1
        # ^Aggro modified based on possible previously taken damage
        if self.characteristics["Resolve"] > 15:
            average += random.randint(0, 20)
            averagedivider += 1
        elif self.characteristics["Resolve"] < 5:
            average += random.randint(-20, 0)
            averagedivider += 1
        # ^Aggro modified based on heightened or low Resolve
        if self.characteristics["Health"] < 80:
            average += random.randint(-20, -5)
            averagedivider += 1
        elif self.characteristics["Health"] > 200:
            average += random.randint(3, 20)
            averagedivider += 1
        if self.characteristics["MaxHealth"] > 250:
            average += random.randint(5, 20)
            averagedivider += 1
        elif self.characteristics["MaxHealth"] < 100:
            average += random.randint(-20, -3)
            averagedivider += 1
        # ^Aggro modified based on Health and MaxHealth
        if self.characteristics["Power"] > 15:
            average += random.randint(0, 20)
            averagedivider += 1
        elif self.characteristics["Power"] < 5:
            average += random.randint(-20, 0)
            averagedivider += 1
        # ^Aggro modified based on Power extremes
        average += random.randint(-20, 20)
        averagedivider += 1
        # ^Aggro modified on random basis
        #average += random.randint(0, 20)
        #averagedivider += 1
        # ^Aggro skew (intended to increase aggression in NPCs
        self.characteristics["Aggro"] = average//averagedivider

    # Returns a string describing the NPC's attitude
    # Can also be used to obtain a generalized attitude
    def charactergetaggro(self):
        if self.characteristics["Aggro"] < -12:
            return "Enamored"
        elif self.characteristics["Aggro"] < -6:
            return "Attached"
        elif self.characteristics["Aggro"] < 0:
            return "Friendly"
        elif self.characteristics["Aggro"] == 0:
            return "Neutral"
        elif self.characteristics["Aggro"] < 6:
            return "Aloof"
        elif self.characteristics["Aggro"] < 12:
            return "Hostile"
        return "Hateful"

    # Prints a message about the attitude of the NPC towards the player
    def charactercheckaggro(self):
        #self.clearconsole()
        name = self.characteristics["Name"]
        data = self.charactergetaggro()
        response = "" + name + " seems to be " + data.lower() + " towards you."
        print(response)

    # Generates and returns a name, sparing some offensive possibilities
    # Names consist of a consonant, vowel, and consonant
    def createname(self):
        name = ""
        consonants = "bcdfghjklmnpqrstvwxz"
        vowels = "aeiouy"
        #remove all possible offensive names
        while (name.lower() == "" or name.lower() == "cuq" or name.lower() == "fag" or name.lower() == "fuc" or name.lower() == "fuk" or name.lower() == "vag" or name.lower() == "dam" or name.lower() == "hor" or name.lower() == "suk" or name.lower() == "suc" or name.lower() == "sux" or name.lower() == "fux" or name.lower() == "cux" or name.lower() == "kux" or name.lower() == "dic" or name.lower() == "dik" or name.lower() == "dix" or name.lower() == "nig" or name.lower() == "neg" or name.lower() == "gay" or name.lower() == "cum" or name.lower() == "kum" or name.lower() == "kuq" or name.lower() == "kuk" or name.lower() == "kuc" or name.lower() == "cuk"):
            name = "" + random.choice(consonants).upper()
            name = name + random.choice(vowels).lower()
            name = name + random.choice(consonants).lower()
        return name

    # Asks the character about their name, can return different possibilities
    # Attitude towards the player changes the outcome considerably if the
    # name was already given to the player.
    def charactergetname(self):
        #self.clearconsole()
        response = ""
        if self.characteristics["Name"] == "???":
            self.characteristics["Name"] = self.createname()
            response = "You introduce yourself... he also introduces himself:\n"
            response = response + "\"My name is " + self.characteristics["Name"] + ".\""
        else:
            response = response + "\"We have already been introduced...\"\n"
            response = response + "\"I am " + self.characteristics["Name"] + ", remember?\"\n"
            aggrolevel = self.charactergetaggro()
            if aggrolevel == "Enamored":
                response = response + self.characteristics["Name"] + " seems hurt that you forgot..."
            elif aggrolevel == "Attached":
                response = response + self.characteristics["Name"] + " seems slightly upset you forgot..."
            elif aggrolevel == "Friendly":
                response = response + self.characteristics["Name"] + " doesn't seem too bothered you forgot."
            elif aggrolevel == "Neutral":
                response = response + self.characteristics["Name"] + " isn't bothered at all you forgot."
            elif aggrolevel == "Aloof":
                response = response + self.characteristics["Name"] + " seems not to like you much anyway."
            elif aggrolevel == "Hostile":
                response = response + self.characteristics["Name"] + " seems like this is another reason not to like you."
            else:
                response = response + self.characteristics["Name"] + " seems not to care, but is mad at you for forgetting anyway."
        print(response)

	# This code doesn't work currently...
    # Please ignore, might be worth returning to later
    def clearconsole(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # This keeps the player in a loop until they exit the interaction.
    # This code provides options, and calls methods for player choices.
    # This code will get extremely complex with additional features.
    # If this code were to be developed further, a rework would be in line.
    def turn(self):
        choice = ""
        byeoption = "A"
        while choice != byeoption:
            if self.turnnumber == 0:
                print("You have encountered " + self.characteristics["Name"] + "!\n")
            else:
                print("" + self.characteristics["Name"] + " is waiting for you...\n")
            print("What would you like to do?")
            print("1. Check\t2. Introduce\nA. Abort/Say Goodbye")
            choice = input("Enter number: ")
            print("\n\n")
            if choice == "1":
                self.charactercheckaggro()
            elif choice == "2":
                self.charactergetname()
            elif choice.upper() == byeoption:
                break
            else:
                print("Bad input! Try again...")
            self.turnnumber = self.turnnumber + 1

sidequest = SideQuest()
sidequest.populatecharacter()

print(sidequest.characteristics)
sidequest.turn()
