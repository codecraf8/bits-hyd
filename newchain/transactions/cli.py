import sys

def get_args():
    args = sys.argv
    if len(args) == 2 and args[1] == 'printchain':
        return 'printchain', None
    elif len(args) == 3:
        return args[1], { 'address' : args[2] }
        # if args[1] == 'addblock':
        #     return 'addblock', args[2]
        # elif args[1] == 'createblockchain':
        #     return 'createblockchain', args[2]
    elif len(args) == 5:
        return args[1], { 'from': args[2], 'to': args[3], 'amount': int(args[4]) }
    else:
        print(
            """
Usage: python blockchain.py option

options:
    createblockchain 'address'
    printchain
    addblock 'data'
    getbalance 'address'
    send 'from address' 'to address' amount
            """
        )
        return None, None
