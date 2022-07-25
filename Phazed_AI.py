from collections import defaultdict as dd
from itertools import combinations

CARD_VALUE = 0
CARD_SUIT = 1
special_value={'0': 10, 'J': 11, 'Q': 12, 'K': 13}
RED_SUIT = 'HD'
BLACK_SUIT = 'SC'
PHASE = 0
CONTENT = 1


def sum_hand(combination):
    """ Accepts a string of card values, 'combinations', as input and returns 
    the total sum of all values in the combination
    """
    
    special_value={'A': 1, '0': 10, 'J': 11, 'Q': 12, 'K': 13}
    total = 0
    
    for value in combination:
        
        if value in special_value:
            total += special_value[value]
            
        else:
            total += int(value)
            
    return total 


def phase1(hand):
    """ Accepts a list of cards (made up of value and suit), 'hand', and if 
    possible, returns two sets of three cards of same value in a list. If not, 
    returns dictionary of desired cards in a dictionary where key is priority.
    """
    
    hand = hand[::-1]
    values = dd(int)
    completed = []
    ace_counter = 0
    desired_cards = dd(list)
    
    # sets up 'values' dictionary, Key is the card value and value is frequency
    for card in hand:
        
        if card[CARD_VALUE] == 'A':
            ace_counter += 1
            
        else:
            values[card[CARD_VALUE]] += 1
    
    # goes through each item in 'values', from highest frequency to lowest
    for key, value in sorted(values.items(), key=lambda x: x[1],
                             reverse=True):
        
        # 'set_card' will append to completed when a set is complete
        set_card = []
        if value >= 3:
            
            # ensures only three values are appended to 'set_card'
            count = 0
            
            # finds all card in the hand which match value
            for card in hand:
                
                if card[CARD_VALUE] == key and count <= 2:
                    set_card.append(card)
                    values[key] -= 1
                    count += 1
                    
            completed.append(set_card)
            
        elif value == 2 and ace_counter >= 1:
            # checks if there will be enough aces to complete any set
            if len(completed) == 1 or ace_counter >= 2:
                
                count = 0
                # 'a_count' ensures only one ace gets appended
                a_count = 0
                copy_hand = hand.copy()
                
                # finds all card in the hand which match value
                for card in copy_hand:
                    
                    if card[CARD_VALUE] == key and count <= 2:
                        set_card.append(card)
                        hand.remove(card)
                        count += 1
                        
                    elif (card[CARD_VALUE] == 'A' and count <= 2 
                          and a_count < 1):
                        set_card.append(card)
                        hand.remove(card)
                        ace_counter -= 1
                        a_count += 1
                        count += 1
                        
                completed.append(set_card)
    
    if len(completed) < 2:
        # goes through each key, value in 'values' to add to 'desired card' 
        for key, value in values.items():
            
            set_value = []
            
            if value == 2:
                priority = 1
            else:
                priority = 2
                
            for suit in 'CSHD':
                set_value.append(str(key) + suit)
                
            # key is priority and values are all the possible card
            desired_cards[priority].append(set_value)
            
        if not desired_cards:
            return "Anything"
        
        else:
            return desired_cards
        
    # checks if 3 possible completion
    elif len(completed) > 2:
        completed.pop()
        return completed
    
    return completed


