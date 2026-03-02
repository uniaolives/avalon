package keeper

import (
	"fmt"
	"math"
	"arkhend/types/sdk"
	"arkhend/x/baconian/types"
)

// GovKeeper stub interface
type GovKeeper interface {
	SubmitProposal(ctx sdk.Context, proposal sdk.GovernanceProposal, deposit sdk.Coins) (string, error)
}

type Keeper struct {
	coherenceProvider  types.CoherenceProvider
	handoverBridge     types.HandoverBridge
	govKeeper          GovKeeper

	// Mock stores for the stub
	observations       map[string][]types.Observation
	instances          map[string]types.PrerogativeInstance
	solomon            types.HouseOfSolomon

	// Counters for ID generation to avoid collisions
	instanceCounter    uint64
	idolCounter        uint64
}

func NewKeeper(cp types.CoherenceProvider, hb types.HandoverBridge, gk GovKeeper) Keeper {
	return Keeper{
		coherenceProvider: cp,
		handoverBridge:    hb,
		govKeeper:         gk,
		observations:      make(map[string][]types.Observation),
		instances:         make(map[string]types.PrerogativeInstance),
	}
}

// -----------------------------------------------------------------------------
// MÁQUINA DE INDUÇÃO BACONIANA
// -----------------------------------------------------------------------------

// PerformInduction executa o método indutivo completo
func (k *Keeper) PerformInduction(ctx sdk.Context, phenomenon string, proposer string) (*types.PrerogativeInstance, error) {
	// FASE 1: COLETA (recuperar observações como handovers)
	observations := k.GetObservationsByPhenomenon(ctx, phenomenon)
	if len(observations) < k.GetMinObservations(ctx) {
		return nil, fmt.Errorf("insufficient observations: need %d, have %d",
			k.GetMinObservations(ctx), len(observations))
	}

	// FASE 2: TABULAÇÃO (organizar em tábuas)
	table := k.OrganizeTables(observations)

	// FASE 3: ELIMINATIO (detectar e corrigir ídolos)
	idols := k.DetectIdols(ctx, observations, table)
	correctedTable := k.ApplyCorrections(table, idols)

	// FASE 4: INDUCTIO (inferir lei causal)
	law, confidence, support, specificity := k.InferLaw(correctedTable)

	// FASE 5: CRIAÇÃO DA INSTÂNCIA PRIVILEGIADA
	instance := &types.PrerogativeInstance{
		ID:          k.GeneratePrerogativeID(ctx),
		Phenomenon:  phenomenon,
		Table:       correctedTable,
		Idols:       idols,
		ProposedLaw: law,
		Confidence:  confidence,
		Support:     support,
		Specificity: specificity,
		Proposer:    proposer,
		Status:      types.StatusDraft,
		CreatedAt:   ctx.BlockTime(),
		BlockHeight: ctx.BlockHeight(),
	}

	// Persistir
	k.SetPrerogativeInstance(ctx, *instance)

	// Emitir evento Arkhe(N)
	ctx.EventManager().EmitEvent(sdk.NewEvent(
		"baconian_induction_created",
		sdk.NewAttribute("instance_id", instance.ID),
		sdk.NewAttribute("phenomenon", phenomenon),
		sdk.NewAttribute("confidence", confidence.String()),
		sdk.NewAttribute("n_idols", fmt.Sprintf("%d", len(idols))),
	))

	return instance, nil
}

// -----------------------------------------------------------------------------
// DETECÇÃO DE ÍDOLOS (ELIMINATIO)
// -----------------------------------------------------------------------------

