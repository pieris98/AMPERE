# AMPERE: Aligned Multimodal Protein Encoder Representations

AMPERE is a framework for integrating and aligning multiple protein encoder representations. It provides a unified interface to work with various protein language models and multimodal encoders, facilitating downstream tasks in protein engineering and analysis.

## Key Features
- **Integration of Multiple Protein Encoders**: Seamlessly work with various state-of-the-art protein encoders.
- **Representation Alignment**: Techniques for aligning different embedding spaces for better multimodal integration.
- **Protein Sequence & Structure Support**: Tools for processing both sequence and structural information.

## Supported Encoders
The repository integrates several protein encoding models, including:
- ESM series
- SaProt
- ProTrek
- ProteinDT
- DiMA
- And more...

## Installation
This project uses [Pixi](https://pixi.sh) for dependency management.

```bash
pixi install
```

## Usage
Refer to the `scripts` and `auto-scripts` directories for examples on how to run experiments and process data.
