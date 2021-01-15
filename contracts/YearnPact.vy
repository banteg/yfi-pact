# @version 0.2.8
from vyper.interfaces import ERC20

interface YFI:
    def governance() -> address: view
    def mint(account: address, amount: uint256): nonpayable
    def addMinter(minter: address): nonpayable


# 3333 YFI over 5 years starting from YFI birthday
total: constant(uint256) = 3333 * 10 ** 18
start: constant(uint256) = 1597845648
duration: constant(uint256) = 5 * 365 * 86400

yfi: public(YFI)
signed: public(bool)
governance: public(address)
pending_governance: public(address)
minted: public(uint256)


@external
def __init__():
    self.governance = msg.sender
    self.yfi = YFI(0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e)


@external
def sign():
    assert not self.signed  # dev: pact signed
    assert self.yfi.governance() == self  # dev: pact not yfi governance
    self.yfi.addMinter(self)
    self.signed = True


@view
@internal
def _vested() -> uint256:
    return min(total, total * (block.timestamp - start) / duration)


@external
def mint(receiver: address = msg.sender, amount: uint256 = MAX_UINT256):
    assert msg.sender == self.governance  # dev: unauthorized
    tokens: uint256 = min(self._vested() - self.minted, amount)
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
    assert msg.sender == self.governance
    self.pending_governance = governance


@external
def accept_governance():
    assert msg.sender == self.pending_governance
    self.governance = msg.sender
    self.pending_governance = ZERO_ADDRESS
