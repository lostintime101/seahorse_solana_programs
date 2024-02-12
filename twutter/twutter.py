
from seahorse.prelude import *

declare_id('')

TWEET_SIZE = 8 + 32 + 8 + 4 + 128 + 4 + 256 # 440

class UserAccount(Account):
  user_name: str
  owner: Pubkey
  last_tweet_id: u64

class Tweet(Account):
  owner: Pubkey
  tweet_id: u64
  text: str
  image: str
  like_count: u64

class Like(Account):
  tweet_owner: Pubkey
  tweet_id: u64
  liker: Pubkey


@instruction
def create_new_user_account(
  owner: Signer, 
  user: Empty[UserAccount], 
  name: str
  ):
  
  account = user.init(
    payer = owner,
    seeds = ['user-account', owner]
  )

  account.user_name = name
  account.owner = owner.key()
  
  print(f'{owner.key()} created a new user account {account.key()} with user name of {account.user_name}')
  
@instruction
def create_new_tweet(
  owner: Signer,
  user: UserAccount,
  tweet: Empty[Tweet],
  text: str,
  image: str
  ):

  assert user.owner == owner.key(), "Signer is not the user account owner"
  
  user.last_tweet_id += 1
  tweet_id = user.last_tweet_id

  tweet = tweet.init(
    payer = owner,
    seeds = ['tweet', owner, tweet_id],
    space = TWEET_SIZE
  )
  
  tweet.owner = owner.key()
  tweet.text = text
  tweet.image = image
  tweet.tweet_id = user.last_tweet_id
  
  print(f'Tweet ID:{tweet_id}, text: {tweet.text}, image: {tweet.image}')

  event = EventNewTweet(tweet.owner, tweet.tweet_id)
  event.emit()


@instruction
def like_tweet(
  liker: Signer, 
  user: UserAccount, 
  tweet: Tweet, 
  like: Empty[Like]
  ):
  
  like_account = like.init(
    payer = liker,
    seeds = ['like', tweet.owner, tweet.tweet_id, liker],
  )
  
  like_account.tweet_owner = tweet.owner
  like_account.tweet_id = tweet.tweet_id
  like_account.liker = liker.key()

  tweet.like_count += 1
  
  print(f'Tweet ID:{tweet.tweet_id} by {tweet.owner} now has {tweet.like_count} likes.')
  
  event = EventLikeTweet(tweet.owner, tweet.tweet_id, tweet.like_count)
  event.emit()


@instruction
def delete_tweet(owner: Signer, tweet: Tweet):
  
  assert owner.key() == tweet.owner, "Signer is not the tweet owner"

  tweet.transfer_lamports(owner, rent_exempt_lamports(TWEET_SIZE))

  event = EventDeleteTweet(tweet.owner, tweet.tweet_id)
  event.emit()


# Calculates rent from account size
def rent_exempt_lamports(size: u64) -> u64:
  return 897840 + 6960 * (size - 1)


class EventNewTweet(Event):
  owner: Pubkey
  id: u64

  def __init__(self, owner: Pubkey, id: u64):
    self.owner = owner
    self.id = id

class EventLikeTweet(Event):
  owner: Pubkey
  id: u64
  like_count: u64

  def __init__(self, owner: Pubkey, id: u64, like_count: u64):
    self.owner = owner
    self.id = id
    self.like_count = like_count

class EventDeleteTweet(Event):
  owner: Pubkey
  id: u64

  def __init__(self, owner: Pubkey, id: u64):
    self.owner = owner
    self.id = id