def phase2(hand):
    """ Accepts a list of cards (made up of value and suit), 'hand', and if 
    possible, returns one set of seven cards of the same suit in a list. If 
    not, returns a list of desired cards.
    """
    values = dd(int)
    completed = []
    desired_suit = ''
    ace_counter = 0
    desired_cards = []
    
    # sets up 'values' dictionary, Key is the card suit and value is frequency
    for card in hand:
        if card[CARD_VALUE] == 'A':
            ace_counter += 1
        else:
            values[card[CARD_SUIT]] += 1
    
    # goes through each item in 'values' to check if there is a phase and
    # sets 'desired_suit' to that suit
    for key, value in values.items():
        
        if value >= 7:
            desired_suit = key
            values[key] -= 7
            break
        
        # checks if there are atleast 2 non-aces and together there will be 7
        elif value >= 2 and value + ace_counter >= 7:
            
            desired_suit = key
            values[key] -= value
            ace_counter -= 7 - value
            break
    
    if not desired_suit:
        # finds the maximum frequency of all suits
        max_suit = max([(y, x) for x, y in values.items()])[0]
        
        # appends to 'desired_card' all cards with max frequency suit/s
        for dic_key, dic_value in values.items():
            
            if dic_value == max_suit:
                
                for value in '234567890JQK':
                    desired_cards.append(value + dic_key)
                    
        return desired_cards
    
    else:
        # appends to 'completed' all cards in hand with 'desired_suit'
        for card in hand:
            if card[CARD_VALUE] != 'A' and card[CARD_SUIT] == desired_suit:
                completed.append(card)
        
        # appends as many aces needed to get 7 cards
        while len(completed) < 7:
            for card in hand:
                if card[CARD_VALUE] == 'A':
                    completed.append(card)
                    
    return completed


def phase3(hand):
    """ Accepts a list of cards (made up of value and suit), 'hand', and if 
    possible, returns two sets of cards which accumulated add to 34. If not, 
    returns a string 'Anything'.
    """
    
    # one string value of all card value of cards in hand 
    string_hand_value = ''
    for value in hand:
        string_hand_value += value[CARD_VALUE]
        
    match = []
    completed = []
    
    # goes through the highest possible length of set1 to the lowest 3, as the
    # second set needs atleast 3  cards to phase
    for ran in range(len(hand) - 3, 2, -1):
        
        # finds all combination of card value with the range
        for combination1 in combinations(string_hand_value, ran):
            
            # if values found to complete phase 3, the loop break
            if match:
                break
            
            # creates a copy of 'string_hand_value' by add a value and slicing
            # it away, so changes can be made to the copy 
            copy_string_hand_value = (string_hand_value + 'X')[:-1]
            
            # finds the total of that combination of values
            total = sum_hand(combination1)
            
            if total == 34:
                
                # removes all values from copy that appear in combination1
                for character in combination1:
                    copy_string_hand_value = copy_string_hand_value.replace(
                                             character, '', 1)
                
                # repeats what has been done without used values
                for ran2 in range(len(hand) - ran, 3, -1):
                    
                    for combination2 in combinations(copy_string_hand_value,
                                                     ran2):
                        
                        total = sum_hand(combination2)
                        # if second combination also equal 34
                        if total == 34:
                            # both are appended
                            match.append(list(combination1))
                            match.append(list(combination2))
    
    # if no potential phase completion
    if not match:
        return 'Anything'
    
    # goes through each value in match, and appends cards which match that
    # value to completed
    for element in match:
        set_completed = []
        
        for value in element:
            
            for card in hand:
                
                if card[CARD_VALUE] == value:
                    set_completed.append(card)
                    hand.remove(card)
                    break
        completed.append(set_completed)
        
    return completed


