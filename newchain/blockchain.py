import hashlib as hasher
from datetime import datetime
from proof_of_work import NewProofOfWork
import persistence as persist
import cli
import transactions
import sys

class Block:
    def __init__(self, timestamp, transactions, previous_hash, hash=None, nonce=None):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = hash
        self.nonce = nonce
        
    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.timestamp) + 
                str(self.transactions) + 
                str(self.previous_hash) + 
                str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()


def new_block(transactions, prev_block_hash):
    block = Block(datetime.now(), transactions, prev_block_hash)

    pow = NewProofOfWork(block)
    nonce, hash = pow.run()

    block.hash = hash
    block.nonce = nonce
    return block


def create_genesis_block(transactions):
    block = new_block(transactions, "0") 
    return block


class BlockChain:
    def __init__(self, address):
        "Creating block chain"
        self.blocks = [ create_genesis_block([transactions.NewCoinbaseTX(address)]) ]
    
    def mine_block(self, transactions):
        prev_block = self.blocks[-1]
        next_block = new_block(transactions, prev_block.hash)
        self.blocks.append(next_block)

    def FindUnspentTransactions(self, address):
        unspent_txs = []
        spent_txos = dict()

        for block in self.blocks:
            for transaction in block.transactions:
                # if transaction.is_coinbase() == False:
                for vin in transaction.Vin:
                    if vin.CanUnlockOutputWith(address):
                        tid = str(vin.Txid)
                        if tid in spent_txos:
                            spent_txos[tid].append(vin.Vout)
                        else:
                            spent_txos[tid] = [vin.Vout]

        for block in self.blocks:
            for transaction in block.transactions:
                txID = str(transaction.ID)

                for i, vout in enumerate(transaction.Vout):
                    if vout.CanBeUnlockedWith(address):
                        # Was the output spent?                    
                        if txID in spent_txos and i in spent_txos[txID]:
                            break
                        else:
                            unspent_txs.append(transaction)

        return unspent_txs

    # FindUTXO finds and returns all unspent transaction outputs
    def FindUTXO(self, address):
        UTXOs = []
        unspentTransactions = self.FindUnspentTransactions(address)
        for tx in unspentTransactions:
            for out in tx.Vout:
                if out.CanBeUnlockedWith(address):
                    UTXOs.append(out)
        return UTXOs

    # FindSpendableOutputs finds and returns unspent outputs to reference in inputs
    def FindSpendableOutputs(self, address, amount):
        unspentOutputs = dict()
        unspentTXs = self.FindUnspentTransactions(address)
        accumulated = 0

        for tx in unspentTXs:
            txID = str(tx.ID)
            for outIdx, out in enumerate(tx.Vout):
                if out.CanBeUnlockedWith(address) and accumulated < amount:
                    accumulated += out.Value

                    if txID not in unspentOutputs:
                        unspentOutputs[txID] = [outIdx]
                    else:
                        unspentOutputs[txID].append(outIdx)

                    if accumulated >= amount:
                        return accumulated, unspentOutputs

        return accumulated, unspentOutputs

    def getBalance(self, address):
        balance = 0
        for out in self.FindUTXO(address):
            balance += out.Value
        
        return balance

    def send(self, sender, to, amount):
        tx = transactions.NewUTXOTransaction(sender, to, amount, self)
        if tx:
            self.mine_block([tx])
            print("Success!")

    def add_block(self, data):
        prev_block = self.blocks[-1]
        next_block = new_block(data, prev_block.hash)
        self.blocks.append(next_block)


if __name__ == '__main__': 
    blockchain = persist.load_chain()
    action, data = cli.get_args()

    # import ipdb; ipdb.set_trace()
    if not blockchain and action != 'createblockchain':
        print("Create blockchain first")
        sys.exit()

    if action == 'printchain':
        for block in blockchain.blocks:
            print("previous_hash: {}".format(block.previous_hash))
            print("Hash: {}".format(block.hash))
            print("Transactions: {}".format(block.transactions))
            print("Nonce: {}".format(block.nonce))
            print()
    elif action == 'addblock':
        blockchain.add_block(data['address'])
    elif action == 'createblockchain':
        blockchain = BlockChain(data['address'])
    elif action == 'getbalance':
        balance = blockchain.getBalance(data['address'])
        print("Balance at {0} is {1}".format(data['address'], balance))
    elif action == 'send':
        blockchain.send(data['from'], data['to'], data['amount'])

   
persist.save_chain(blockchain)
