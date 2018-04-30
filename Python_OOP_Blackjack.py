from random import shuffle
import os
class Wallet():
    '''Class for managing the chips of the user.
    Attributes:
        balance: integer storing amount of chips on the wallet
    '''
    def __init__(self):
        self.balance=0
        self.deposit()
    
    def deposit(self):
        '''Asks the user to add  chips to the wallet, updates its balance.'''
        while True:
            try:
                chipsAdded=int(input(f'Enter the amount of chips to deposit. (Balance: {self.balance})'))
            except:
                print('There was an error, please try again.')
            else:
                if chipsAdded>=1:
                    print(f'You have successfully added {chipsAdded} to your wallet.\n')
                    break
                else:
                    print('You cannot add less than 1 chip.')
        self.balance+=chipsAdded
    
    def bet(self):
        '''Asks the user how much to bet.
        Returns:
            bet: An integer containing the amount to bet.
        '''
        while True:
            try:
                bet=int(input(f'Enter the amount to bet. (Balance: {self.balance}) (-1 to deposit more chips)'))
            except:
                print('There was an error, please try again.')
            else:
                if bet<=self.balance and bet>=1:
                    print(f"You've bet {bet}.\n")
                    return bet
                elif bet==-1:
                    self.deposit()
                else:
                    print('You may not have enough balance or you tried to bet less than 1.')
                    
    def updateBalance(self,result,bet):
        '''Updates the balance after a game. No output.
        Arguments:
            result: boolean representing wether the user has lost or won.
            bet: Integer containing the amount of chips the user bet.
        '''
        if result:
            self.balance+=bet
        else:
            self.balance-=bet
        
class Card():
    '''Class for comparing  and printing cards'''
    def __init__(self,suit,num,value):
        '''Initialize card instance.
        Arguments:
            suit: String representing suit of card.
            num: String representing number of card
            value: Integer representing the value of the card in the game.
        '''
        self.suit=suit
        self.num=num
        self.value=value
    def __str__(self):
        #Override for easier printing of the card.
        return f'{self.num} de {self.suit}'

    def __radd__(self, other):
        #Override for easier addition of cards
        return other + self.value
    
class Deck():
    '''Class for generating decks of cards and deal from them.
    Attributes:
        suits: List containing the suits.
        numValue: List containing tuples, which contain the number and value for each card.
        cards: List of card objects contained in deck
    '''
    suits=['Spades','Hearts','Clubs','Diamonds']
    numValue=[('Two',2),('Three',3),('Four',4),('Five',5),('Six',6),('Seven',7),('Eight',8),('Nine',9),('Ten',10),('Jack',10),('Queen',10),('King',10),('Ace',11)]
    
    def __init__(self):
        '''Initializes deck instance and shuffles the cards'''
        self.cards=[Card(suit,num,value) for suit in Deck.suits for num,value in Deck.numValue]
        shuffle(self.cards)
    
    def hit(self):
        '''Returns the last card in the deck''' 
        return self.cards.pop(-1)
        
class Hand():
    '''Manages players and dealers cards.
    Attributes:
        cards: List of cards.
        aces: Integer containing amount of aces.
        value: Integer containing the value of the hand.
    '''
    def __init__(self):
        '''Initializes an instance of a hand.'''
        self.cards=[]
        self.aces=0
        self.value=0
        
    def addCard(self,card):
        '''Adds a card and updates value of hand.
        Arguments:
            card: Card Object.
        '''
        self.cards.append(card)
        if card.value==11:
            self.aces+=1
        self.calculateValue()
        
    def calculateValue(self):
        '''Updates value of the hand'''
        value=sum(self.cards)
        contAces=self.aces
        while value>21 and contAces>0:
            value-=10
            contAces-=1
        self.value=value
    
    def __str__(self):
        #Override for easy printing
        stringCards='\n'
        for card in self.cards:
            stringCards+=card.__str__()+' | '
        stringCards+=f'\nValue: {self.value}\n' 
        return stringCards
    
class DealerHand(Hand):
    '''Represents dealer hand, inherits Hand class, used to override string representation and add a method.'''
    def __str__(self):
        #Override for easy printing
        return f'{self.cards[1]} \nValue: {self.cards[1].value}\n'
    
    def printAll(self):
        '''Prints all the cards in the hand'''
        stringCards='Dealer: \n'
        for card in self.cards:
            stringCards+=card.__str__()+' | '
        print(stringCards+f'\nValue: {self.value}\n')
        
def hitOrStay():
    '''Asks the user whether they want to stay (stop dealing cards) or hit (get one more card)
    Return:
        answer: Character containing the answer (s/h is stay/hit)
    '''
    while True: 
        answer=input('Enter "h" to hit, "s" to stay:\n')
        if answer.lower()=='h' or answer.lower()=='s':
            return answer.lower()
        else:
            print('There was an error, please try again.')
            
def replay():
    '''Asks whether the user wants to keep playing
    Returns:
        boolean: true represents continue, false represents stop playing
    '''
    while True:
        answer=input('Do you want to play again? (Y/N)')
        if answer.lower() =='y':
            return True
        elif answer.lower()=='n':
            return False
        else:
            print('There was an error, please try again.')

if __name__ == '__main__':
    print('\nWelcome to BlackJack!\n')
    #Initialize wallet.
    wallet=Wallet()
while True:
    #Initialize deck, player hand and dealer hand.
    deck=Deck()
    playerHand=Hand()
    dealerHand=DealerHand()
    #Ask user how much to bet.
    bet=wallet.bet()
    os.system('cls' if os.name == 'nt' else 'clear')
    #Deal cards to both dealer and player and show them.
    playerHand.addCard(deck.hit())
    dealerHand.addCard(deck.hit())
    playerHand.addCard(deck.hit())
    dealerHand.addCard(deck.hit())
    print(f'Dealer: {dealerHand}')
    print(f'Player: {playerHand}Bet: {bet}')
    playerHasBusted=False
    #While player wants to hit, keep dealing cards unless player busts.
    while hitOrStay()=='h':
        os.system('cls' if os.name == 'nt' else 'clear')
        playerHand.addCard(deck.hit())
        print(f'Dealer: {dealerHand}')
        print(f'Player: {playerHand}Bet: {bet}')
        if playerHand.value>21:
            #If value is greater than 21 player looses its bet, game is over.
            print(f'Player: {playerHand}')
            wallet.updateBalance(False,bet)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"You've busted, you lost {bet} so your current balance is {wallet.balance}")
            playerHasBusted=True
            break

    #Check whether player has busted, deal cards to dealer until its hand value is equal or greater than 17.        
    if not playerHasBusted:
        while dealerHand.value<=17:
            dealerHand.addCard(deck.hit())
        
        os.system('cls' if os.name == 'nt' else 'clear')
        #Print all cards from dealer.
        dealerHand.printAll()
        print(f'Player: {playerHand}Bet: {bet}\n')
        #Check who has won modify wallet accordingly.
        if dealerHand.value>21 or playerHand.value>=dealerHand.value:
            wallet.updateBalance(True,bet)
            print(f'Congratulations, you won the game! You receive {bet}, so your current balance is {wallet.balance}')
        else:
            wallet.updateBalance(False,bet)
            print(f"You've lost the game, you loose {bet}, so your current balance is  {wallet.balance}")

    #Ask whether player wants to play again, if not, program stops its execution
    if not replay():
        break
    os.system('cls' if os.name == 'nt' else 'clear')