def phase4(hand):
    """ Accepts a list of cards (made up of value and suit), 'hand', and if 
    possible, returns two sets of four cards of same value in a list. If not, 
    returns list of desired cards.
    """
    
    values = dd(int)
    ace_count = []
    match = []
    match_values = []
    set1 = []
    set2 = []
    completed = []
    desired_cards = []
    copy_hand = hand.copy()
    
    # sets up 'values' where key is card value and value is frequency
    for card in copy_hand:
        # removes ace from hand and added to 'ace_count'
        if card[CARD_VALUE] == 'A':
            ace_count.append(card)
            hand.remove(card)
            
        else:
            # checks there are only 4 cards of that value
            if values[card[CARD_VALUE]] < 4:
                values[card[CARD_VALUE]] += 1
            else:
                hand.remove(card)
    
    string_value = ''
    copy_values = values.copy()
    
    # goes the 'values' dictionary removing any one offs and adding frequency 
    # to 'string_value'
    for dic_key, dic_value in copy_values.items():
        # a set cannot have one non-ace value
        if dic_value == 1:
            del values[dic_key]
        else:
            string_value += str(dic_value)
    
    # goes through all combination of frequencies of card value
    for combination in combinations(string_value, 2):
        # checks if frequency of two values and aces are enough to phase 
        if int(combination[0]) + int(combination[1]) + len(ace_count) >= 8:
            match.append(int(combination[0]))
            match.append(int(combination[1]))
            break
            
    if match:
        set1_value = 0
        
        # checks what card value frequency have the same frequencies in 'match'
        for dic_key, dic_value in values.items():
            
            if len(match_values) == 2:
                break
                
            elif dic_value in match:
                # appends card value that has same frequency as in match   
                match_values.append(dic_key)
                
        # finds all cards in 'hand' with the same value in 'match_values'
        # and appends each card value to its own set
        for card in hand:
            
            if card[CARD_VALUE] in match_values:
                
                # first card to be appended to 'set1'
                if not set1:
                    set1.append(card)
                    set1_value = card[CARD_VALUE]
                    
                elif card[CARD_VALUE] == set1_value:
                    set1.append(card)
                # second card value in 'match_values', but not first card value  
                else:
                    set2.append(card)
        
        # goes through each set and ensures there are four cards 
        # while loops take too much memory
        if ace_count:
            if len(set1) < 4:
                set1.append(ace_count[0])
                ace_count.remove(ace_count[0])
                
        if ace_count:
            if len(set1) < 4:
                set1.append(ace_count[0])
                ace_count.remove(ace_count[0])
                
        if ace_count:
            if len(set2) < 4:
                set2.append(ace_count[0])
                ace_count.remove(ace_count[0])
                
        if ace_count:
            if len(set2) < 4:
                set2.append(ace_count[0])
                ace_count.remove(ace_count[0])
                
        if len(set1) == len(set2):
            completed.append(set1)
            completed.append(set2)
            return completed
    
    # appends to 'desired_card' all cards with keys from 'values'
    for dic_key in values.keys():
        for suits in 'CSHD':
            desired_cards.append(str(dic_key) + suits)
            
    return desired_cards


def phase5(hand, length=8, ace_counter=0):
    """ Accepts a list of cards (made up of value and suit), 'hand', and if 
    possible, returns one list of 'length' cards in order. If not, returns a 
    list of desired cards and duplicate cards. 'length' and 'ace_counter' 
    exclusive use for phase 7.
    """
    
    sorted_hand = set()
    # 'ordered_value' is a list of 12 'A', used to place values into 
    ordered_value = ['A'] * 12
    completed = []
    completed_value = []
    desired_cards = []
    duplicate = []
    
    # goes through all cards and adds values to 'sorted_hand' set
    for card in hand:
        
        if card[CARD_VALUE] in special_value:
            
            if str(special_value[card[CARD_VALUE]]) in sorted_hand:
                
                duplicate.append(card)
                hand.remove(card)
                
            sorted_hand.add(str(special_value[card[CARD_VALUE]]))
            
        elif card[CARD_VALUE] == 'A':
            ace_counter += 1
            
        else:
            if str(card[CARD_VALUE]) in sorted_hand:
                
                duplicate.append(card)
                hand.remove(card)
                
            sorted_hand.add(card[CARD_VALUE])
            
    # all unique values in 'hand', 'ordered_value' list is indexed 
    # example:sorted_hand = (2,3,5,8,10)
    # example:ordered_list = ['2','3','A','5','A','A','8','A','10','A','A','A']
    for value in sorted_hand:
        ordered_value[int(value) - 2] = value
    
    # ensures when looping through, wrap arounds can be looked into 
    ordered_value = ordered_value * 2
    
    # goes through 'ordered_list', slicing the list to match length value 
    # from index location. Then within that slice, adds all 'A's to 'a_count'
    for index in range(12):
        
        ordered_list = ordered_value[index: index + length]
        a_count = 0
        
        for value in ordered_list:
            if value == 'A':
                a_count += 1
        
        # checks if there are enough aces in hand to complete run of 8 cards
        if a_count <= ace_counter:
            # that sliced list is added to 'completed'
            completed = ordered_list
        
    if completed:
        # goes through each value in 'completed' and card in 'hand', to append
        # card to 'completed_values' in the same order. 
        for value in completed:
            for card in hand:
                # checks if value of card match the value in 'completed' 
                if value == card[CARD_VALUE]:
                    completed_value.append(card)
                    hand.remove(card)
                    break
                    
                elif value == 'A':
                    # for phase 7
                    if length == 4:
                        completed_value.append('ace')
                        hand.remove(card)
                        break
                        
                    elif card[CARD_VALUE] == 'A':
                        completed_value.append(card)
                        hand.remove(card)
                        break

                # appends useable version of special_values
                elif int(value) > 9:
                    if int(value) == 10 and card[CARD_VALUE] == '0':
                        completed_value.append('0' + card[CARD_SUIT])
                        hand.remove(card)
                        break
                    elif int(value) == 11 and card[CARD_VALUE] == 'J':
                        completed_value.append('J' + card[CARD_SUIT])
                        hand.remove(card)
                        break 
                    elif int(value) == 12 and card[CARD_VALUE] == 'Q':
                        completed_value.append('Q' + card[CARD_SUIT])
                        hand.remove(card)
                        break 
                    elif int(value) == 13 and card[CARD_VALUE] == 'K':
                        completed_value.append('K' + card[CARD_SUIT])
                        hand.remove(card)
                        break 
                        
        return completed_value
    else:
        
        non_duplicate_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 
                               'J', 'Q', 'K']
        # removes any values in 'non_duplicate_cards' if in 'sorted_hand'
        
        for value in sorted_hand:
            if int(value) == 10:
                non_duplicate_cards.remove('0')
                break
                
            elif int(value) == 11:
                non_duplicate_cards.remove('J')
                break
                
            elif int(value) == 12:
                non_duplicate_cards.remove('Q')
                break
                
            elif int(value) == 13:
                non_duplicate_cards.remove('K')
                break
                
            else:
                non_duplicate_cards.remove(value)
                break
                
        # returns all desired_cards which are not duplicates       
        for value in non_duplicate_cards:
            for suit in 'CSHD':
                desired_cards.append(value + suit)
                
        # returns desired card and duplicate cards in 'hand'
        return (desired_cards, duplicate)

    
