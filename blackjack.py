import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
flag =0

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    
    def __init__(self):
            # create Hand object
            
        self.hand = []	
        self.value = 0
            
    def __str__(self):
        pr = "Hand contains " 
        for i in range(len(self.hand)):
            pr = pr +self.hand[i].suit + self.hand[i].rank+" "
        return pr
            # return a string representation of a hand

    def add_card(self, card):
        self.hand.append(card)
        # add a card object to a hand

    def get_value(self):
        
        global flag
        self.value=0
        for i in self.hand:
            self.value = self.value+VALUES[i.rank]
            if(i.rank=='A'):
                flag=1
            #print VALUES[i.rank]
        
        if(flag==0):
                return self.value
            
        else:
                #print "Here"+ " "+str(self.value)
                if(self.value+10<=21):
                    return self.value+10
                else:
                    return self.value	
                
    # draw a hand on the canvas, use the draw method for cards            
    def draw(self, canvas, pos):
        for i in range(len(self.hand)):
            self.hand[i].draw(canvas,pos)
            pos[0]=pos[0]+ 100
 
# create a Deck object        
# define deck class 
class Deck:
    def __init__(self):
        self.deck=[]
        for i in SUITS:
            for j in RANKS:
             card = Card(i,j)
             self.deck.append(card) 

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()	# deal a card object from the deck
    
    def __str__(self):
        pr = "Deck contains "
        for i in range(len(self.deck)):# return a string representing the deck
            pr = pr +self.deck[i].suit + self.deck[i].rank+" "
        return pr

#define event handlers for buttons
def deal():
    global outcome, in_play,player_hand,dealer_hand, card_deck,score,outcome1,flag
    if(in_play==True):
        score = score-1
    flag=0
    card_deck= Deck()
    card_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(card_deck.deal_card())
    player_hand.add_card(card_deck.deal_card())
    dealer_hand.add_card(card_deck.deal_card())
    dealer_hand.add_card(card_deck.deal_card())
    
    
    outcome = "Hit or stand?"
    outcome1 = ""
    
    in_play = True

def hit():
    # replace with your code below
    global player_hand, card_deck,outcome, outcome1,in_play,score
    if(player_hand.get_value()<=21 and in_play):
        player_hand.add_card(card_deck.deal_card())
        if player_hand.get_value()>21 and in_play:
                outcome = "New deal?"
                outcome1 = "You went bust and lose"
                score = score-1
                in_play=False
       
def stand():
    # replace with your code below
    global player_hand, dealer_hand,outcome,score,in_play,outcome,outcome1
    if(player_hand.get_value()>21 ):
        outcome1 = "Already busted."
        
    else:
        while dealer_hand.get_value()<17 and in_play:
            dealer_hand.add_card(card_deck.deal_card())
        if(dealer_hand.get_value()>=17 and in_play):
            
            if(dealer_hand.get_value()>21) and in_play:
                score = score+1
                outcome1 = "Dealer busted. You win."
            elif(player_hand.get_value()<=dealer_hand.get_value() and in_play):
                score = score-1
                outcome1 = "You lose."
            elif(player_hand.get_value()>dealer_hand.get_value() and in_play):
                score = score+1
                outcome1 = "You win."
    outcome = "New deal?"
    in_play=False
   
# draw handler    
def reset_score():
    global score
    score = 0
    
def draw(canvas):
    global player_hand, dealer_hand,in_play,score,outcome,outcome1
    dealer_hand.draw(canvas,[80,200])
    if(in_play==True):
        canvas.draw_image(card_back, (36,48), CARD_SIZE, [80 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_SIZE)

    player_hand.draw(canvas,[80,380])
    canvas.draw_text("Blackjack",[90,100],50,"cyan")
    canvas.draw_text("Score " + str(score),[400,100],25,"black")
    canvas.draw_text("Dealer",[80,190],25,"Black")
    canvas.draw_text("Player",[80,370],25,"Black")
    canvas.draw_text(outcome,[250,370],25,"Black")
    canvas.draw_text(outcome1,[250,190],25,"Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Reset score", reset_score, 200)

frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
