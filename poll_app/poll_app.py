
from seahorse.prelude import *

declare_id('')

class Poll(Account):
  solana: u64
  ethereum: u64
  polygone: u64


@instruction
def create(user: Signer, poll: Empty[Poll]):
    poll = poll.init(payer=user)


@instruction
def vote(user: Signer, poll: Poll, vote_op: str):
    
    if vote_op == "solana":
        poll.solana += 1
    elif vote_op == "ethereum":
        poll.ethereum += 1
    elif vote_op == "polygone":
        poll.polygone += 1
    else:
        print("Sorry, this option does not exist")

