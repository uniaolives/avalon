package types

import "arkhend/types/sdk"

const (
	Satoshi          = 7.28
	PhiCrit          = 0.15
	SyzygyMax        = 0.98
	VacuumEnergy     = -3.71e-11
)

func GetGlobalSatoshi() sdk.Dec {
	return sdk.Dec(Satoshi)
}

func GetPhiThreshold() sdk.Dec {
	return sdk.Dec(PhiCrit)
}

func GetConservationInvariant() sdk.Dec {
	return sdk.Dec(1.0)
}
