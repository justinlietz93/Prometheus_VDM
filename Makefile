# Root Makefile for experiment scaffolding
# Usage examples:
#   make scaffold DOMAIN=metriplectic EXPERIMENT=my_exp TIER=T0 VERSION=0.1.0 SUMMARY="My TL;DR"
#   make scaffold-metriplectic VERSION=0.1.0 SUMMARY="Default skeleton" [FORCE=--force]
# Notes:
#   - Set FORCE=--force to allow overwriting existing files (admin password required)
#   - AUTHOR and CONTACT default from git config; override as needed

.PHONY: scaffold \
	scaffold-agency scaffold-axioms scaffold-causality scaffold-collapse \
	scaffold-conservation_law scaffold-cosmology scaffold-dark_photons \
	scaffold-fluid_dynamics scaffold-intelligence_model scaffold-memory_steering \
	scaffold-metriplectic scaffold-quantum scaffold-rd_conservation \
	scaffold-reaction_diffusion scaffold-tachyonic_condensation \
	scaffold-thermo_routing scaffold-topology

PY ?= python
SCAFFOLD := Derivation/code/common/domain_setup/scaffold_cli.py
# Defaults (can be overridden)
VERSION ?= 0.1.0
TIER ?= T0
AUTHOR ?= $(shell git config user.name 2>/dev/null || echo "Justin K. Lietz")
CONTACT ?= $(shell git config user.email 2>/dev/null || echo "justin@neuroca.ai")
SUMMARY ?= Initial default scaffold
# Optional: set FORCE=--force to enable overwrite with admin prompt
FORCE ?=

# Generic scaffold: provide DOMAIN and EXPERIMENT
scaffold:
	@test -n "$(DOMAIN)" || (echo "ERROR: DOMAIN is required" && exit 2)
	@test -n "$(EXPERIMENT)" || (echo "ERROR: EXPERIMENT is required" && exit 2)
	$(PY) $(SCAFFOLD) \
	  --domain $(DOMAIN) \
	  --experiment $(EXPERIMENT) \
	  --tier $(TIER) \
	  --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(EXPERIMENT)-$(VERSION)) \
	  --author "$(AUTHOR)" \
	  --contact "$(CONTACT)" \
	  --summary "$(SUMMARY)" \
	  $(FORCE)

# Domain-specific defaults
EXPERIMENT_agency           ?= agency_skeleton
EXPERIMENT_axioms           ?= axioms_skeleton
EXPERIMENT_causality        ?= causality_skeleton
EXPERIMENT_collapse         ?= collapse_skeleton
EXPERIMENT_conservation_law ?= conservation_law_skeleton
EXPERIMENT_cosmology        ?= cosmology_skeleton
EXPERIMENT_dark_photons     ?= dark_photons_skeleton
EXPERIMENT_fluid_dynamics   ?= fluid_dynamics_skeleton
EXPERIMENT_intelligence_model ?= intelligence_model_skeleton
EXPERIMENT_memory_steering  ?= memory_steering_skeleton
EXPERIMENT_metriplectic     ?= metriplectic_skeleton
EXPERIMENT_quantum          ?= quantum_skeleton
EXPERIMENT_rd_conservation  ?= rd_conservation_skeleton
EXPERIMENT_reaction_diffusion ?= reaction_diffusion_skeleton
EXPERIMENT_tachyonic_condensation ?= tachyonic_condensation_skeleton
EXPERIMENT_thermo_routing   ?= thermo_routing_skeleton
EXPERIMENT_topology         ?= topology_skeleton

scaffold-agency:
	$(PY) $(SCAFFOLD) --domain agency \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_agency)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_agency))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-axioms:
	$(PY) $(SCAFFOLD) --domain axioms \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_axioms)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_axioms))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-causality:
	$(PY) $(SCAFFOLD) --domain causality \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_causality)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_causality))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-collapse:
	$(PY) $(SCAFFOLD) --domain collapse \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_collapse)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_collapse))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-conservation_law:
	$(PY) $(SCAFFOLD) --domain conservation_law \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_conservation_law)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_conservation_law))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-cosmology:
	$(PY) $(SCAFFOLD) --domain cosmology \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_cosmology)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_cosmology))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-dark_photons:
	$(PY) $(SCAFFOLD) --domain dark_photons \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_dark_photons)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_dark_photons))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-fluid_dynamics:
	$(PY) $(SCAFFOLD) --domain fluid_dynamics \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_fluid_dynamics)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_fluid_dynamics))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-intelligence_model:
	$(PY) $(SCAFFOLD) --domain intelligence_model \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_intelligence_model)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_intelligence_model))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-memory_steering:
	$(PY) $(SCAFFOLD) --domain memory_steering \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_memory_steering)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_memory_steering))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-metriplectic:
	$(PY) $(SCAFFOLD) --domain metriplectic \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_metriplectic)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_metriplectic))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-quantum:
	$(PY) $(SCAFFOLD) --domain quantum \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_quantum)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_quantum))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-rd_conservation:
	$(PY) $(SCAFFOLD) --domain rd_conservation \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_rd_conservation)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_rd_conservation))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-reaction_diffusion:
	$(PY) $(SCAFFOLD) --domain reaction_diffusion \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_reaction_diffusion)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_reaction_diffusion))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-tachyonic_condensation:
	$(PY) $(SCAFFOLD) --domain tachyonic_condensation \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_tachyonic_condensation)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_tachyonic_condensation))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-thermo_routing:
	$(PY) $(SCAFFOLD) --domain thermo_routing \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_thermo_routing)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_thermo_routing))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)

scaffold-topology:
	$(PY) $(SCAFFOLD) --domain topology \
	  --experiment $(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_topology)) \
	  --tier $(TIER) --version $(VERSION) \
	  --tag $(if $(TAG),$(TAG),$(if $(EXPERIMENT),$(EXPERIMENT),$(EXPERIMENT_topology))-$(VERSION)) \
	  --author "$(AUTHOR)" --contact "$(CONTACT)" --summary "$(SUMMARY)" $(FORCE)
