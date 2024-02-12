
from seahorse.prelude import *

declare_id('')

MAX_ENERGY = 5
TIME_TO_REFILL_ENERGY = 30

class PlayerData(Account):
  name: str
  level: u8
  xp: u64
  wood: u64
  energy: u64
  last_login: i64


@instruction
def init_player(signer: Signer, player: Empty[PlayerData], clock: Clock):

    player = player.init(
        payer = signer,
        seeds = ['player', signer]
    )

    player.energy = MAX_ENERGY
    player.last_login = clock.unix_timestamp()


@instruction
def chop_tree(signer: Signer, player: PlayerData, clock: Clock):

    update_energy(player, clock)

    assert player.energy > 0, 'Not Enough Energy'

    player.wood += 1
    player.energy -= 1

    print(f"You chopped a tree and got 1 wood. You have {player.wood} wood and {player.energy} energy left.")


def update_energy(player: PlayerData, clock:Clock):
    
    time_passed = clock.unix_timestamp() - player.last_login
    time_spent: i64 = 0

    print("time passed: ", time_passed)
    print("time to refill energy: ", TIME_TO_REFILL_ENERGY)

    while time_passed > TIME_TO_REFILL_ENERGY:
        player.energy += 1
        time_passed -= TIME_TO_REFILL_ENERGY
        time_spent += TIME_TO_REFILL_ENERGY

        if player.energy == MAX_ENERGY:
            break
    
    if player.energy >= MAX_ENERGY:
        player.last_login = clock.unix_timestamp()
    else:
        player.last_login += time_spent
