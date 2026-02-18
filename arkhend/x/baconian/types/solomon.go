package types

import (
	"time"
	"arkhend/types/sdk"
)

// HouseOfSolomon = governança científica
type HouseOfSolomon struct {
	Members         []string  `json:"members"`          // endereços dos sábios
	EntryThreshold  sdk.Dec   `json:"entry_threshold"`  // C mínimo para entrada
	Experiments     []string  `json:"experiments"`      // IDs ativos
	Laws            []string  `json:"laws"`             // IDs de leis aprovadas
	Secrets         []Secret  `json:"secrets"`          // conhecimentos graduais
	Treasury        sdk.Coins `json:"treasury"`         // fundos de pesquisa
	CreatedAt       time.Time `json:"created_at"`
}

type Secret struct {
	ID          string    `json:"id"`
	Description string    `json:"description"`
	ContentHash string    `json:"content_hash"`     // hash do conteúdo criptografado
	Threshold   sdk.Dec   `json:"threshold"`        // C_global necessário
	Revealed    bool      `json:"revealed"`
	RevealedAt  *time.Time `json:"revealed_at,omitempty"`
}

// Governança: apenas membros podem propor induções
func (h HouseOfSolomon) CanPropose(member string) bool {
	for _, m := range h.Members {
		if m == member {
			return true
		}
	}
	return false
}

// Revelação gradual: conhecimento é liberado conforme C_total aumenta
func (h HouseOfSolomon) ShouldReveal(secret string, globalCoherence sdk.Dec, threshold sdk.Dec) bool {
	return globalCoherence.GTE(threshold)
}
