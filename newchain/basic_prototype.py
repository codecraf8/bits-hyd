import hashlib as hasher
from datetime import datetime


class Block:
  def __init__(self, timestamp, data, previous_hash):
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()

  def hash_block(self):
    sha = hasher.sha256()
    sha.update((str(self.timestamp) + 
               str(self.data) + 
               str(self.previous_hash)).encode('utf-8'))
    return sha.hexdigest()


def new_block(data, prev_block_hash):
    timestamp = datetime.now()
    return Block(timestamp, data, prev_block_hash) 


def create_genesis_block():
  return new_block("Genesis Block", "0") 


class BlockChain:
    def __init__(self):
        self.blocks = [ create_genesis_block() ]
    
    def add_block(self, data):
        prev_block = self.blocks[-1]
        next_block = new_block(data, prev_block.hash)
        self.blocks.append(next_block)


if __name__ == '__main__':
    blockchain = BlockChain()
    blockchain.add_block("Send 1 BTC to Ivan")
    blockchain.add_block("Send 2 more BTC to Ivan")

    for block in blockchain.blocks:
        print("previous_hash: {}".format(block.previous_hash))
        print("Hash: {}".format(block.hash))
        print("Data: {}".format(block.data))
        print()
