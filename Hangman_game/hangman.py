import requests
import random




class Players:
    players_registered = []

    def __init__(self):
        self.name = input('please give me your name:')
        self.word = self.chose_word()
        self.guesses = len(self.word )
        Players.players_registered.append(self)
        self.__status  = 'player'
        self.correct_character = 0
        self.all_guesses = []
    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self,label):
        self.__status = label
    @classmethod
    def del_player(cls,player):
        cls.players_registered.remove(player)

    def chose_word(self):
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site)
        words = response.content.splitlines()
        words = [word for word in words if len(word)>5]
        random_word = random.choice(words).decode('utf-8') 
        return random_word
    
class GameController():
    Ranking = {}
    def __init__(self) :
        while True:
            if len(Players.players_registered) == 0:
                print(GameController.Ranking)
                break
            for player in Players.players_registered:
                if player.guesses >0 :
                    print(f'player is {player.name}')
                    
                    guess = input('give me your guess or word\n')
                    while guess in player.all_guesses:
                        guess = input('give me another character\n')

                    if guess != 'word' :
                        player.guesses -=1
                        print(f'remaining guesses is {player.guesses}')
                        player.all_guesses.append(guess)
                        positions =[]
                        for index, i in enumerate(player.word,1):
                            if i == guess:
                                positions.append(index)
                                player.correct_character +=1
                        print(f'the position of your guess is {positions}')        
                        print(f'correct characters is {player.correct_character}')
                        if player.correct_character == len(player.word):
                            player.status = 'winner'
                            print(f'{player.name} win and the word is {player.word}')
                            GameController.make_ranking(player)
                            Players.del_player(player)

                    elif guess == 'word' and player.guesses >0:
                        player.guesses -=1
                        print(f'remaining guesses is {player.guesses}')
                        suggested_word = input('give me your word\n')
                        if suggested_word == player.word:
                            player.status = 'winner'
                            print(f'{player.name} win and the word is {player.word}')
                            GameController.make_ranking(player)
                            Players.del_player(player)
                        else :
                            print('wrong answer')
                elif player.guesses ==0:
                    player.status = 'losser'
                    print(f'game over the word was {player.word}')
                    GameController.make_ranking(player)
                    Players.del_player(player)
    @classmethod
    def make_ranking(cls,name):
        cls.Ranking[name.name] = name.status
                    


while True:
    order = input('what do you want to do:\n')
    if order == 'register':
        Players()
        
    elif order == 'start':
        GameController()
        break
    else:
        break
        
