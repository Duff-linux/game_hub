import random

words = ['patience', 'football', 'car', 'girl', 'many']

word = random.choice(words).upper()

letters = [l for l in word]

won = False
hunged = 0

solution = ['' for l in letters]


def add_letter(guess):
    for i, l in list(enumerate(letters)):
        if guess == l:
            solution [i] = l
    
    print(solution)

    
def main():
    while hunged < 6 and not won:

        player_input = input('guess a letter: ').upper()
        
        if player_input in letters:
            add_letter(player_input)
            if solution == letters:
                won = True
        else:
            hunged += 1
            print('wrong guess!, try again', hunged)


        if hunged == 6:
            print("Your're dead!")
            break
        
        elif won:
            print(word, "is the right word!")
            break

if __name__ == '__main__':
    main()