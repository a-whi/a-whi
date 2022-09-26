"""
Assignment 1

Created by: Alexander Whitfield
Student ID: 32541767
"""

def analyze(results, roster, score):
    """
    This function takes a list of results, sorts them and then outputs the top 10 matches with the highest score into a list called
    'top10matches'. If there are not 10 matches available it will output however many there are. This function also looks for matches
    with a certain score, inputted with the 'score'. If no matches meet the score the match with a score closest and higher than the 
    desired score is outputted in to 'searchedmatches'. 
    In my implementation I first duplicate the results and combine them into one list, this gives me all matches in each variation. Then
    I sort the letters in the team names through radix sort. After that I then sort the team names with radix sort again so they are in 
    ascending lexicographical order. Finally I sort the scores with count sort as scores will only vary between 0 & 100 and they are 
    ordered in descending order. 
    Then I remove the duplicate matches and append the top 10 matches to a list and the match that meets the searchedmatches requirement 
    to its own list and return both lists. 

    Inputs:
        results: A list of lists with: 'team 1', 'team 2', 'match score'
        roster: An integer that denotes how many the character set is
        score: An integer value in the range of 0 to 100 inclusive
    
    Outputs: 
        top10matches: A list of 10 matches with the highest score, or the max amount of matches if there are less than 10
        searchedmatches: A list of matches with the same score as 'score' or with the closest score which is higher

    Time Complexity: O(NM)
    AUX Space Complexity: O(NM)

    O(N) --> refers to N being the number of matches in results
    O(M) --> refers to the number of characters within a team for each match.
    """
    #Import copy as I use it to deepcopy the results
    import copy
    #Initalising the output lists   [O(1)]
    final_output = []
    top10matches= []
    searchedmatches = []
    #Initalising the other lists which will be used later
    highscore_matches = []
    score50plus = []

    #Here I copy the results into a new list, I use deep copy as it won't affect the other list as I make changes to it
    lst = copy.deepcopy(results)        #Deep copy has a time & space complexity of O(N). 
    
    #This 'for' loop allows me to swap all matches so that I have every variation of each match
    #I then append the swapped matches back to the results list and from there I can sort all match variations
    for i in range(0, len(lst)):    #This for loop will have a time and space omplexity of O(N)
        lst[i][0], lst[i][1] = lst[i][1], lst[i][0]     #Time and Space complexity for this swap is O(1)
        lst[i][2] = 100 - lst[i][2]
        results.append(lst[i])      #append has a time and space complexity of O(1)

    #I am doubling the result length so now looping through the results will be O(2N) == O(N)

    #Setting up max and minimum values so I can use them later for my count sort
    max_value = 0
    min_value = 100
    for i in range(0, len(results)):    #[O(N)]
        if results[i][2] > max_value:   #[O(1)]
            max_value = results[i][2]   #[O(1)]
        elif results[i][2] < min_value: #[O(1)]
            min_value = results[i][2]   #[O(1)]

    #Sorts the team name characters so they are in order
    #Loops twice so it can do the characters in team 1 then the characters in team 2
    for j in range(2):  #[O(2)]
        for i in range(0, len(results)):    #[O(N)]
            #This turns the teams to strings of individual characters which can then be sorted in the radix sort 
            results[i][j] = list(results[i][j])     #list() has a time & space complexity of O(M) where M is the length of the team name
            radsort_teamsort(results[i][j], roster, j)  #Call radix sort function   #[O(N+M)]
            results[i][j] = ''.join(results[i][j])  #.join is O(N) and turns the characters in the team name and joins them back to a string

    #Now we sort the team names so they are in ascending order
    #This will loop twice to sort all of team 1 then team 2
    #Loops backwards so it sorts all the team 2s then sorts all the team 1s
    for j in range(1, -1, -1):  #[O(2)]
        radsort_teamsort(results, roster, j)    #Calls the same radix sort function #[O(N+M)]
        #Radix sort returns the results sorted in descending order so I reverse the list so its in ascending order
        results = results[::-1]     #O(N) time complexity as we are just copying the list and reversing it
        #I originally was working on radix sort going backwards but I never got it to work

    #Finally I count sort the result scores so they are in ascending score
    countsort_scores(results, min_value, max_value) #[O(N)]
    #This reverse the results so its in descending order
    results = results[::-1]     #[O(N)]

    #This will be a list with no duplicates
    nonduplist = [] 

    #Removing duplicate results
    #Fist I append the first value in results to nonduplist
    nonduplist.append(results[0])
    #This 'for' loop goes through all results and appends results that are not the same
    for i in range(len(results) - 1):
        if results[i] != results[i + 1]:
            nonduplist.append(results[i + 1])

    #Creating a temp list
    #This allows the nonduplist results to be changed without changing the results in the top10matches list
    #This comes in later when I find the seachedmatches
    temp_list = copy.deepcopy(nonduplist)       #O(N)
    #Append the top 10 matches or less if not 10
    for i in range(len(temp_list)):   #[O(N)]
        if i == (10):   
            break
        else:
            top10matches.append(temp_list[i])

    #To look for searchedmatches
    #This will return empty if the first score in results is smaller than the score (nonduplist will be in decending order)
    if nonduplist[0][2] < score:
        #Appends the 2 lists into the final_output and return it
        final_output.append(top10matches)   #O(1)
        final_output.append(searchedmatches)
        return final_output

    #If scores are smaller than 49 I'll have to flip the nonduplist so the scores are are below 50
    elif score <= 49:
    #adding the lowest score in the temp list to scores50plus incase when I flip the results there are none that are greater than or equal to score
        score50plus.append(temp_list[-1])
        for i in range(len(temp_list)-2,-1,-1): #Just adds all matches with the smae score to the score50plus list
            if score50plus[0][2] != temp_list[i][2]:  #Loop ends if the match scores aren't the same
                break
            else:
                score50plus.append(temp_list[i])

        #Now I swap the results in nonduplist so they are below 50
        for i in range(0, len(nonduplist)):    #This for loop will have a time and space complexity of O(N)
            nonduplist[i][0], nonduplist[i][1] = nonduplist[i][1], nonduplist[i][0] #Time and Space complexity for this swap is O(1)
            nonduplist[i][2] = 100 - nonduplist[i][2]
        #Add all scores that match the score or are higher to highscore_matches
        for i in range(len(nonduplist)):    #This will be O(N) in the worst case if every value in results == score
            if nonduplist[i][2] >= score:
                highscore_matches.append(nonduplist[i])
            #This list will be in increasing order as results are flipped
        
        #Now I append the score50plus to the end of the highscore_matches as they will be greater than the values already in highscore_matches
        highscore_matches.append(score50plus)

        #Append the first value to searched matches as it is the smallest
        searchedmatches.append(highscore_matches[0])
        for i in range(1,len(highscore_matches)-1): #Check to see if there are anymore matches with the same score
            if searchedmatches[0][2] != highscore_matches[i][2]:
                break
            else:
                searchedmatches.append(highscore_matches[i])
           
    elif score >= 50:
        for i in range(len(nonduplist)-1):  #O(N)
            if nonduplist[i][2] >= score:
                highscore_matches.append(nonduplist[i])
        #Now we have all matches >= to score in decending score order

        #Appends the last match of matches_with_scoreorhigher as it is the match closest to score
        searchedmatches.append(highscore_matches[-1])
        #Check the rest of the list for any matches with the same score as the one we appended
        #Looping backwards
        for i in range(len(highscore_matches)-2,-1,-1): #Starts -2 as the last result will already be appended to searched matches
            #Breaks immediatly if the last match in match_with_scoreorhigher isn't the same
            if searchedmatches[0][2] != highscore_matches[i][2]:
                break
            else:
                searchedmatches.append(highscore_matches[i])

    #Reverses the list so its in ascending lexicographical order
    searchedmatches = searchedmatches[::-1]
    #Returns the 2 lists that are required
    final_output.append(top10matches)
    final_output.append(searchedmatches)
    return final_output


