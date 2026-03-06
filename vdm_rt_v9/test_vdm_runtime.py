"""
Test script to verify all CF-aligned modules can be imported.

Run from /mnt/okcomputer/output:
    python test_vdm_runtime.py
"""

import sys
sys.path.insert(0, '.')

def main():
    print("=" * 60)
    print("VDM Runtime v9 - Import Test")
    print("=" * 60)
    
    results = []
    
    # Test CF01: QGT
    print("\n--- CF01: QGT ---")
    try:
        from vdm_runtime import (
            QGTResult, MetriplecticOperators,
            compute_qgt, construct_metriplectic_operators
        )
        print("✅ CF01: QGT module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ CF01: {e}")
        results.append(False)
    
    # Test CF02: Contact Geometry
    print("\n--- CF02: Contact Geometry ---")
    try:
        from vdm_runtime import (
            ContactForm, ReebVectorField, GenericEvolution,
            construct_contact_form, compute_reeb_vector_field
        )
        print("✅ CF02: Contact geometry module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ CF02: {e}")
        results.append(False)
    
    # Test CF03: A8 Hierarchy
    print("\n--- CF03: A8 Hierarchy ---")
    try:
        from vdm_runtime import (
            InterfaceCount, HierarchyAnalysis,
            analyze_a8_hierarchy, verify_log_scaling
        )
        print("✅ CF03: A8 hierarchy module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ CF03: {e}")
        results.append(False)
    
    # Test CF04/CF11: Void Equations
    print("\n--- CF04/CF11: Void Equations ---")
    try:
        from vdm_runtime import (
            CFDerivedParameters, telegraph_rhs,
            bond_weighted_laplacian, solve_telegraph_step
        )
        print("✅ CF04/CF11: Void equations module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ CF04/CF11: {e}")
        results.append(False)
    
    # Test CF05: Integrability Closure
    print("\n--- CF05: Integrability Closure ---")
    try:
        from vdm_runtime import (
            FirstIntegral, CasimirVerification,
            verify_metriplectic_casimirs, prove_closure
        )
        print("✅ CF05: Integrability closure module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ CF05: {e}")
        results.append(False)
    
    # Test CF07: Measurement Theory
    print("\n--- CF07: Measurement Theory ---")
    try:
        from vdm_runtime import (
            DensityMatrix, DecoherenceResult, BornRuleResult,
            compute_decoherence_time, derive_born_rule
        )
        print("✅ CF07: Measurement theory module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ CF07: {e}")
        results.append(False)
    
    # Test CF08: Spinor Emergence
    print("\n--- CF08: Spinor Emergence ---")
    try:
        from vdm_runtime import (
            DomainWallProfile, ChiralZeroMode, GinspargWilsonOperator,
            compute_domain_wall_profile, construct_ginsparg_wilson_operator
        )
        print("✅ CF08: Spinor emergence module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ CF08: {e}")
        results.append(False)
    
    # Test CF09: Gauge Emergence
    print("\n--- CF09: Gauge Emergence ---")
    try:
        from vdm_runtime import (
            BerryConnection, FieldStrength, MaxwellAction, GaugeBoson,
            compute_berry_connection, compute_field_strength
        )
        print("✅ CF09: Gauge emergence module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ CF09: {e}")
        results.append(False)
    
    # Test CF09: Gauge Dynamics
    print("\n--- CF09: Gauge Dynamics ---")
    try:
        from vdm_runtime import (
            GaugeBosonEvent, GaugeBosonEmitter,
            GaugeBosonPropagator, GaugeDynamics
        )
        print("✅ CF09: Gauge dynamics module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ CF09: {e}")
        results.append(False)
    
    # Test Connectome
    print("\n--- Connectome ---")
    try:
        from vdm_runtime import (
            Node, Bond, Connectome
        )
        print("✅ Connectome module imported successfully")
        results.append(True)
    except Exception as e:
        print(f"❌ Connectome: {e}")
        results.append(False)
    
    # Test package functions
    print("\n--- Package Functions ---")
    try:
        from vdm_runtime import (
            get_cf_alignment_status, print_cf_alignment_report
        )
        status = get_cf_alignment_status()
        print(f"✅ Package functions imported successfully")
        print(f"   CF documents implemented: {len(status)}")
        results.append(True)
    except Exception as e:
        print(f"❌ Package functions: {e}")
        results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} modules imported successfully")
    print("=" * 60)
    
    if passed == total:
        print("✅ All imports successful!")
        print("\nRunning CF alignment report...")
        print_cf_alignment_report()
        return 0
    else:
        print("❌ Some imports failed")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
