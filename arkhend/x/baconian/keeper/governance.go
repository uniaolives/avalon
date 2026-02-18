package keeper

import (
	"fmt"
	"arkhend/types/sdk"
	"arkhend/x/baconian/types"
)

// SubmitToGovernance envia instância para votação φ
func (k *Keeper) SubmitToGovernance(ctx sdk.Context, instanceID string) error {
	instance, found := k.GetPrerogativeInstance(ctx, instanceID)
	if !found {
		return fmt.Errorf("instance not found: %s", instanceID)
	}

	if instance.Status != types.StatusDraft {
		return fmt.Errorf("instance not in draft status")
	}

	// Verificar requisitos mínimos
	if instance.Confidence.LT(k.GetMinConfidence(ctx)) {
		return fmt.Errorf("confidence too low: %s < %s",
			instance.Confidence.String(), k.GetMinConfidence(ctx).String())
	}

	// Criar proposta de governança
	proposal := sdk.GovernanceProposal{
		Title:       fmt.Sprintf("Induction: %s", instance.Phenomenon),
		Description: instance.ProposedLaw,
		InstanceID:  instanceID,
		Deposit:     k.GetRequiredDeposit(ctx),
	}

	// Submeter
	_, err := k.govKeeper.SubmitProposal(ctx, proposal, proposal.Deposit)
	if err != nil {
		return err
	}

	// Atualizar instância
	instance.Status = types.StatusPending
	now := ctx.BlockTime()
	instance.SubmittedAt = &now
	k.SetPrerogativeInstance(ctx, instance)

	// Registrar na Casa de Salomão
	solomon := k.GetHouseOfSolomon(ctx)
	solomon.Experiments = append(solomon.Experiments, instanceID)
	k.SetHouseOfSolomon(ctx, solomon)

	return nil
}

// ProcessVote processa voto de validador com peso φ
func (k *Keeper) ProcessVote(ctx sdk.Context, instanceID string, voter string, decision bool, justification string) error {
	instance, found := k.GetPrerogativeInstance(ctx, instanceID)
	if !found {
		return fmt.Errorf("instance not found")
	}

	// Calcular poder de voto baseado em coerência do nó
	nodeCoherence := k.coherenceProvider.GetNodeCoherence(ctx, voter)
	phiPower := nodeCoherence // peso direto da coerência

	vote := types.Vote{
		Validator:     voter,
		Decision:      decision,
		PhiPower:      phiPower,
		Justification: justification,
		Timestamp:     ctx.BlockTime(),
	}

	instance.Votes = append(instance.Votes, vote)

	// Verificar se atingiu resolução
	if k.CheckResolution(ctx, instance) {
		k.ResolveInstance(ctx, &instance)
	}

	k.SetPrerogativeInstance(ctx, instance)
	return nil
}

// CheckResolution verifica se atingiu quorum φ (61.8%)
func (k *Keeper) CheckResolution(ctx sdk.Context, instance types.PrerogativeInstance) bool {
	var totalPower, acceptPower sdk.Dec

	for _, vote := range instance.Votes {
		totalPower = totalPower.Add(vote.PhiPower)
		if vote.Decision {
			acceptPower = acceptPower.Add(vote.PhiPower)
		}
	}

	if totalPower.IsZero() {
		return false
	}

	// Quorum φ = 61.8% (proporção áurea)
	quorum := sdk.NewDecWithPrec(618, 3) // 0.618
	ratio := acceptPower.Quo(totalPower)

	return ratio.GTE(quorum)
}

// ResolveInstance finaliza a instância
func (k *Keeper) ResolveInstance(ctx sdk.Context, instance *types.PrerogativeInstance) {
	now := ctx.BlockTime()
	instance.ResolvedAt = &now

	// Contar votos
	var acceptPower, rejectPower sdk.Dec
	for _, vote := range instance.Votes {
		if vote.Decision {
			acceptPower = acceptPower.Add(vote.PhiPower)
		} else {
			rejectPower = rejectPower.Add(vote.PhiPower)
		}
	}

	if acceptPower.GT(rejectPower) {
		instance.Status = types.StatusAccepted

		// Adicionar às leis da Casa de Salomão
		solomon := k.GetHouseOfSolomon(ctx)
		solomon.Laws = append(solomon.Laws, instance.ID)
		k.SetHouseOfSolomon(ctx, solomon)

		// Criar handover de lei para o ledger científico
		k.handoverBridge.CreateHandover(ctx, "baconian", "scientific_ledger",
			k.MustMarshalLaw(*instance))

		// Atualizar coerência global (descoberta científica aumenta C)
		globalC := k.coherenceProvider.GetGlobalCoherence(ctx)
		delta := instance.Confidence.Mul(sdk.NewDecWithPrec(1, 2)) // +1% * confiança
		k.coherenceProvider.UpdateCoherence(ctx, "global", globalC.Add(delta))

	} else {
		instance.Status = types.StatusRejected
	}

	// Persistir
	k.SetPrerogativeInstance(ctx, *instance)
}