def countsort_scores(results, min_value, max_value):
    """
    Counting sort:
    This count sort is used to sort the match scores in results. I chose to use this sorting algorithm as the scores would only vary 
    between 0 & 100 which is perfect for count sort to sort as the values aren't large enough for the algorithm to not be as effient. 

    Inputs:
        results: A list of lists with: 'team 1', 'team 2', 'match score'
        min_value: The smallest match score found in results
        max_value: The largest match score found in results
    
    Outputs: 
        Returns 'results' ordered in ascending order based on their match scores

    Time Complexity: O(N+M)
    AUX Space Complexity: O(N+M)

    O(N) --> refers to N being the number of matches in results
    O(M) --> refers to the number of characters within a team for each match.
    """
    #Finds the range of the list and adds 1 as python starts count at 0
    rangeofvaules = (max_value - min_value) + 1 
    #Creates a list for counting that will hold the values found in results
    counting = [0] * rangeofvaules
    #This will be were the sorted results are inputted
    output = [0] * len(results)      #len() has an O(1) time & space complexity.

    #Loops N times taking the score and subtracting the min_value so it can be input into the counting list in that index
    for i in range(0, len(results)):
        counting[results[i][2]- min_value] += 1

    #This put all the values in counting into proper positions
    #Currently: counting[1] = 5, counting[2] = 2
    #After: counting[0] = 5, counting[1] = 2
    for i in range(1,len(counting)):
        counting[i] += counting[i-1]

    #Looping in a decending order to put the values into the output array 
    for i in range(len(results)-1,-1,-1):
        output[counting[results[i][2] - min_value]-1] = results[i]
        #Subtract the count as it has been put into the output
        counting[results[i][2] - min_value] -= 1

    #Takes the values in output and puts them back into results
    for i in range(0, len(results)):
        results[i] = output[i] 