def phase6(hand):
    """ Accepts a list of cards (made up of value and suit), 'hand', and if 
    possible, returns two sets of cards of the same colour which sum up to 34
    in a list. If not, returns list of desired cards.
    """
    
    values = dd(list)
    match = []
    completed = []
    desired_cards = []
    
    # sets up 'values', where key is suit colour and value is list of cards
    for card in hand:
        
        if card[CARD_SUIT] in RED_SUIT:
            values[RED_SUIT].append(card)
            
        else:
            values[BLACK_SUIT].append(card)
    
    # checks if one suit can complete two sets 
    for dic_key, dic_value in values.items():
        check = phase3(dic_value)
        if len(check) == 2:
            return check
        
    # goes through each item in 'values' to find if phase is possible
    for dic_key, dic_value in values.items():
        string_value = ''
        # converts cards in 'values' value
        for value in dic_value:
            string_value += value[0] 
        
        # goes through the highest length of set1 to the lowest 3  
        for ran in range(len(string_value), 2, -1):
            
            # finds all combination of card value with the range
            for combination in combinations(string_value, ran):
                # breaks if a combination for that key has been found
                if values[dic_key] == 'Done':
                    break
                    
                total = sum_hand(combination)
                if total == 34:
                    set_card = []
                    # appends the value and colour as a string based on dic_key
                    for num in combination:
                        if dic_key == RED_SUIT:
                            set_card.append(num + 'red')
                        else:
                            set_card.append(num + 'black')
                            
                    match.append(set_card)
                    values[dic_key] = 'Done'
                    
                    break
   
    if len(match) < 2:
        # goes through 'values' items to find which colour did not sum up to 34
        for dic_key, dic_value in values.items():
            
            if dic_value != 'Done':
                
                for values in '234567890JQK':
                    
                    for suit in dic_key:
                        desired_cards.append(values + suit)
                        
        return desired_cards
 
    else:
        
        for sets in match:
            match_set = []
            # converts values in 'match' to cards in hand
            for value in sets:
                
                for cards in hand:
                    
                    if ('red' in value and cards[CARD_SUIT] in RED_SUIT and 
                        cards[CARD_VALUE] == value[CARD_VALUE]):
                        match_set.append(cards)
                        hand.remove(cards)
                        break
                        
                    elif ('black' in value and cards[CARD_SUIT] in BLACK_SUIT 
                          and cards[CARD_VALUE] == value[CARD_VALUE]):
                        match_set.append(cards)
                        hand.remove(cards)
                        break
                        
            completed.append(match_set)
            
        return completed

    
