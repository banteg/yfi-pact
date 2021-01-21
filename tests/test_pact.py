import brownie
from brownie import ZERO_ADDRESS


def test_migration_from_timelock(yfi, timelock, pact, chain, treasury):
    assert yfi.governance() == timelock
    timelock.setTargetGovernance(pact)

    # this line takes a very long time
    chain.mine(timelock.period())

    timelock.updateTargetGovernance()
    assert yfi.governance() == pact

    before = yfi.balanceOf(treasury)
    pact.brrr()

    assert yfi.totalSupply() == "36666 ether"
    assert yfi.balanceOf(treasury) - before == "6666 ether"

    with brownie.reverts("dev: not governance"):
        pact.brrr()

    assert yfi.governance() == ZERO_ADDRESS


def test_migration_fake_gov(yfi, a, pact, treasury):
    gov = a.at(yfi.governance(), force=True)
    yfi.setGovernance(pact, {"from": gov})
    before = yfi.balanceOf(treasury)

    pact.brrr()

    with brownie.reverts("dev: not governance"):
        pact.brrr()

    print("yfi supply", yfi.totalSupply().to("ether"))
    assert yfi.totalSupply() == "36666 ether"
    assert yfi.balanceOf(treasury) - before == "6666 ether"
    assert yfi.governance() == ZERO_ADDRESS
