# This script will run 50,000 simulations attempting to determine
# the number of rolls it takes on average to get yahtzees with any
# requested number of dice between 1 and 10.  It will then print
# the mean, the min, the max, the full set of data, and a graph.

import random

# gets the requested number of dice from the user
length = 0
chosen = False
done = False
while not done:
    length = int(raw_input("How large would you like the Yahtzee to be?\n" +
                    "Please enter an integer between 1 and 10. "))
    if length < 1 or length > 10:
        print("Please choose an integer between 1 and 10.")
        length = 0
    else:
        done = True

# labelling the dice
temp = 0
DICE = []
while temp < length:
    DICE += [temp]
    temp += 1

# allowing the user to choose whether to fix the target die value
done = False
ask = ""
while not done:
    ask = raw_input("Would you like to aim for a specific number? y/n ")
    if ask == 'y':
        chosen = True
    if ask in ['y','n']:
        done = True
    else:
        print("Please answer 'y' or 'n'.")

# if desired, lets the user manually select the target value
target = -1
done = False
while chosen and not done:
    ask = raw_input("Would you like to select the number? y/n ")
    if ask == 'y':
        while target < 0:
            target = int(raw_input("Enter an integer 1 - 6. "))-1
            if target not in [0,1,2,3,4,5]:
                target = -1
                print("Please choose between 1 and 6. ")
    if ask in ['y','n']:
        done = True
if target == -1 and chosen:
    target = random.randint(0,5)
    print("The target is: " + str(target+1))

roll = [] # stores an individual roll
keep = [] # whether to keep a rolled die or not
temp = 0
while temp < length: # makes roll/keep the correct length
    roll += [0]
    keep += [0]
    temp += 1
count = [0,0,0,0,0,0] # stores a count of each value in the roll
answer = [] # stores how many trials have taken n rolls
tRolls = 0 # total rolls (for mean calculation)

#running the trials

trial = 0
while trial < 50000:
    done = False
    rolls = 0
    while not done:
        rolls += 1
        count = [0,0,0,0,0,0]
        # roll dice that aren't to be kept
        for die in DICE:
            if not keep[die]:
                roll[die]=random.randint(0,5)
            count[roll[die]] += 1
        tCount = count[target]
        # if target not fixed, make target = value mode
        if not chosen:
            for value in [0,1,2,3,4,5]:
                if count[target] < count[value]:
                    target = value
        if count[target] == length: # Yahtzee!
            done = True # end the trial
            tRolls += rolls # add trial rolls to total
            # makes answer array long enough to hold data
            if len(answer) < rolls:
                answer = answer + ([0] * (rolls-len(answer)))
            answer[rolls-1] += 1
            temp = 0
            while temp < length: # resets keep array
                keep[temp] = 0
                temp += 1
            trial += 1
            # keep user aware of progress
            if trial % 1000 == 0:
                print("Trial " + str(trial))
        else: # no yahtzee. :( reset keep array
            for die in DICE:
                keep[die] = (roll[die] == target)

# compute mean

mean = str(tRolls/50000) + "." # integer part
mDec = 2 * (tRolls%50000) # decimal part
mean = mean + (5-len(str(mDec))) * "0" + str(mDec)
print("Mean = " + mean) # print mean
# compute min
tMin = 0 #total min
done = False
while not done:
    if answer[tMin]: # if some trial lasted tMin rolls:
        done = True
    tMin += 1
print("Min = " + str(tMin)) # print min
print("Max = " + str(len(answer))) # print max
print(answer) # give data to user

# print a graph!
i = 0
while i < 40:
    j = 0
    yVal = 7800 - 200*i
    if i % 4 == 3:
        graph = (4-len(str(yVal))) * " " + str(yVal)
    else:
        graph = "    "
    graph += "|"
    while j < len(answer):
        if answer[j] - (7800 - 200*i) > 150:
            graph += "X"
        elif answer[j] - (7800 - 200*i) > 100:
            graph += "x"
        elif answer[j] - (7800 - 200*i) > 0:
            graph += "."
        else:
            graph += " "
        j+= 1
    print(graph)
    i += 1
# print an x-axis
graph = "    +" + len(answer) * "-"
print(graph)
# print x values
graph = "     1"
temp = 1
while 10*temp < len(answer):
    graph += "        " + str(temp) + "0"
    temp += 1
print(graph)
print("y = number of times it took x rolls to get yahtzee")