def phase7(hand):
    """ Accepts a list of cards (made up of value and suit), 'hand', and if 
    possible, returns two sets of four cards, one where there is a run of four 
    cards of the same colour and another of the same value in a list. If not, 
    returns list of desired cards.
    """
    
    values_suit = dd(list)
    values_hand = dd(int)
    ace_counter = 0
    set1 = []
    set2 = []
    set2_value = ''
    completed = []
    desired_cards = []
    
    # sets up 'values_suit' where key is suit colour and values are cards
    for card in hand:
        if card[CARD_VALUE] == 'A':
            ace_counter += 1
        elif card[CARD_SUIT] in RED_SUIT:
            values_suit[RED_SUIT].append(card)
        else:
            values_suit[BLACK_SUIT].append(card)
    
    # for run of cards, there can only be two values
    if ace_counter > 2:
        a_count = 2
    else:
        a_count = ace_counter

    # checks if there is a run of cards in the value of 'values'
    for dic_key, dic_value in values_suit.items():
        
        check = phase5(dic_value, length=4, ace_counter=a_count)
        
        if set1:
            break
        
        if len(check) == 4:
            # converts 'ace' to ace cards in hand and sets up 'set1'
            for card in check:
                
                if card == 'ace':
                    
                    for cards in hand:
                        
                        if cards[CARD_VALUE] == 'A':
                            set1.append(cards)
                            hand.remove(cards)
                            ace_counter -= 1
                            break
                            
                else:
                    set1.append(card)
                    hand.remove(card)
                    
    # sets up 'values_hand' without cards used to complete 'set1'              
    for card in hand:
        if card[CARD_VALUE] != 'A':
            values_hand[card[CARD_VALUE]] += 1
    
    # goes through all 'values_hand' items and tries to complete set2
    for dic_key, dic_value in values_hand.items():
        
        if dic_value >= 4:
            for card in hand:
                # sets set2 value when it is the first value, ensures one value
                if not set2 and card[CARD_VALUE] == dic_key:
                    set2.append(card)
                    set2_value = card[CARD_VALUE]
                    
                elif (card[CARD_VALUE] == dic_key and 
                      card[CARD_VALUE] == set2_value):
                    set2.append(card)

        elif dic_value == 3 and ace_counter >= 1:
            for card in hand:
                
                if not set2 and card[CARD_VALUE] == dic_key:
                    set2.append(card)
                    set2_value = card[CARD_VALUE]
                elif (card[CARD_VALUE] == dic_key and 
                      card[CARD_VALUE] == set2_value):
                    set2.append(card)


        elif dic_value == 2 and ace_counter >= 2:
            
            for card in hand:
                
                if not set2 and card[CARD_VALUE] == dic_key:
                    set2.append(card)
                    set2_value = card[CARD_VALUE]
                elif (card[CARD_VALUE] == dic_key and 
                      card[CARD_VALUE] == set2_value):
                    set2.append(card)
                    
    # adds aces from hand to ensure 4 cards in set2
    # could have used while loop, took too much memory
    if set2:
        if len(set2) < 4:
            for card in hand:
                if card[CARD_VALUE] == 'A':
                    set2.append(card)
                    hand.remove(card)
                    break
        if len(set2) < 4:
            for card in hand:
                if card[CARD_VALUE] == 'A':
                    set2.append(card)
                    hand.remove(card)
                    break
    
    else:
        # appends desired_values for set2 which have dic_value of 3 
        for dic_key, dic_value in values_hand.items():
            set_value = []
            
            if dic_value == 3:
                for suit in 'CSHD':
                    set_value.append(str(dic_key) + suit)
                    
            desired_cards += set_value
            
    # when both are comlpeted        
    if set1 and set2:
        completed.append(set1)
        completed.append(set2)
        return completed
    
    else:
        if desired_cards:
            return desired_cards
        else:
            return 'Anything'
       
    