func (k *Keeper) DetectIdols(ctx sdk.Context, obs []types.Observation, table types.Table) []types.Idol {
	var idols []types.Idol

	// IDOLUM TRIBUS: viés sensorial sistemático
	if idol := k.detectTribus(ctx, obs); idol != nil {
		idols = append(idols, *idol)
	}

	// IDOLUM SPECUS: padrões idiossincráticos
	idols = append(idols, k.detectSpecus(ctx, obs)...)

	// IDOLUM FORI: inconsistências semânticas
	if idol := k.detectFori(ctx, obs); idol != nil {
		idols = append(idols, *idol)
	}

	// IDOLUM THEATRI: dogmas cristalizados
	if idol := k.detectTheatri(ctx, obs, table); idol != nil {
		idols = append(idols, *idol)
	}

	return idols
}

func (k *Keeper) detectTribus(ctx sdk.Context, obs []types.Observation) *types.Idol {
	validators := make(map[string]int)
	for _, o := range obs {
		validators[o.Validator]++
	}

	if len(validators) < 3 && len(obs) > 20 {
		return &types.Idol{
			ID:              k.GenerateIdolID(ctx),
			Type:            types.IdolumTribus,
			Severity:        sdk.NewDecWithPrec(7, 1), // 0.7
			Description:     "Baixa diversidade de observadores: risco de viés sensorial coletivo",
			DetectionMethod: "diversity_index < 3",
			AffectedObs:     k.getAllObsIDs(obs),
			AffectedNodes:   k.getKeys(validators),
			Correction: types.Correction{
				Strategy:   "weight",
				Parameters: []string{"diversity_penalty", "0.5"},
			},
			DetectedAt:  ctx.BlockTime(),
			BlockHeight: ctx.BlockHeight(),
		}
	}
	return nil
}

func (k *Keeper) detectSpecus(ctx sdk.Context, obs []types.Observation) []types.Idol {
	var idols []types.Idol
	byValidator := make(map[string][]types.Observation)
	for _, o := range obs {
		byValidator[o.Validator] = append(byValidator[o.Validator], o)
	}

	globalMean := k.calculateMeanIntensity(obs)
	globalStd := k.calculateStdIntensity(obs)

	for validator, vObs := range byValidator {
		if len(vObs) < 5 {
			continue
		}

		localMean := k.calculateMeanIntensity(vObs)
		diff := localMean.Sub(globalMean).Abs()

		var zScore sdk.Dec
		if globalStd.IsZero() {
			if diff.GT(sdk.ZeroDec()) {
				zScore = sdk.NewDec(10) // Arbitrary high z-score
			} else {
				zScore = sdk.ZeroDec()
			}
		} else {
			zScore = diff.Quo(globalStd)
		}

		if zScore.GT(sdk.NewDec(2)) {
			idols = append(idols, types.Idol{
				ID:              k.GenerateIdolID(ctx),
				Type:            types.IdolumSpecus,
				Severity:        sdk.MinDec(zScore.Quo(sdk.NewDec(3)), sdk.NewDec(1)),
				Description:     fmt.Sprintf("Padrão idiossincrático: média local %s vs global %s",
					localMean.String(), globalMean.String()),
				DetectionMethod: "z-score > 2",
				AffectedObs:     k.getObsIDs(vObs),
				AffectedNodes:   []string{validator},
				Correction: types.Correction{
					Strategy:   "weight",
					Parameters: []string{"outlier_downweight", "0.3"},
				},
				DetectedAt:  ctx.BlockTime(),
				BlockHeight: ctx.BlockHeight(),
			})
		}
	}
	return idols
}

func (k *Keeper) detectFori(ctx sdk.Context, obs []types.Observation) *types.Idol {
	contexts := make(map[string]int)
	for _, o := range obs {
		contexts[o.Context]++
	}

	if len(contexts) > len(obs)/2 && len(obs) > 10 {
		return &types.Idol{
			ID:              k.GenerateIdolID(ctx),
			Type:            types.IdolumFori,
			Severity:        sdk.NewDecWithPrec(5, 1),
			Description:     "Alta variabilidade semântica nos contextos observacionais",
			DetectionMethod: "unique_contexts / total_obs > 0.5",
			AffectedObs:     k.getAllObsIDs(obs),
			AffectedNodes:   k.getUniqueValidators(obs),
			Correction: types.Correction{
				Strategy:   "cluster",
				Parameters: []string{"semantic_embedding", "cosine_similarity", "0.8"},
			},
			DetectedAt:  ctx.BlockTime(),
			BlockHeight: ctx.BlockHeight(),
		}
	}
	return nil
}

