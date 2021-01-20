# YFI Pact

When signed, Yearn Pact mints 6666 YFI to Yearn Treasury.

The contract is meant to be set as YFI token governance.

## How to use

1. Deploy `YearnPact`
2. `TimelockGovernance.setTargetGovernance(YearnPact)`
3. Wait 3 days
4. `TimelockGovernance.updateTargetGovernance()`
5. Anyone calls `YearnPact.brrr()` which mints 6666 YFI to treasury and reverts YFI token governance back to timelock.
