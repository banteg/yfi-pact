import brownie


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

    with brownie.reverts("dev: already minted"):
        pact.brrr()

    # timelock has a bug which allows to bounce the pending governance back
    timelock.updateTargetGovernance()
    assert yfi.governance() == pact

    with brownie.reverts("dev: already minted"):
        pact.brrr()

    # pact can recover from this state by bouncing it back to timelock
    pact.revoke()
    assert yfi.governance() == timelock


def test_migration_fake_gov(yfi, a, pact, treasury):
    gov = a.at(yfi.governance(), force=True)
    yfi.setGovernance(pact, {"from": gov})
    before = yfi.balanceOf(treasury)

    with brownie.reverts("dev: not minted"):
        pact.revoke()

    pact.brrr()

    with brownie.reverts("dev: already minted"):
        pact.brrr()

    print("yfi supply", yfi.totalSupply().to("ether"))
    assert yfi.totalSupply() == "36666 ether"
    assert yfi.balanceOf(treasury) - before == "6666 ether"