def table_play(table, hand):
    """ Accepts a list of each phase play in form 2-tuple, 'table', and all 
    cards in hand, 'hand'. Which returns a 2-tuple of information about the 
    play if possible to complete. Else return none.
    """
    
    # the player the phase is being looked at 
    player = -1
    # goes through each phases on table and checks which can be added to  
    for phases in table:
        player += 1
        
        phase = phases[PHASE]
        content = phases[CONTENT]
        
        # when phase 1 or 4, checks if cards in hand share same values on table
        if phase == 1 or phase == 4:
            # goes through both set2
            for index in range(len(content)):
                # finds base value for that set, ignore aces
                for card in content[index]:
                    if card[CARD_VALUE] != 'A':
                        base_value = card[CARD_VALUE]
                        break
                        
                for card in hand:
                    if (card[CARD_VALUE] == 'A' or 
                        card[CARD_VALUE] == base_value):
                        return(4, (card, (player, index, len(content[index]))))
                    
        # when phase 2, checks if cards in hand share same suit on table
        elif phase == 2:
            # finds shared suit
            for card in content[0]:
                if card[CARD_VALUE] != 'A':
                    base_suit = card[CARD_SUIT]
                    break
                    
            for card in hand:
                if card[CARD_VALUE] == 'A' or card[CARD_SUIT] == base_suit:
                    return(4, (card, (player, 0, len(content))))    
        
        # when phase 3, checks if cards in hand can add to sum of table cards
        elif phase == 3:
            # goes through both sets in 'content'
            for index in range(len(content)):
                
                string_value_content = ''
                string_value_hand = ''
                # finds string value for both hand and content
                for cards in content[index]:
                    string_value_content += cards[CARD_VALUE]
                    
                for cards in hand:
                    string_value_hand += cards[CARD_VALUE]

                # total that is on the board now
                total = sum_hand(string_value_content)
                fibonacci_sum = [34, 55, 68, 76, 81, 84, 86, 87]
                # finds the value to end the turn with 
                for value in fibonacci_sum:
                    if total < value:
                        fibonnaci_target = value
                        break
                        
                target_value = fibonnaci_target - total
                min_com = 1
                
                if target_value > 13:
                    min_com = 2
                
                # goes through each combination of varrying length to find 
                # combination which total up to 'target_value'
                for ran in range(len(string_value_hand), min_com -1, -1):
                    
                    for combination in combinations(string_value_hand, ran):
                        
                        string_com = ''
                        for letter in combination:
                            string_com += letter
                            
                        total_com = sum_hand(string_com)
                        
                        if total_com == target_value:
                            # goes through hand to find the card
                            for card in hand:
                                if card[CARD_VALUE] == combination[0]:
                                    return(4, (card, (player, index, 
                                                      len(content[index]))))
                                
        # when phase 5, checks if there is a continuance of sequence 
        elif phase == 5:
            
            ace_count = 0
            # the first non-ace value from the end
            for card in content[0][::-1]:
                if card[CARD_VALUE] != 'A':
                    last_card = card
                    break
                ace_count += 1
            
            # adds the integer value to 'last_card_value'
            if last_card[CARD_VALUE] in special_value:
                last_card_value = special_value[last_card[CARD_VALUE]] 
                
            else:
                last_card_value = last_card[CARD_VALUE] 
            
            # finds the integer value of the card that can add to the sequence
            desired_card = int(last_card_value) + 1 + ace_count
            
            # wrap arounds
            if desired_card > 13:
                desired_card -= 12
            
            # converts integer value back to a special value
            if desired_card in special_value.values():
                for dic_key, dic_value in special_value.items():
                    if desired_card == dic_value:
                        desired_card = dic_key
                        break
            
            # checks if any cards match the 'desired_card' value
            for card in hand:
                if (card[CARD_VALUE] == 'A' or 
                    card[CARD_VALUE] == str(desired_card)):
                    if len(content[0]) < 12:
                        return(4, (card, (player, 0, len(content[0]))))
        
        # when phase 6, checks if cards in hand can add to sum of the table 
        elif phase == 6:
            # goes through each set 
            for index in range(len(content)):
                
                string_value_content = ''
                string_value_hand = ''
                
                # finds the 'desired_suit' and sets up 'string_value_content'
                for card in content[index]:
                    string_value_content += card[CARD_VALUE]
                    if card[CARD_VALUE] != 'A':
                        if card[CARD_SUIT] in RED_SUIT:
                            desired_suit = RED_SUIT
                        else:
                            desired_suit = BLACK_SUIT
                
                # sets up 'string_value_hand' based on 'desired_suit'
                for card in hand:
                    if card[CARD_SUIT] in desired_suit:
                        string_value_hand += card[CARD_VALUE]
                
                # total that is on the board now
                total = sum_hand(string_value_content)
                fibonacci_sum = [34, 55, 68, 76, 81, 84, 86, 87]
                # finds the value to end the turn with 
                for value in fibonacci_sum:
                    if total < value:
                        fibonnaci_target = value
                        break
                        
                target_value = fibonnaci_target - total
                min_com = 1
                
                if target_value > 13:
                    min_com = 2
                
                # goes through each combination to see if any match the target
                for ran in range(len(string_value_hand), min_com -1, -1):
                    
                    for combination in combinations(string_value_hand, ran):
                        
                        string_com = ''
                        for letter in combination:
                            string_com += letter
                            
                        total_com = sum_hand(string_com)
                        
                        if total_com == target_value:
                            
                            for card in hand:
                                
                                if (card[CARD_VALUE] == combination[0] and
                                    card[CARD_SUIT] in desired_suit):
                                    return(4, (card, (player, index, 
                                                      len(content[index]))))
        # when phase 7, checks if card in hand can add to the run of set 1
        # with same colour or share same value as set 2
        elif phase == 7:
            for index in range(len(content)):
                if index == 0:
                    ace_count = 0
                    
                    # finds non-ace last card
                    for card in content[index][::-1]:
                        
                        if card[CARD_VALUE] != 'A':
                            last_card_value = card[CARD_VALUE]
                            last_card_suit = card[CARD_SUIT]
                            break
                            
                        ace_count += 1
                    
                    # converts it integer if special
                    if last_card_value in special_value:
                        last_card_value = special_value[last_card_value]
                    
                    # finds integer value of 'desired_card'
                    desired_card_value = int(last_card_value) + 1 + ace_count
                    
                    # converts for wrap arounds
                    if desired_card_value > 13:
                        desired_card_value -= 12
                    
                    # converts integer to special value
                    if desired_card_value in special_value.values():
                        
                        for dic_key, dic_value in special_value.items():
                            if desired_card_value == dic_value:
                                desired_card_value = dic_key
                                break
                                
                    if last_card_suit in RED_SUIT:
                        desired_card_suit = RED_SUIT
                    else:
                        desired_card_suit = BLACK_SUIT
                        
                    # finds cards which match desired value and suit
                    for card in hand:
                        
                        if card[CARD_VALUE] == 'A':
                            return(4, (card, (player, index, 
                                              len(content[index]))))
                        
                        elif (card[CARD_VALUE] == str(desired_card_value) and 
                              card[CARD_SUIT] in desired_card_suit):
                            
                            if len(content[index]) < 12:
                                return(4, (card, (player, index, 
                                                  len(content[index]))))
                            
                else:
                    # finds same value in set 2
                    for card in content[index]:
                        if card[CARD_VALUE] != 'A':
                            base_value = card[CARD_VALUE]
                            break
                    # checks if in hand there is a card with same value        
                    for card in hand:
                        if (card[CARD_VALUE] == 'A' or 
                            card[CARD_VALUE] == base_value):
                            return(4, (card, (player, index, 
                                              len(content[index]))))
                       
    
