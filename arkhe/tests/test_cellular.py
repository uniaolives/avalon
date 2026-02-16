import pytest
from cellular.phosphoinositide_hypergraph import (
    CellularMembrane, Phosphoinositide, BindingDomain,
    HandoverOperator, CellularProcess
)

def test_pi_transformation():
    pm = CellularMembrane("plasma_membrane")
    pm.add_pi("PI(4,5)P2", count=1)
    pm.add_kinase("PI3K", "PI(4,5)P2 → PI(3,4,5)P3")

    assert pm.pis[0].pi_type == "PI(4,5)P2"

    success = pm.execute_handover(0, 0)
    assert success is True
    assert pm.pis[0].pi_type == "PI(3,4,5)P3"

def test_effector_recruitment():
    pm = CellularMembrane("plasma_membrane")
    pm.add_pi("PI(3,4,5)P3", count=1)
    pm.add_binding_domain("PH", "Akt")

    pm.recruit_effectors()

    assert "Akt" in pm.pis[0].bound_effectors

def test_cellular_process_execution():
    pm = CellularMembrane("plasma_membrane")
    pm.add_pi("PI(3,4,5)P3", count=1)
    pm.add_binding_domain("PH", "Akt")
    pm.recruit_effectors()

    survival = CellularProcess("Cell_survival", "PI(3,4,5)P3", "Akt")
    assert survival.can_execute(pm) is True

    endocytosis = CellularProcess("Endocytosis", "PI(4,5)P2", "Epsin")
    assert endocytosis.can_execute(pm) is False
