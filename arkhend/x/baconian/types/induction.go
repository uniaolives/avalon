package types

import (
	"time"
	"arkhend/types/sdk"
)

// Observation = handover sensorial atomico
type Observation struct {
	ID          string    `json:"id"`
	Phenomenon  string    `json:"phenomenon"`   // chave de agrupamento
	Context     string    `json:"context"`      // condições experimentais
	Result      bool      `json:"result"`       // fenômeno ocorreu?
	Intensity   sdk.Dec   `json:"intensity"`    // grau [0,1]
	Timestamp   time.Time `json:"timestamp"`
	Validator   string    `json:"validator"`    // endereço do nó
	Signature   []byte    `json:"signature"`    // prova criptográfica
	BlockHeight int64     `json:"block_height"`
	Node        string    `json:"node"`         // Alias for Validator if needed

	// Metadados Arkhe(N)
	CoherenceAtCreation sdk.Dec `json:"coherence_at_creation"` // C do nó
	HandoverID          string  `json:"handover_id"`           // link ao handover
}

// Table = tábua baconiana organizada
type Table struct {
	Phenomenon string        `json:"phenomenon"`
	Presence   []Observation `json:"presence"`   // tábua de presença
	Absence    []Observation `json:"absence"`    // tábua de ausência
	Degrees    []Observation `json:"degrees"`    // tábua de graus
	CreatedAt  time.Time     `json:"created_at"`
	UpdatedAt  time.Time     `json:"updated_at"`

	// Métricas de qualidade
	TotalObservations int     `json:"total_observations"`
	ValidatorSet      []string `json:"validator_set"` // nós únicos
}

// Idol = nó de baixa coerência epistemológica
type Idol struct {
	ID              string     `json:"id"`
	Type            IdolType   `json:"type"`
	Severity        sdk.Dec    `json:"severity"`         // [0,1]
	Description     string     `json:"description"`
	DetectionMethod string     `json:"detection_method"`
	AffectedObs     []string   `json:"affected_obs"`     // IDs de observações
	AffectedNodes   []string   `json:"affected_nodes"`   // endereços
	Correction      Correction `json:"correction"`
	DetectedAt      time.Time  `json:"detected_at"`
	BlockHeight     int64      `json:"block_height"`

	// Arkhe(N) specific
	CoherenceImpact sdk.Dec `json:"coherence_impact"` // redução em C_global
}

type IdolType int

const (
	IdolumTribus  IdolType = iota // 0: erros da tribo (sensoriais)
	IdolumSpecus                  // 1: erros da caverna (individuais)
	IdolumFori                    // 2: erros do fórum (linguísticos)
	IdolumTheatri                 // 3: erros do teatro (dogmáticos)
)

func (i IdolType) String() string {
	switch i {
	case IdolumTribus:  return "Idolum Tribus"
	case IdolumSpecus:  return "Idolum Specus"
	case IdolumFori:    return "Idolum Fori"
	case IdolumTheatri: return "Idolum Theatri"
	default:            return "Unknown"
	}
}

// Correction = método de remediação
type Correction struct {
	Strategy    string   `json:"strategy"`     // "filter", "weight", "exclude"
	Parameters  []string `json:"parameters"`   // args específicos
	Applied     bool     `json:"applied"`
	AppliedAt   *time.Time `json:"applied_at,omitempty"`
	AppliedBy   string   `json:"applied_by,omitempty"`
}

// PrerogativeInstance = handover de alta intensidade epistemológica
type PrerogativeInstance struct {
	ID           string        `json:"id"`
	Phenomenon   string        `json:"phenomenon"`
	Table        Table         `json:"table"`
	Idols        []Idol        `json:"idols"`          // detectados e (talvez) corrigidos

	// Resultado da indução
	ProposedLaw  string        `json:"proposed_law"`   // formulação causal
	Confidence   sdk.Dec       `json:"confidence"`     // P(lei|dados)
	Support      sdk.Dec       `json:"support"`        // cobertura dos dados
	Specificity  sdk.Dec       `json:"specificity"`    // precisão da condição

	// Governança
	Proposer     string        `json:"proposer"`       // endereço
	Status       Status        `json:"status"`         // lifecycle
	Votes        []Vote        `json:"votes"`
	CreatedAt    time.Time     `json:"created_at"`
	SubmittedAt  *time.Time    `json:"submitted_at,omitempty"`
	ResolvedAt   *time.Time    `json:"resolved_at,omitempty"`
	BlockHeight  int64         `json:"block_height"`
}

type Status int

const (
	StatusDraft      Status = iota // 0: em construção
	StatusPending                  // 1: submetido, aguardando votação
	StatusVoting                   // 2: em votação φ
	StatusAccepted                 // 3: lei aprovada
	StatusRejected                 // 4: lei rejeitada
	StatusExpired                  // 5: expirou sem quorum
)

// Vote = voto φ de validador
type Vote struct {
	Validator   string    `json:"validator"`
	Decision    bool      `json:"decision"`      // true = aceitar
	PhiPower    sdk.Dec   `json:"phi_power"`     // peso baseado em C do nó
	Justification string  `json:"justification"` // argumento baconiano
	Timestamp   time.Time `json:"timestamp"`
}
