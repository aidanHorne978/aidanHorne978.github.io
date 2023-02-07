#!/usr/bin/env python
from urllib.request import urlopen

# Gets input from stdin and processes it and also stores
# all the votes in a string so they are properly formatted
# when tallying all the winning votes
votes = dict([])
bigdata = []
req = urlopen("https://aidanHorne978.github.io/projects/testcases/pdftest.txt") 
bigdata = req.read()
bigdata = str(bigdata, 'utf-8')
bigdata = bigdata.split('\n')
data = bigdata[0]
tempdata = []
temp = ""
candidate_count = 0
i = 1
while data:
    try:
        temp += data + " "
        tempdata.append(data.split())
        data = bigdata[i]
        print(data)
        i += 1
    except IndexError:
        break
for vote in tempdata:
    for j in vote:
        if j not in votes:
            votes[j] = 0
            candidate_count += 1
all_votes = temp.split(" ")
# run through the votes and count them for each round and then
# sort them in ascending order and decide whether there is a tie
# or not and display the round information, then keep going until
# a winner is decided.
voter_round = 0
eliminated = []
round_keys = []
round_values = []
no_tie = True
no_winner = True
while no_winner:
    candidate_eliminated = []
    for candidate in tempdata:
        try:
            if candidate[0] not in eliminated:
                votes[candidate[0]] += 1
            else:
                i = 0
                while candidate[i] in eliminated:
                    i += 1
                votes[candidate[i]] += 1
        except IndexError:
            continue

    # Sorting in ascending order
    votes = sorted(votes.items())
    votes = sorted(votes, key=lambda item: item[1], reverse=True)
    votes = dict(votes)
    # If we only have one candidate left they are the winner
    # So we print out the information and the program is finished

    if len(votes) == 1:
        key, value = list(votes.items())[0]
        print("Round {}".format(voter_round + 1))
        print("%-12s%-12i" % (key, value))
        print("Winner: {} ".format(key))
        no_winner = False
        exit()

    value = list(votes.values())[0]
    counter = 0
    for i in range(len(votes.items())):
        counter += list(votes.values())[i]

    if value > counter / 2:
        print("Round {}".format(voter_round + 1))
        for i in range(candidate_count):
            key, value = list(votes.items())[i]
            print("%-12s%-12i" % (key, value))
        key = list(votes.keys())[0]
        print("Winner: {} ".format(key))
        no_winner = False
        exit()

    print("Round {}".format(voter_round + 1))
    for i in range(candidate_count):
        key, value = list(votes.items())[i]
        print("%-12s%-12i" % (key, value))

    # # Deciding if it's a tie between the bottom two candidates
    # # and deciding if it's a breakable tie or not.
    try:
        if list(votes.values())[-1] == list(votes.values())[-2]:
            candidate1 = list(votes.keys())[-1]
            candidate2 = list(votes.keys())[-2]
            no_tie = False
            run_loop = True
            if voter_round == 0:
                print("Unbreakable tie")
                exit()
            for r in reversed(round_keys):

                counter1 = 0
                for i in r:
                    if i[0] == candidate1:
                        break
                    counter1 += 1
                counter2 = 0

                for i in r:
                    if i[0] == candidate2:
                        break
                    counter2 += 1

                if r[counter1][1] < r[counter2][1]:
                    print("Eliminated: {}".format(list(votes.keys())[-1]))
                    print()
                    candidate_eliminated = list(votes.keys())[-1]
                    run_loop = False
                    break
                elif r[counter1][1] > r[counter2][1]:
                    print("Eliminated: {}".format(list(votes.keys())[-2]))
                    print()
                    candidate_eliminated = list(votes.keys())[-2]
                    run_loop = False
                    break
            if run_loop:
                print("Unbreakable tie")
                no_winner = False
                exit()
    except IndexError:
        continue


    # Printing output of each round if there is no tie
    if no_tie:
        if candidate_count > 2:
            print("Eliminated: {}".format(list(votes.keys())[-1]))
            candidate_eliminated = list(votes.keys())[-1]
            print()

    # Removing the eliminated candidate, appending the last rounds votes
    # to an array if needed for comparing in the case of a tie and increasing
    # the round counter by one.
    eliminated.append(candidate_eliminated)
    no_tie = True
    del votes[candidate_eliminated]
    votes = sorted(votes.items())
    votes = sorted(votes, key=lambda item: item[1], reverse=True)
    round_keys.append(votes)
    votes = dict(votes)
    candidate_count -= 1
    voter_round += 1
    votes = votes.fromkeys(votes, 0)