# Domain Setup Tools

This allows the user or an agent to run a single command to scaffold a template domain for experiments. Doing so creates these directories:

- Prometheus_VDM/Derivation/code/physics/{domain}
- Prometheus_VDM/Derivation/code/physics/{domain}/schemas
  - Created with a generic example
- Prometheus_VDM/Derivation/code/physics/{domain}/specs
  - Created with a generic example
- Prometheus_VDM/Derivation/code/physics/{domain}/APPROVAL.json
  - Created with generic example content
- Prometheus_VDM/Derivation/code/physics/{domain}/README.md
  - Created with skeleton content. The header should be # {Domain} Experiments, with common sections listed with ## {Section name}. Some sections might include equations, constants, symbols and their meanings, or other important domain or experiment specific documentation.

## Schemas Directory

This directory will hold the schemas that define metadata about individual experiments, along with any tags that are associated.

## Specs Directory

This directory holds the individual configurations and other tag-specific metadata for the experiment. An individual spec MUST BE tag-specific.

## APPROVAL.json

This file is what is checked for the correct authorization hash key and other approval meta-data. If the data values within a given tag key is missing or incorrect, the helpers in common/ will not let the experiment run.

## README.md

This should be automatically created from a template skeleton to include blank sections that would be filled out with important, interesting, or domain specific details like equations, constants, symbols, or other items used that might also be documented in the global "all-caps" files at the root of Prometheus_VDM/Derivations/ (EQUATIONS.md for example).
