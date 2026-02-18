package coherence
import "arkhend/types/sdk"
type Module struct{}
func (m Module) GetNodeCoherence(ctx sdk.Context, address string) sdk.Dec { return sdk.NewDecWithPrec(85, 2) }
func (m Module) GetGlobalCoherence(ctx sdk.Context) sdk.Dec { return sdk.NewDecWithPrec(86, 2) }
func (m Module) UpdateCoherence(ctx sdk.Context, address string, delta sdk.Dec) error { return nil }
