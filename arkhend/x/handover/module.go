package handover
import (
    "arkhend/types/sdk"
    "arkhend/x/baconian/types"
)
type Module struct{}
func (m Module) CreateHandover(ctx sdk.Context, from, to string, payload []byte) (string, error) { return "h1", nil }
func (m Module) GetHandover(ctx sdk.Context, id string) (types.Handover, error) { return types.Handover{}, nil }
