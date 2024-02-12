from seahorse.prelude import *

declare_id('HHQoyeYQFsgy2Uqv75Qm26m67Aoh3bVTbhpav1xtm6iD')

class GameState(Enum):
  Game = 0
  Player1Wins = 1
  Player2Wins = 2
  Draw = 3

class Game(Account):
  players: Array[Pubkey,2]
  grid: Array[u8,9]
  game_status: u8
  curr_player: u8


@instruction
def init_game(owner: Signer, player1: Pubkey, player2: Pubkey, game: Empty[Game]):
  game = game.init(
    payer = owner,
    seeds = ['ttt', owner]
  )
  game.players[0] = player1
  game.players[1] = player2
  game.game_status = 0
  game.curr_player = 1


def win_check(grid: Array[u8,9], player: u8)-> GameState:

  # check for 8 possible win conditions
  if((grid[0] == player and grid[1] == player and grid[2] == player) or
    (grid[0] == player and grid[3] == player and grid[6] == player) or
    (grid[6] == player and grid[7] == player and grid[8] == player) or
    (grid[2] == player and grid[5] == player and grid[8] == player) or
    (grid[0] == player and grid[4] == player and grid[8] == player) or
    (grid[2] == player and grid[4] == player and grid[6] == player) or
    (grid[1] == player and grid[4] == player and grid[7] == player) or
    (grid[3] == player and grid[4] == player and grid[5] == player)):
 
    if player == 1:
      return GameState.Player1Wins
    else:
      return GameState.Player2Wins

  # check for full board i.e. draw
  for i in range(9):
    if grid[i] == 0:
        return GameState.Game

  return GameState.Draw


@instruction
def play_game(player:Signer, game_data:Game, played_by:u8, move_position:u8):
   
  # check the game is active
  assert game_data.game_status == 0, 'This game is already finished'

  # check for valid signer
  assert game_data.players[played_by-1] == player.key(), 'Invalid Signer'
   
  # check the correct player is taking their turn
  assert played_by == game_data.curr_player, 'Invalid Player'

  # check that move is possible
  assert move_position > 0 and move_position < 10, 'Invalid move, off the grid'
   
  # check that grid position is unoccupied
  assert game_data.grid[move_position - 1] == 0, 'Invalid move, position occupied'

  move_position -= 1
 
  game_data.grid[move_position] = game_data.curr_player
   
  game_status = win_check(Array(game_data.grid, len = 9), game_data.curr_player)

  if game_data.curr_player == 2:
    game_data.curr_player = 1
  else:
    game_data.curr_player = 2

  if(game_status == GameState.Game):
    print("Ready for next move")
   
  if(game_status == GameState.Player1Wins):
    game_data.game_status=1
    print("Player1 wins")
   
  if(game_status == GameState.Player2Wins):
    game_data.game_status=2
    print("Player2 wins")
   
  if(game_status == GameState.Draw):
    game_data.game_status=3
    print("Draw")
