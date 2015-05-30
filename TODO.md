
* Test-driven development of Blackjack model
  - basic logic, basic strategy action, dealer action
* Strategy pattern for action, counting, shuffling
* Configuration parser, echoed in command line options

* Pluggable human play supporting human input, basic strategy, and counting
* Simulation to test probabilities against empirical results
* Various shuffling algorithms
* Configurable options such as payout ratios, S17, surrender


* Integrated advice system for basic strategy, counting
* Various counting strategies
* GUI
* Markov learning deterministic process to online learn basic strategy
  - manipulate payout ratios, minimum bets, play policies to see how strategy changes


CLASSES

Basic
* Card
* HandInterface
* BlackjackHand
* Deck
* Shoe

Logic
* ActionStrategy
* ShufflerStrategy
* CountingStrategy
* HumanAction
* DealerAction
* HiLoCounting
* ShuffleTracking
* Action
* HitCommand
* SplitCommand
* DoubleCommand
* StandCommand
* SurrenderCommand
* EarlySurrenderCommand
* 

Game
* Player
* Dealer
* Bank
* Bankroll (players stack)
* Table
* 

Utilities
* Driver
  - command-line
* StrategyParser
* ConfigurationParser
* Logger

Simulation
* ...

GUI
* ...

MLDP
* ...

