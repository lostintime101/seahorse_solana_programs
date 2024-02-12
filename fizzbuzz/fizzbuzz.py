
from seahorse.prelude import *

declare_id('')

class FizzBuzz(Account):
  fizz: bool
  buzz: bool
  n: u64


@instruction
def init(owner: Signer, fizzbuzz: Empty[FizzBuzz]):
    
  fizzbuzz.init(payer = owner, seeds = ['fizzbuzz', owner])


@instruction
def do_fizzbuzz(fizzbuzz: FizzBuzz, n: u64):
    
  fizzbuzz.fizz = n % 3 == 0
  fizzbuzz.buzz = n % 5 == 0
    
  if not fizzbuzz.fizz and not fizzbuzz.fuzz:
    fizzbuzz.n = n

