package keeper

import (
	"fmt"
	"testing"
	"arkhend/types/sdk"
	"arkhend/x/baconian/types"
	"arkhend/x/coherence"
	"arkhend/x/handover"
	"arkhend/x/gov"
)

func TestPerformInduction(t *testing.T) {
	cp := coherence.Module{}
	hb := handover.Module{}
	gk := gov.Module{}
	k := NewKeeper(cp, hb, gk)

	ctx := sdk.Context{} // Initialized with zero values

	// Add some observations
	phenomenon := "combustion"
	k.observations[phenomenon] = []types.Observation{
		{ID: "o1", Phenomenon: phenomenon, Result: true, Intensity: 0.9, Validator: "v1"},
		{ID: "o2", Phenomenon: phenomenon, Result: true, Intensity: 0.95, Validator: "v2"},
		{ID: "o3", Phenomenon: phenomenon, Result: true, Intensity: 0.8, Validator: "v3"},
		{ID: "o4", Phenomenon: phenomenon, Result: false, Intensity: 0.0, Validator: "v4"},
		{ID: "o5", Phenomenon: phenomenon, Result: true, Intensity: 0.85, Validator: "v5"},
	}

	instance, err := k.PerformInduction(ctx, phenomenon, "proposer1")
	if err != nil {
		t.Fatalf("PerformInduction failed: %v", err)
	}

	if instance.Phenomenon != phenomenon {
		t.Errorf("Expected phenomenon %s, got %s", phenomenon, instance.Phenomenon)
	}

	if len(instance.Table.Presence) != 4 {
		t.Errorf("Expected 4 presence observations, got %d", len(instance.Table.Presence))
	}

	t.Logf("Proposed Law: %s", instance.ProposedLaw)
	t.Logf("Confidence: %v", instance.Confidence.String())
}

func TestDetectIdols(t *testing.T) {
	cp := coherence.Module{}
	hb := handover.Module{}
	gk := gov.Module{}
	k := NewKeeper(cp, hb, gk)

	ctx := sdk.Context{}

	phenomenon := "biased_phenomenon"
	// Create a case for Idolum Tribus (low diversity)
	obs := []types.Observation{}
	for i := 0; i < 25; i++ {
		obs = append(obs, types.Observation{
			ID: fmt.Sprintf("o%d", i),
			Phenomenon: phenomenon,
			Result: true,
			Intensity: 0.9,
			Validator: "v1", // Only 1 validator for 25 observations
		})
	}

	table := k.OrganizeTables(obs)
	idols := k.DetectIdols(ctx, obs, table)

	foundTribus := false
	for _, idol := range idols {
		if idol.Type == types.IdolumTribus {
			foundTribus = true
		}
	}

	if !foundTribus {
		t.Errorf("Expected Idolum Tribus to be detected")
	}
}

func TestIdolIDGeneration(t *testing.T) {
	cp := coherence.Module{}
	hb := handover.Module{}
	gk := gov.Module{}
	k := NewKeeper(cp, hb, gk)
	ctx := sdk.Context{}

	id1 := k.GenerateIdolID(ctx)
	id2 := k.GenerateIdolID(ctx)

	if id1 == id2 {
		t.Errorf("Expected unique IDs, got both as %s", id1)
	}
}

func TestGovernanceResolution(t *testing.T) {
	cp := coherence.Module{}
	hb := handover.Module{}
	gk := gov.Module{}
	k := NewKeeper(cp, hb, gk)
	ctx := sdk.Context{}

	instance := &types.PrerogativeInstance{
		ID:         "ind-1",
		Confidence: 0.9,
		Status:     types.StatusVoting,
	}
	k.instances[instance.ID] = *instance

	// Voter 1: Accept, Power 0.9
	// Voter 2: Accept, Power 0.8
	// Voter 3: Reject, Power 0.7
	// Total: 2.4. Accept: 1.7. Ratio: 1.7/2.4 = 0.708 >= 0.618

	k.ProcessVote(ctx, "ind-1", "v1", true, "Great")
	k.ProcessVote(ctx, "ind-1", "v2", true, "Good")
	k.ProcessVote(ctx, "ind-1", "v3", false, "Bad")

	updated, _ := k.GetPrerogativeInstance(ctx, "ind-1")
	if updated.Status != types.StatusAccepted {
		t.Errorf("Expected StatusAccepted, got %v", updated.Status)
	}
}