def rad_countsort(results, roster, j, column):
    """
    Radix counting sort for strings: 
    This count sort is used to sort the strings in order. To do this I convert the letters into integers to sort them then 
    convert them back at the end of the sorting process.

    Inputs:
        results: A list of lists with: 'team 1', 'team 2', 'match score'
        roster: An integer that denotes how many the character set is
        j: Tell the count sort part of radix sort to sort team 1 or 2
        column: Tells the sort what position in the string its on
    
    Outputs: 
        Returns 'results' back to radix sort which then sends it back to analyze

    Time Complexity: O(N+M)
    AUX Space Complexity: O(N+M)

    O(N) --> refers to N being the number of matches in results
    O(M) --> refers to the number of characters within a team for each match.
    """
    j = 0

    counting = [0] * roster #Creating a list with the range of unique values that it will get
    output = [0] * len(results)      #len() has an O(1) time complexity.
    minbase = ord('A') #Convert 'A' to an Unicode code point value
    #'A' being the smallest letter that can be inputted we use it as our minium value.

    #Creates the count
    #Gets column letter within the team name string
    for i in range(0, len(results)):
        character = ord(results[i][j][column]) - minbase
        counting[character] += 1    #Adds 1 to that counts index

    #This put all the values in counting into proper positions
    #Currently: counting[1] = 5, counting[2] = 2
    #After: counting[0] = 5, counting[1] = 2
    for i in range(1,len(counting)):
        counting[i] += counting[i-1]

    #Get index of current letter of item at index col in count array
    #Looping in a decending order to put the values into the output array
    for i in range(len(results)-1, -1, -1):
        character = ord(results[i][j][column]) - minbase
        output[counting[character] - 1] = results[i]
        #Subtract the count as it has been put into the output
        counting[character] -= 1

    #Takes the values in output and puts them back into results
    for i in range(0, len(results)):
        results[i] = output[i] 


def radsort_teamsort(results, roster, j):
    """
    Radix sort:
    This radix sort sorts strings, I use it to sort the characters in the team names in acending order and I use to then sort 
    the team names in order. To do this I call a count sort function that I have modified to sort strings instead of integers.
    The radix count sort all converts the strings to decimal using the ord() function then sort it like an integer, at the 
    end it converts it back to a string and returns results. 

    Inputs:
        results: A list of lists with: 'team 1', 'team 2', 'match score'
        roster: An integer that denotes how many the character set is
        j: Tell the count sort part of radix sort to sort team 1 or 2

    Outputs: 
        Returns 'results' ordered in decending order based on the list it sorted

    Time Complexity: O(M(N+b))
    AUX Space Complexity: O(N+M)

    O(N) --> refers to N being the number of matches in results
    O(b) --> refers to the base. I convert the characters to integers so the base is 10
    O(M) --> refers to the number of characters within a team for each match.

    """
    #First we find the length of the team names
    team_length = len(results[0][0])    #Team 1 and Team 2 are the same length

    for column in range(team_length-1, -1, -1):    #This will loop team length - 1 times decreasing by 1 each time until its gone through all letters
        rad_countsort(results, roster, j, column)