func (k *Keeper) detectTheatri(ctx sdk.Context, obs []types.Observation, table types.Table) *types.Idol {
	if len(table.Presence) + len(table.Absence) < 10 {
		return nil
	}

	presenceRatio := sdk.NewDec(int64(len(table.Presence))).Quo(
		sdk.NewDec(int64(len(table.Presence) + len(table.Absence))))

	if presenceRatio.GT(sdk.NewDecWithPrec(9, 1)) {
		return &types.Idol{
			ID:              k.GenerateIdolID(ctx),
			Type:            types.IdolumTheatri,
			Severity:        presenceRatio.Sub(sdk.NewDecWithPrec(8, 1)).Mul(sdk.NewDec(5)),
			Description:     "Possível confirmação seletiva: 90%+ de observações positivas",
			DetectionMethod: "presence_ratio > 0.9",
			AffectedObs:     k.getObsIDs(table.Presence),
			AffectedNodes:   k.getUniqueValidators(obs),
			Correction: types.Correction{
				Strategy:   "require_absence",
				Parameters: []string{"mandatory_negative_controls", "10"},
			},
			DetectedAt:  ctx.BlockTime(),
			BlockHeight: ctx.BlockHeight(),
		}
	}
	return nil
}

// -----------------------------------------------------------------------------
// INFERÊNCIA CAUSAL (INDUCTIO)
// -----------------------------------------------------------------------------

func (k *Keeper) InferLaw(table types.Table) (law string, confidence, support, specificity sdk.Dec) {
	presenceFeatures := k.ExtractFeatures(table.Presence)
	absenceFeatures := k.ExtractFeatures(table.Absence)
	necessaryCondition := k.FindIntersection(presenceFeatures)
	isSufficient := k.CheckSufficiency(necessaryCondition, absenceFeatures)

	total := int64(len(table.Presence) + len(table.Absence))
	if total == 0 {
		return "Sem dados", sdk.ZeroDec(), sdk.ZeroDec(), sdk.ZeroDec()
	}
	support = sdk.NewDec(int64(len(table.Presence))).Quo(sdk.NewDec(total))

	specificity = sdk.NewDec(1)
	if len(absenceFeatures) > 0 {
		specificity = sdk.NewDec(int64(len(absenceFeatures) - k.CountMatches(necessaryCondition, absenceFeatures))).Quo(
			sdk.NewDec(int64(len(absenceFeatures))))
	}

	confidence = support.Mul(specificity)
	if isSufficient {
		confidence = confidence.Mul(sdk.NewDec(1))
	} else {
		confidence = confidence.Mul(sdk.NewDecWithPrec(5, 1))
	}

	if isSufficient {
		law = fmt.Sprintf("∀x: %s → Fenômeno ocorre (necessário e suficiente)", necessaryCondition)
	} else {
		law = fmt.Sprintf("∀x: %s → Fenômeno provavelmente ocorre (necessário, não suficiente)", necessaryCondition)
	}

	return law, confidence, support, specificity
}

// -----------------------------------------------------------------------------
// HELPERS & STUBS
// -----------------------------------------------------------------------------

func (k *Keeper) ExtractFeatures(obs []types.Observation) []string {
	return []string{"heat", "oxygen"}
}

func (k *Keeper) FindIntersection(features []string) string {
	return "calor + oxigênio"
}

func (k *Keeper) CheckSufficiency(condition string, absenceFeatures []string) bool {
	return true
}

func (k *Keeper) CountMatches(condition string, absenceFeatures []string) int {
	return 0
}

func (k *Keeper) GetObservationsByPhenomenon(ctx sdk.Context, phenomenon string) []types.Observation {
	return k.observations[phenomenon]
}

