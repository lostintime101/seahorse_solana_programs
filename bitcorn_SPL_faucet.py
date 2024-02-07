from seahorse.prelude import *
from seahorse.pyth import *

declare_id('fMX8bmgPgmcanxQJPJYgqoXAk4HExMAQ4uGexpLQZVN')

class BitcornFaucet(Account):
  bump: u8
  owner: Pubkey
  mint: Pubkey
  last_withdraw: i64
  

@instruction
def init_faucet(
    signer: Signer, 
    mint: TokenMint, 
    faucet: Empty[BitcornFaucet], 
    faucet_account: Empty[TokenAccount]):
  
  bump = faucet.bump()
  
  faucet = faucet.init(
    payer = signer,
    seeds = ['mint', mint]
  )

  faucet_account.init(
    payer = signer,
    seeds = ["token-seed", mint],
    mint = mint,
    authority = faucet,
  )
  
  faucet.bump = bump
  faucet.mint = mint.key()
  faucet.owner = signer.key()


# drips tokens based on the oracle price of BTC
@instruction
def drip_bitcorn_tokens(
    signer: Signer, 
    mint: TokenMint, 
    faucet: BitcornFaucet, 
    faucet_account: TokenAccount, 
    user_account: TokenAccount, 
    bitcoin_price_account: PriceAccount, 
    clock: Clock):
  
  timestamp: i64 = clock.unix_timestamp() 

  assert mint.key() == faucet.mint, 'Faucet token does not match the token provided'
  assert timestamp - 30 > faucet.last_withdraw, 'Please try again in 30 seconds'
  
  btc_price_feed = bitcoin_price_account.validate_price_feed('devnet-BTC/USD')
  btc_price = u64(btc_price_feed.get_price().price)
  btc_price = btc_price // 100_000_000  # converts to dollar units i.e. 4313965499999 -> 43,139
  
  print("The Bitcorn price is ", btc_price)
  
  thousand_bucks = 1000 * 1_000_000_000
  drip_amount = u64(thousand_bucks // btc_price)
  
  bump = faucet.bump

  faucet_account.transfer(
    authority = faucet,
    to = user_account,
    amount = u64(drip_amount),
    signer = ['mint', mint, bump]
  )


# send tokens back to replenish the faucet
@instruction
def replenish_bitcorn_tokens(
    signer: Signer, 
    mint: TokenMint, 
    user_account: TokenAccount, 
    faucet_account: 
    TokenAccount, 
    amount: u64):
  
  user_account.transfer(
    authority = signer,
    to = faucet_account,
    amount = u64(amount)
  )
