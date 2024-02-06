
from seahorse.prelude import *

declare_id('5ajaF9o3dP1nw7A5uNhhXMG16Fb5QrS2aRrnLtFasdt4')


class LotteryAdmin(Account):
  admin_address: Pubkey
  winner_address: Pubkey
  user_count: u64
  winning_user: u64 # chosen by you 

class User(Account):
  user_address: Pubkey
  balance: u64
  

# Initialise the LotteryAdmin account
@instruction
def init_admin(owner: Signer, admin: Empty[LotteryAdmin], winner_random_num: u64):
  
  admin = admin.init(
    payer = owner, 
    seeds = ['admin',owner]
  )

  admin.admin_address = owner.key()
  admin.user_count = 0
  admin.winning_user = winner_random_num
  # winner_address not set


# Initialise the token mint for prize token
@instruction
def init_token_mint(signer: Signer, new_token_mint: Empty[TokenMint], admin: LotteryAdmin):
  
  assert(signer.key() == admin.admin_address), "Only Admin authorised to call this function"  
  
  new_token_mint.init(
    payer = signer,
    seeds = ['token-mint', signer],
    decimals = 4,
    authority = signer
  )


# Initialize LotteryAdmin's prize token account
@instruction
def init_admin_token_account(signer: Signer, admin_token_acc: Empty[TokenAccount], mint: TokenMint):
    
  admin_token_acc.init(
    payer = signer, 
    seeds = ['admin-token-acc', signer], 
    mint = mint, 
    authority = signer
  )


# Mint prize tokens to Admin's account
@instruction
def mint_tokens_to_admin(signer: Signer, mint: TokenMint, recipient: TokenAccount, admin:LotteryAdmin):

  assert(signer.key() == admin.admin_address), "Only Admin authorised to call this function"
  
  mint.mint(
    authority = signer,
    to = recipient,
    amount = 10_000
  )


# Initialize User's account 
@instruction
def init_user(owner: Signer, user: Empty[User]):
  
  user = user.init(
    payer=owner,
    seeds = ['user',owner]
  )
  
  user.user_address = owner.key()


# User enters lottery by generating a prize token account
@instruction
def user_enters_lottery(signer: Signer, user: User, admin: LotteryAdmin, user_token: Empty[TokenAccount], mint: TokenMint):  
  
  user_token.init(
    payer = signer, 
    seeds = ['Token', signer],
    mint = mint, 
    authority = signer
  )   

  admin.user_count += 1
  
  if(admin.user_count == admin.winning_user):
    admin.winner_address = user.user_address
    

# Check to see if user has won
@instruction
def check_winner(signer: Signer, user: User, admin: LotteryAdmin, user_token: TokenAccount, admin_token: TokenAccount):
  
  assert(signer.key() == admin.admin_address), "Only Admin authorised to call this function"
                   
  if(user.user_address == admin.winner_address):
    
    print("Congrats you've won the lottery!")

    # 90% distributed to winner, 10% retained by admin
    admin_token.transfer( 
        authority = signer, 
        to = user_token, 
        amount = 9_000)

    user.balance += 9_000
  
  else:
    print("Sorry, you did not win. Try again next time.")
  