func (k *Keeper) GetMinObservations(ctx sdk.Context) int {
	return 5
}

func (k *Keeper) OrganizeTables(obs []types.Observation) types.Table {
	var table types.Table
	table.Phenomenon = obs[0].Phenomenon
	for _, o := range obs {
		if o.Result {
			table.Presence = append(table.Presence, o)
		} else {
			table.Absence = append(table.Absence, o)
		}
		if o.Intensity.GT(sdk.ZeroDec()) {
			table.Degrees = append(table.Degrees, o)
		}
	}
	table.TotalObservations = len(obs)
	return table
}

func (k *Keeper) ApplyCorrections(table types.Table, idols []types.Idol) types.Table {
	return table
}

func (k *Keeper) GeneratePrerogativeID(ctx sdk.Context) string {
	k.instanceCounter++
	return fmt.Sprintf("ind-%d-%d", ctx.BlockHeight(), k.instanceCounter)
}

func (k *Keeper) SetPrerogativeInstance(ctx sdk.Context, instance types.PrerogativeInstance) {
	k.instances[instance.ID] = instance
}

func (k *Keeper) GetPrerogativeInstance(ctx sdk.Context, id string) (types.PrerogativeInstance, bool) {
	inst, ok := k.instances[id]
	return inst, ok
}

func (k *Keeper) GetHouseOfSolomon(ctx sdk.Context) types.HouseOfSolomon {
	return k.solomon
}

func (k *Keeper) SetHouseOfSolomon(ctx sdk.Context, solomon types.HouseOfSolomon) {
	k.solomon = solomon
}

func (k *Keeper) GetMinConfidence(ctx sdk.Context) sdk.Dec {
	return sdk.NewDecWithPrec(6, 1) // 0.6
}

func (k *Keeper) GetRequiredDeposit(ctx sdk.Context) sdk.Coins {
	return sdk.Coins("100satoshi")
}

func (k *Keeper) MustMarshalLaw(instance types.PrerogativeInstance) []byte {
	return []byte(instance.ProposedLaw)
}

func (k *Keeper) GenerateIdolID(ctx sdk.Context) string {
	k.idolCounter++
	return fmt.Sprintf("idol-%d-%d", ctx.BlockHeight(), k.idolCounter)
}

func (k *Keeper) calculateMeanIntensity(obs []types.Observation) sdk.Dec {
	if len(obs) == 0 {
		return sdk.ZeroDec()
	}
	var total sdk.Dec
	for _, o := range obs {
		total = total.Add(o.Intensity)
	}
	return total.Quo(sdk.NewDec(int64(len(obs))))
}

func (k *Keeper) calculateStdIntensity(obs []types.Observation) sdk.Dec {
	if len(obs) < 2 {
		return sdk.ZeroDec()
	}
	mean := k.calculateMeanIntensity(obs)
	var sumSq sdk.Dec
	for _, o := range obs {
		diff := o.Intensity.Sub(mean)
		sumSq = sumSq.Add(diff.Mul(diff))
	}
	variance := sumSq.Quo(sdk.NewDec(int64(len(obs))))
	return sdk.Dec(math.Sqrt(float64(variance)))
}

func (k *Keeper) getAllObsIDs(obs []types.Observation) []string {
	var ids []string
	for _, o := range obs {
		ids = append(ids, o.ID)
	}
	return ids
}

func (k *Keeper) getObsIDs(obs []types.Observation) []string {
	return k.getAllObsIDs(obs)
}

func (k *Keeper) getKeys(m map[string]int) []string {
	var keys []string
	for k := range m {
		keys = append(keys, k)
	}
	return keys
}

func (k *Keeper) getUniqueValidators(obs []types.Observation) []string {
	m := make(map[string]bool)
	var keys []string
	for _, o := range obs {
		if !m[o.Validator] {
			m[o.Validator] = true
			keys = append(keys, o.Validator)
		}
	}
	return keys
}
