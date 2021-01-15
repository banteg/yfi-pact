# YFI Pact

An implementation of [this proposal](https://twitter.com/bantg/status/1349755318448910337).

## Abstract

When signed, Yearn Pact mints 666 YFI per year over 5 years, making the terminal YFI supply 33333 YFI.

The contract is meant to be set as YFI token governance.

## How to use

1. Deploy `YearnPact` from Treasury
2. `TimelockGovernance.setTargetGovernance(YearnPact)`
3. Wait 3 days
4. `TimelockGovernance.updateTargetGovernance()`
5. `YearnPact.sign()`
6. `YearnPact.mint(receiver, amount)` to mint up to a vested amount
