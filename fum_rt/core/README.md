core/
├── __init__.py
├── README.md
├── control_server.py (this belongs in api or something)
├── global_system.py
│
├── cortex/
│   ├── __init__.py
│   ├── connectome.py
│   ├── sparse_connectome.py
│   ├── void_b1.py
│   └── void_dynamics_adapter.py
│
├── neuroplasticity/
│   ├── __init__.py
│   ├── fum_growth_arbiter.py
│   ├── fum_sie.py
│   ├── fum_structural_homeostasis.py
│   └── sie_v2.py
│
├── primitives/
│   ├── __init__.py
│   └── text_utils.py
│
├── proprioception/
│   ├── __init__.py
│   ├── announce.py
│   ├── diagnostics.py
│   ├── metrics.py
│   └── visualizer.py
│
└── substrate/
    ├── __init__.py
    ├── adc.py
    ├── bus.py
    └── memory.py