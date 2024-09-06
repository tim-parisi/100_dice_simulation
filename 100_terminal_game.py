#!/usr/bin/python3
'''
100_terminal_game.py
A simple terminal-based version of the dice game 100
- Author: Tim Parisi
- Last Updated: 9/5/24
'''
import sys
import os
import random
import argparse

### GLOBALS

### METHODS

def roll_dice() -> tuple[int, int]:
    '''roll_dice: Simulates a dice roll and returns the rolled number'''
    return random.randint(1, 6), random.randint(1, 6)

def player_turn(player_score: int, player_number: int, highest_score: int, verbose: bool=True) -> int:
    '''player_turn: Prompts a user for their turn decisions and returns their total score at the end'''
    #Warning if a player has scored over 100
    if highest_score >= 100 and verbose:
        print(f'WARNING: A score of {highest_score} has been banked!')
    elif highest_score >= 100:
        print(f'{highest_score} max')
        
    if not verbose:
        print(f'Player {player_number+1}:')
        
    # Prompt user to roll
    round_score = 0
    user_roll = prompt_to_roll(player_number, verbose)
    
    # User roll
    while user_roll == True:
        dice_total = sum(roll_dice())
        if dice_total == 7:
            if verbose:
                print(f'You rolled a 7! You finished with {player_score} End of Turn')
            else:
                print(f'7|{player_score}')
            return player_score
        elif dice_total == 2:
            if verbose:
                print(f'Oh no! You rolled a 2! You finished with 0 End of Turn')
            else:
                print(f'2|0')
            return 0
        round_score += dice_total
        if verbose:
            print(f'You rolled a {dice_total}! Score: {round_score} | {round_score+player_score}')
        else:
            print(f'{dice_total}|{round_score}|{player_score + round_score}')
        user_roll = prompt_to_roll(player_number, verbose)
    if verbose:  
        print(f'You finished with {round_score + player_score}')
    else:
        print(f'{round_score + player_score}')
    return round_score + player_score

def prompt_to_roll(player_number: int, verbose: bool) -> bool:
    '''prompt_to_roll: Prompts user for their roll decision'''
    roll_choice = ''
    while not(roll_choice.lower() == 'y' or roll_choice.lower() == 'n'):
        if verbose:
            roll_choice = input(f'Player {player_number + 1}, would you like to roll? (Y/N) ')
        else:
            roll_choice = input('')
        if roll_choice.lower() == 'y':
            return True
        elif roll_choice.lower() == 'n':
            return False
        else:
            print(f'Unable to read input.')
        
def print_player_scores(player_scores: list[int], verbose: bool=True) -> None:
    '''prints the scores of all players in the game
    >>>print_player_scores([1, 3, 5], True)
    Player 1 has a score of 1
    Player 2 has a score of 3
    Player 3 has a score of 5
    '''
    for count, score in enumerate(player_scores, 1):
        print(f'Player {count} has a score of {score}')

def print_scorechart_info():
    print('''
The scorechart will usually have this format:
    Your roll | Your total for this round | Your total score if you end your turn
    
If you rolled a 7 or a 2, the scorechart will have this format:
    Your roll | Your end-of-round total''')
    sys.exit(0)

### MAIN
def main():
    #Input Argument Handling
    parser = argparse.ArgumentParser(description='A terminal verison of the dice game 100.')
    parser.add_argument('-q', '--quiet', help='Condenses a majority of the output text of the program', action='store_false')
    parser.add_argument('-p', '--players', help='Defines the amount of players in the game', type=int)
    parser.add_argument('-s', '--scorechart', help='Displays a score chart for how scoring is displayed in quiet mode', action='store_true')
    args = parser.parse_args()
    
    if args.scorechart:
        print_scorechart_info()
    
    #Setting Player Count
    if not args.players or args.players <= 0:
        player_count = input('How many players do you want? ')
        while True:
            try:
                player_count = int(player_count)
            except:
                player_count = input('Error: Invalid player count. Please try again: ')
            else:
                if player_count <= 0:
                    player_count = input('Error: Invalid player count. Please try again: ')
                    continue
                break
    else:
        player_count = args.players
    
    #Initializing data
    winning_player = 0
    max_score = 0
    player_scores = [0] * player_count
    turn_counter = 0
    
    #Regular Play (No one has scored 100 or more)
    while max_score < 100:
        p = turn_counter % player_count
        player_scores[p] = player_turn(player_scores[p], p, max_score, args.quiet)
        if player_scores[p] > max_score:
            max_score = player_scores[p]
            winning_player = turn_counter % player_count
        turn_counter += 1
    print_player_scores(player_scores, args.quiet)
    if args.quiet:
        print(f'The score has been set at {max_score} by player {(turn_counter-1)%player_count + 1}! 1 turn remaining for all other players:')
    else:
        print(f'{max_score} from {(turn_counter-1)%player_count + 1}')

    #Handling Final Turn
    winning_player = (turn_counter-1)%player_count
    for i in range(turn_counter, turn_counter + player_count - 1):
        p = turn_counter % player_count
        player_scores[p] = player_turn(player_scores[p], p, max_score, args.quiet)
        if player_scores[p] > max_score:
            max_score = player_scores[p]
            winning_player = turn_counter % player_count
        turn_counter += 1
    
    print(f"Player {winning_player + 1} wins!")
    
if __name__ == '__main__':
    main()