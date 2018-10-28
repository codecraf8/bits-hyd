import hashlib as hasher
subsidy = 50

class Transaction:
    def __init__(self, tid, vin, vout):
        self.ID = tid
        self.Vin = vin
        self.Vout = vout

    def SetID(self):
        sha = hasher.sha256()
        sha.update((str(self.ID) + str(self.Vin) + str(self.Vout)).encode('utf-8'))
        self.ID = sha.hexdigest()
    
    def is_coinbase(self):
        return len(self.Vin) == 1 and self.Vin[0].Txid == 0 and self.Vin[0].Vout == -1


class TXInput:
    def __init__(self, txid, vout, scriptSig):
        self.Txid = txid
        self.Vout = vout
        self.ScriptSig = scriptSig

    # CanUnlockOutputWith checks whether the address initiated the transaction
    def CanUnlockOutputWith(self, unlockingData):
        return self.ScriptSig == unlockingData


class TXOutput:
    def __init__(self, value, scriptPubKey):
        self.Value = value
        self.ScriptPubKey = scriptPubKey

    # CanBeUnlockedWith checks if the output can be unlocked with the provided data
    def CanBeUnlockedWith(self, unlockingData):
        return self.ScriptPubKey == unlockingData

# NewCoinbaseTX creates a new coinbase transaction
def NewCoinbaseTX(to, data=""):
    if data == "":
        data = "Reward to " + to

    txin = TXInput(0, -1, data)
    txout = TXOutput(subsidy, to)
    first_transaction = Transaction(0, [txin], [txout])
    first_transaction.SetID()

    return first_transaction


# NewUTXOTransaction creates a new transaction
def NewUTXOTransaction(sender, to, amount, blockchain):
    inputs = []
    outputs = []
    acc, validOutputs = blockchain.FindSpendableOutputs(sender, amount)

    if acc < amount:
        print("ERROR: Not enough funds")
        return None
        

    # Build a list of inputs
    for txid, outs in validOutputs.items():
        for out in outs:
            inputs.append(TXInput(txid, out, sender))

    # Build a list of outputs
    outputs.append(TXOutput(amount, to))

    if acc > amount:
        outputs.append(TXOutput(acc - amount, sender))

    tx = Transaction(None, inputs, outputs)
    tx.SetID()
    return tx
