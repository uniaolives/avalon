package gov
import "arkhend/types/sdk"
type Module struct{}
func (m Module) SubmitProposal(ctx sdk.Context, proposal sdk.GovernanceProposal, deposit sdk.Coins) (string, error) { return "p1", nil }
