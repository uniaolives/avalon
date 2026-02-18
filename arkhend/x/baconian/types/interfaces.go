package types

import (
	"time"
	"arkhend/types/sdk"
)

// -----------------------------------------------------------------------------
// INTERFACES ARKHE(N)
// -----------------------------------------------------------------------------

// CoherenceProvider = interface para x/coherence
type CoherenceProvider interface {
	GetNodeCoherence(ctx sdk.Context, address string) sdk.Dec
	GetGlobalCoherence(ctx sdk.Context) sdk.Dec
	UpdateCoherence(ctx sdk.Context, address string, delta sdk.Dec) error
}

// HandoverBridge = interface para x/handover
type HandoverBridge interface {
	CreateHandover(ctx sdk.Context, from, to string, payload []byte) (string, error)
	GetHandover(ctx sdk.Context, id string) (Handover, error)
}

type Handover struct {
	ID        string    `json:"id"`
	From      string    `json:"from"`
	To        string    `json:"to"`
	Type      string    `json:"type"`      // "observation", "induction", "law"
	Payload   []byte    `json:"payload"`
	Timestamp time.Time `json:"timestamp"`
	Coherence sdk.Dec   `json:"coherence"` // C no momento do handover
}