def phazed_play(player_id, table, turn_history, phase_status, hand, discard):
    """ Accepts a integer of the player's id, 'player_id', the state of the 
    phases played on the table, 'table', turn_history of all action within the 
    game, 'turn_history', a list of all players completed phases, 
    'phase_status', cards within the players hand, 'hand', and the face up
    card on the discard pile. Which returns the action that should be taken
    in the form of a 2-tuple.
    """
    max_priority = 3
    min_priority = 0
    desired_card = []
    discard_card = []
    completed = []
    actions_taken = 0
    copy_hand = hand.copy()
    # checks how many actions have been taken by the player for that turn
    if turn_history:
        if turn_history[-1][0] == player_id:
            actions_taken += len(turn_history[-1][1])
    # player can only have less then 10 cards when completed a phase that game
    if len(hand) < 10:
        completed_phase = True
    else:
        completed_phase = False
        
    # phase has not been completed
    if not completed_phase:
        # finds current phase the player needs to play for
        current_phase = phase_status[player_id] + 1
        
        # goes through what actions to be taken based on the phase
        if current_phase == 1:
            check = phase1(copy_hand)
            
            # finds cards to draw and dicard based on priority 
            if type(check) != list:
                
                for dic_key in check.keys():
                    if dic_key < max_priority:
                        max_priority = dic_key
                    if dic_key > min_priority:
                        min_priority = dic_key
                        
                for sets in check[max_priority]:
                    desired_card += sets
                    
                for sets in check[min_priority]:
                    discard_card += sets
                    
            else:
                # completed becomes the values of both sets to complete phase 1
                completed += check
                
        elif current_phase == 2:
            check = phase2(copy_hand)
            # can only have 7 if phase completed 
            if len(check) == 7:
                completed += check
                
            else:
                desired_card += check
                
        elif current_phase == 3:
            check = phase3(copy_hand)
            if len(check) == 2:
                completed += check
                
            else:
                desired_card += check    

        elif current_phase == 4:
            check = phase4(copy_hand)
            if len(check) == 2:
                completed += check
                
            else:
                desired_card += check
                
        elif current_phase == 5:
            check = phase5(copy_hand)
            if len(check) == 8:
                completed += check
                
            else:
                # discard_card are the duplicate cards
                desired_card += check[0]
                discard_card += check[1]
                
        elif current_phase == 6:
            check = phase6(copy_hand)
            if len(check) == 2:
                completed += check
                
            else:
                desired_card += check    
                
        elif current_phase == 7:
            check = phase7(copy_hand)
            if len(check) == 2:
                completed += check
                
            else:
                desired_card += check
    
    # the player has not drawn a card yet
    if actions_taken == 0:
        # first priority if discard card an ace 
        if discard[CARD_VALUE] == 'A':
            return (2, discard)
        
        # second priority if discard card in desired card
        elif discard in desired_card:
            return (2, discard)
        
        # draw from deck
        else:
            return (1, None)
        
    # a card has been drawn    
    elif actions_taken > 0:
        # phase is not completed for that game and can be completed
        if not completed_phase and completed:
            # goes through all phases to get phases in a specific format
            for phase in range(8):
                if current_phase == phase:
                    
                    if len(completed) != 2:
                        return(3, (phase, [completed]))
                    else:
                        return(3, (phase, completed))
                    
        # phase completed for that game, play for table 
        elif completed_phase:
            table_check = table_play(table, hand)
            
            if table_check:
                return(table_check)
            
            # discards the generally highest value card for end of game 
            else:
                return(5, hand[-1])
            
        else:
            # tries to discard non important cards
            if current_phase in (1, 5):
                copy_hand = hand.copy()
                for card in copy_hand:
                    if card in discard_card and card[CARD_VALUE] != 'A':
                        return(5, card)
                    
                # discards highest score cards besides aces
                for card in copy_hand[::-1]:
                    if card[CARD_VALUE] != 'A' and card not in desired_card:
                        return(5, card)
                    
            elif current_phase in (2, 3, 4, 6, 7):
                copy_hand = hand.copy()
                for card in copy_hand:
                    if card not in desired_card and card[CARD_VALUE] != 'A':
                        return(5, card)
                    
                copy_hand = hand.copy()
                for card in copy_hand[::-1]:
                    if card[CARD_VALUE] != 'A':
                        return(5, card)
