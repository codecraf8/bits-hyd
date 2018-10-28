## Installation 

pip install vyper 

## Running a script 

vyper yourFileName.vy


vyper -f ['abi', 'abi_python', 'bytecode', 'bytecode_runtime', 'ir', 'asm'] yourFileName.vy


## Deploymnet 

- deploy it with current browser on myetherwallet contract menu.

- Truper helps integrate with Truffle ecosystem - https://github.com/maurelian/truper

## Structure 

#### State Variables 

- values permanently stored in the contract 
- come in all shapes and textures 

#### Functions 

- executable units of code within a contract 
- Default function : that would run if all fails. 
- public / private function : depending upon visibility
- @payable - that would trigger exchanges, consumes more than 2300 gas

    Payment: event({amount: int128, from: indexed(address)})

		@public
		@payable
		def __default__():
		    log.Payment(msg.value, msg.sender)

#### Events 

- logs of functions which can be indexed and searched by clients of all sorts. 

		Payment: event({amount: int128, arg2: indexed(address)})

		total_paid: int128

		@public
		@payable
		def pay():
		    self.total_paid += msg.value
		    log.Payment(msg.value, msg.sender)

#### Sample Script 

		# Open Auction
		# Auction params
		# Beneficiary receives money from the highest bidder
		beneficiary: public(address)
		auctionStart: public(timestamp)
		auctionEnd: public(timestamp)

		# Current state of auction
		highestBidder: public(address)
		highestBid: public(wei_value)

		# Set to true at the end, disallows any change
		ended: public(bool)

		# Create a simple auction with `_bidding_time`
		# seconds bidding time on behalf of the
		# beneficiary address `_beneficiary`.
		@public
		def __init__(_beneficiary: address, _bidding_time: timedelta):
		    self.beneficiary = _beneficiary
		    self.auctionStart = block.timestamp
		    self.auctionEnd = self.auctionStart + _bidding_time

		# Bid on the auction with the value sent
		# together with this transaction.
		# The value will only be refunded if the
		# auction is not won.
		@public
		@payable
		def bid():
		    # Check if bidding period is over.
		    assert block.timestamp < self.auctionEnd
		    # Check if bid is high enough
		    assert msg.value > self.highestBid
		    if not self.highestBid == 0:
		        # Sends money back to the previous highest bidder
		        send(self.highestBidder, self.highestBid)
		    self.highestBidder = msg.sender
		    self.highestBid = msg.value


		# End the auction and send the highest bid
		# to the beneficiary.
		@public
		def endAuction():

		    # 1. Conditions
		    # Check if auction endtime has been reached
		    assert block.timestamp >= self.auctionEnd
		    # Check if this function has already been called
		    assert not self.ended

		    # 2. Effects
		    self.ended = True

		    # 3. Interaction
		    send(self.beneficiary, self.highestBid)		    	