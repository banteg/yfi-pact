# @version 0.2.8
from vyper.interfaces import ERC20

interface YFI:
    def governance() -> address: view
    def mint(account: address, amount: uint256): nonpayable
    def addMinter(minter: address): nonpayable
    def removeMinter(minter: address): nonpayable
    def setGovernance(governance: address): nonpayable
    def transferFrom(sender: address, receiver: address, amount: uint256) -> bool: nonpayable


# 666 YFI per year starting from YFI birthday
rate: constant(uint256) = (666 * 10 ** 18) / (365 * 86400)
start: constant(uint256) = 1594972885

yfi: public(YFI)
signed: public(bool)
governance: public(address)
pending_governance: public(address)
minted: public(uint256)

# 3333 YFI must be sacrificed to break the pact
breakage: constant(uint256) = 3333 * 10 ** 18
broken: public(bool)
sacrificed: public(HashMap[address, uint256])


@external
def __init__():
    self.governance = msg.sender
    self.yfi = YFI(0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e)


@external
def sign_pact():
    assert not self.signed  # dev: pact signed
    assert self.yfi.governance() == self  # dev: pact not yfi governance
    self.yfi.addMinter(self)
    self.signed = True


@external
def break_pact(new_pact: address):
    assert self.signed  # dev: no pact signed
    assert not self.broken  # dev: pact already broken
    assert self.sacrificed[new_pact] >= breakage  # dev: not enough sacrificed
    self.yfi.removeMinter(self)
    self.yfi.setGovernance(new_pact)
    self.broken = True


@external
def tribute(new_pact: address, amount: uint256):
    assert self.signed  # dev: no pact signed
    assert not self.broken  # dev: pact already broken
    self.yfi.transferFrom(msg.sender, self, amount)
    self.sacrificed[new_pact] += amount


@view
@internal
def _vested() -> uint256:
    return rate * (block.timestamp - start)


@external
def mint(receiver: address = msg.sender, amount: uint256 = MAX_UINT256):
    assert msg.sender == self.governance  # dev: unauthorized
    tokens: uint256 = min(self._vested() - self.minted, amount)
    assert tokens > 0  # dev: not mintable
    self.yfi.mint(receiver, tokens)
    self.minted += tokens


@view
@external
def vested() -> uint256:
    return self._vested()


@view
@external
def mintable() -> uint256:
    return self._vested() - self.minted


@external
def set_governance(governance: address):
    assert msg.sender == self.governance  # dev: unauthorized
    self.pending_governance = governance


@external
def accept_governance():
    assert msg.sender == self.pending_governance  # dev: unauthorized
    self.governance = msg.sender
    self.pending_governance = ZERO_ADDRESS
