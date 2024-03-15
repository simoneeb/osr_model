# Description 

This repository contains custom codes for a retina model that predricts the Omitted Stimulus Response (OSR) with latency shift via a depressing inhibitory synapse as presented in:

"Temporal pattern recognition in retinal ganglion cells is mediated by dynamical inhibitory synapses." Simone Ebert, Thomas Buffet, B.Semihcan Sermet, Olivier Marre, Bruno Cessac. bioRxiv 2023.01.12.523643; doi: https://doi.org/10.1101/2023.01.12.523643

# Installation

clone repository 

```
git clone https://github.com/simoneeb/osr_model.git
```

create environment
```
conda env create --name osr_env --file osr_env.yml
```

# Run simulation

run the simulation with the model

```
conda activate osr
python run_simulation_Agly_depressing.py
```

simulations are saved in the  ```output``` folder
