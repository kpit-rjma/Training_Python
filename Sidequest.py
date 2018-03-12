import sys
import random

# Sidequest Methodology
# Define a sidequest as a turn-based interaction between player & NPC
# TurnNumber: The turn number
# Characteristics: Dictionary of values containing data about stats,
# populated later.
class Sidequest:
    def __init__(self):
        self.turnnumber = 0;
        self.characteristics = {
            "Name": "???",
            # Health, values 10 to 300, can drop
            # MaxHealth, values 10 to 300 & immutable
            # Resolve, 1 to 20, based on Health
            # Power, 1 to 20, based on Resolve and health
            # Intelligence, 1 to 20, entirely random
        }

    def populatecharacter(self):
        # Health can be between 10 and 300, by intervals of 10.
        self.characteristics["Health"] = (random.randint(1, 30) * 10)
        self.characteristics["MaxHealth"] = self.characteristics["Health"]
        # ...maybe include the possibility that the NPC has already taken some damage...?

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
        average += random.randint(0, 20)
        averagedivider += 1
        # ^Aggro skew (intended to increase aggression in NPCs
        self.characteristics["Aggro"] = average//averagedivider

    def charactergetaggro(self):
        if self.characteristics["Aggro"] < -12:
            return "Enamoured"
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
        else:
            return "Hateful"

    def charactercheckaggro(self):
        name = self.characteristics["Name"]
        data = self.charactergetaggro()
        response = "" + name + " seems to be " + data.lower() + " towards you."
        print(response)

    def turn(self):
        choice = ""
        name = self.characteristics["Name"]
        byeoption = "2"
        while choice != byeoption:
            if (self.turnnumber == 0):
                print("You have encountered " + name + "!\n")
            else:
                print("" + name + " is waiting for you...\n")
            print("What would you like to do?")
            print("1. Check\t2. Bye")
            choice = input("Enter number: ")
            print("\n\n")
            if choice == "1":
                self.charactercheckaggro()
            elif choice == byeoption:
                break
            else:
                print("Bad input! Try again...")
            self.turnnumber = self.turnnumber + 1



sidequest = Sidequest()
sidequest.populatecharacter()

print(sidequest.characteristics)
sidequest.turn()