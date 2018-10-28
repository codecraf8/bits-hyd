import hashlib as hasher
import datetime as date
import sys

nonce = 0

class Block:
  def __init__(self, index, timestamp, data, previous_hash, nonce):
    self.index = index
    self.timestamp = timestamp
    self.data = data 
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
    self.nonce = nonce 
  
  def hash_block(self):
    sha = hasher.sha256()
    sha.update((str(self.index) + 
               str(self.timestamp) + 
               str(self.data) + 
               str(self.previous_hash)+
               hex(nonce)).encode('utf-8'))
    return sha.hexdigest()



#creating genesis Block
def create_genesis_block():
  return Block(0, date.datetime.now(), "Genesis Block", "0", 0) 
  #


#adding blocks one-by-one
def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = "Hey! I'm block " + str(this_index)
  this_hash = last_block.hash
  this_nonce = last_block.nonce
  return Block(this_index, this_timestamp, this_data, this_hash, nonce)


# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# How many blocks should we add to the chain
#  after the genesis block
num_of_blocks_to_add = 2


# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
  target_bits = 24
  maxint = 9223372036854775807
  target = 2 ** (256-target_bits)
  nonce = 0
  
  while nonce < maxint:
    block_to_add = next_block(previous_block)    
    
    if(int(block_to_add.hash, 16) < target):
      blockchain.append(block_to_add)
      previous_block = block_to_add
      
      break
    else:
      nonce = nonce + 1
  

  print("Block #{} has been added to the blockchain!".format(block_to_add.index))
  print("Previous Hash: {}".format(block_to_add.previous_hash))
  print("Hash: {}".format(block_to_add.hash)) 
  print("data: {}\n".format(block_to_add.data))
  print("nonce: {}\n".format(nonce))








