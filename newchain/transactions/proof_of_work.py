import hashlib as hasher

target_bits = 16

class ProofOfWork:
    def __init__(self, block, target):
        self.block = block
        self.target = target

    def run(self):
        maxint = 9223372036854775807
        nonce = 0

        print("Mining new block ")

        sha = hasher.sha256()

        while nonce < maxint:
            print(f"\r{nonce}", end='')
            self.block.nonce = nonce
            hash = self.block.hash_block()

            if(int(hash, 16) < self.target):
                break
            else:
                nonce = nonce + 1
        print()
        return nonce , hash


def NewProofOfWork(block):
    target = 2 ** (256-target_bits)
    pow = ProofOfWork(block, target)
    return pow
