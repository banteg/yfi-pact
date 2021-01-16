import pytest
import brownie


@pytest.mark.skip()
def test_migration_from_timelock(yfi, timelock, pact, chain):
    assert yfi.governance() == timelock
    timelock.setTargetGovernance(pact)
    # skip because of this line
    chain.mine(timelock.period())
    timelock.updateTargetGovernance()
    assert yfi.governance() == pact
    pact.sign_pact()
    chain.sleep(5 * 86400 * 365)
    pact.mint()
    assert pact.minted() == "3333 ether"
    assert yfi.totalSupply() == "33333 ether"


def test_migration_fake_gov(yfi, a, pact, chain):
    gov = a.at(yfi.governance(), force=True)
    yfi.setGovernance(pact, {"from": gov})
    pact.sign_pact()
    pact.mint()
    print("pact minted", pact.minted().to("ether"))
    print("yfi supply", yfi.totalSupply().to("ether"))
    assert yfi.totalSupply() > "30000 ether"
    chain.sleep(5 * 86400 * 365)
    pact.mint()
    print("pact minted", pact.minted().to("ether"))
    print("yfi supply", yfi.totalSupply().to("ether"))
    assert pact.minted() > "3333 ether"
    assert yfi.totalSupply() > "33333 ether"


def test_migration_caveats(yfi, a, pact, chain):
    gov = a.at(yfi.governance(), force=True)

    # can't sign because pact is not governance
    with brownie.reverts("dev: pact not yfi governance"):
        pact.sign_pact()

    yfi.setGovernance(pact, {"from": gov})
    assert yfi.governance() == pact
    pact.sign_pact()

    # can't sign the pact twice
    with brownie.reverts("dev: pact signed"):
        pact.sign_pact()

    with brownie.reverts("dev: unauthorized"):
        pact.mint({"from": a[1]})

    # can mint to another account
    mintable = pact.mintable()
    pact.mint(a[1])
    assert yfi.balanceOf(a[1]) == mintable

    # can mint to partial amounts
    chain.sleep(86400)
    before = pact.minted()
    pact.mint(a[2], "1 ether")
    assert yfi.balanceOf(a[2]) == "1 ether"
    assert pact.minted() - before == "1 ether"


def test_pact_gov(a, pact):
    pact.set_governance(a[1])
    assert pact.pending_governance() == a[1]
    pact.accept_governance({"from": a[1]})
    assert pact.governance() == a[1]
