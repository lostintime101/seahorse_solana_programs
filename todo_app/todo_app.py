
from seahorse.prelude import *

declare_id('')

class UserProfile(Account):
  owner: Pubkey
  last_todo: u8

class TodoAccount(Account):
  owner: Pubkey
  index: u8
  todo: str
  done: bool


@instruction
def init_user_profile(owner: Signer, user_profile: Empty[UserProfile]):
  
  user_profile = user_profile.init(
    payer = owner,
    seeds = ['user_profile',owner])
  
  user_profile.owner = owner.key()
  user_profile.last_todo = 0


@instruction
def add_task(
  owner: Signer,
  user_profile: UserProfile,
  todo_account: Empty[TodoAccount], 
  todo: str
  ):
  
  todo_account = todo_account.init(
    payer = owner,
    seeds = ['todo_account', owner, user_profile.last_todo]
  )
  
  todo_account.todo = todo
  todo_account.index = user_profile.last_todo
  todo_account.owner = owner.key()
  user_profile.last_todo += 1


@instruction
def mark_task_as_done(
  owner: Signer,
  todo_account: TodoAccount
  ):

  assert owner.key() == todo_account.owner, 'Only the owner of the task can mark as done'
  
  todo_account.done = True
  
  print('This todo has been marked as done')
