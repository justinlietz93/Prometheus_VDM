"""
Test script to verify all CF-aligned modules can be imported.

Run: python test_imports.py
"""

import sys
import traceback

def test_import(module_name, items=None):
    """Test importing a module and optionally specific items"""
    try:
        if items:
            exec(f"from {module_name} import {', '.join(items)}")
        else:
            exec(f"import {module_name}")
        print(f"✅ {module_name}")
        return True
    except Exception as e:
        print(f"❌ {module_name}: {e}")
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("VDM Runtime v9 - Import Test")
    print("=" * 60)
    
    results = []
    
    # Test CF01: QGT
    print("\n--- CF01: QGT ---")
    results.append(test_import("qgt", [
        "QGTResult", "MetriplecticOperators",
        "compute_qgt", "construct_metriplectic_operators"
    ]))
    
    # Test CF02: Contact Geometry
    print("\n--- CF02: Contact Geometry ---")
    results.append(test_import("contact_geometry", [
        "ContactForm", "ReebVectorField", "GenericEvolution",
        "construct_contact_form", "compute_reeb_vector_field"
    ]))
    
    # Test CF03: A8 Hierarchy
    print("\n--- CF03: A8 Hierarchy ---")
    results.append(test_import("a8_hierarchy", [
        "InterfaceCount", "HierarchyAnalysis",
        "analyze_a8_hierarchy", "verify_log_scaling"
    ]))
    
    # Test CF04/CF11: Void Equations
    print("\n--- CF04/CF11: Void Equations ---")
    results.append(test_import("void_equations", [
        "CFDerivedParameters", "telegraph_rhs",
        "bond_weighted_laplacian", "solve_telegraph_step"
    ]))
    
    # Test CF05: Integrability Closure
    print("\n--- CF05: Integrability Closure ---")
    results.append(test_import("integrability_closure", [
        "FirstIntegral", "CasimirVerification",
        "verify_metriplectic_casimirs", "prove_closure"
    ]))
    
    # Test CF07: Measurement Theory
    print("\n--- CF07: Measurement Theory ---")
    results.append(test_import("measurement_theory", [
        "DensityMatrix", "DecoherenceResult", "BornRuleResult",
        "compute_decoherence_time", "derive_born_rule"
    ]))
    
    # Test CF08: Spinor Emergence
    print("\n--- CF08: Spinor Emergence ---")
    results.append(test_import("spinor_emergence", [
        "DomainWallProfile", "ChiralZeroMode", "GinspargWilsonOperator",
        "compute_domain_wall_profile", "construct_ginsparg_wilson_operator"
    ]))
    
    # Test CF09: Gauge Emergence
    print("\n--- CF09: Gauge Emergence ---")
    results.append(test_import("gauge_emergence", [
        "BerryConnection", "FieldStrength", "MaxwellAction", "GaugeBoson",
        "compute_berry_connection", "compute_field_strength"
    ]))
    
    # Test CF09: Gauge Dynamics
    print("\n--- CF09: Gauge Dynamics ---")
    results.append(test_import("gauge", [
        "GaugeBosonEvent", "GaugeBosonEmitter",
        "GaugeBosonPropagator", "GaugeDynamics"
    ]))
    
    # Test Connectome
    print("\n--- Connectome ---")
    results.append(test_import("connectome", [
        "Node", "Bond", "Connectome"
    ]))
    
    # Test package __init__
    print("\n--- Package __init__ ---")
    results.append(test_import("__init__", [
        "get_cf_alignment_status", "print_cf_alignment_report"
    ]))
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} modules imported successfully")
    print("=" * 60)
    
    if passed == total:
        print("✅ All imports successful!")
        return 0
    else:
        print("❌ Some imports failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
