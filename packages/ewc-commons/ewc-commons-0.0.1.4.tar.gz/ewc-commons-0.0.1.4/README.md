# EWC Commons Library #

A collection of common & useful things to make other things easier.

```bash
$ pip install ewc-commons[dev]
```


### Getting Started ###

* Dice Module
* Card Deck Module

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Dice Module ###
```python
from ewccommons.dice import roll_d6, D4, Dice

# Just roll a standard D6 die
roll:int = roll_d6()
# Create a 4 sided named Dice object
dice:Dice = Dice(name="Piramid", sides=D4, val=None)
# Returns a new die roll
dice_roll:int = dice.roll()
# Returns the last rolled value
dice_rolled:int = dice.rolled()
```

### Card Deck Module ###
```python
from ewccommons.carddeck import (
    _Deck_,
    _Hand_,
    shuffle_deck,
    draw_card,
    new_deck,
    new_shuffled_deck,
)
        
deck: _Deck_ = new_deck()
shuffled_deck: _Deck_ = shuffle_deck(deck)
# alternitively create a new shuffled deck
shuffled_deck_alt: _Deck_ = new_shuffled_deck()

hand_size:int = 5
drawn: _Hand_
deck_remaining:_Deck_
drawn, deck_remaining = draw_card(deck=shuffled_deck, cards=hand_size)

```
### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact