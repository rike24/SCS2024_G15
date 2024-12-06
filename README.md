# SCS2024_G15
Group project for the simulation of complex systems course at chalmers in 2024

Forest ecosystems have become increasingly vulnerable to diseases and pests in recent years, posing significant ecological and economic challenges. 
The loss of forests impacts biodiversity by reducing wildlife habitats, while also threatening the sustainable supply of wood, a critical resource for construction and other industries.

Our project aims to investigate the dynamics of disease and pest outbreaks in forests through simulations. 
Specifically, we will model common scenarios such as fungal infections, using a graph-based representation of root systems, and beetle infestations, employing an adapted lattice model inspired by the lecture.

As an initial step, we will model a simplified forest with a single tree species and one type of disease, drawing inspiration from the forest fire simulation discussed in the lecture (chapter 3).
In subsequent stages, we aim to explore how the presence of multiple tree species influences the overall stability of the forest ecosystem. 
Further possibilities of our models are the introduction of other diseases.

Agenda:

Deadline simulations: 12/12

Index
No tree = 0
Species A = -1
Species B = -2 (immune)
Infected = 1

# To-do (from Fri 6/12)

 - Research the time scale for disease spreading (should one time step = 1 yr?) (Brian, Marike)

 - Description of mechanisms of disease-spreading (for report/poster) (Megan)

 - Should we take age into account (when disease-spreading? older trees have a larger range of infection) (Zishan, is this possible?)

 - Should we implement a probability of tree dying (trees don't die w 100% prob after infectionTime)

 - Batch simulations (new main for running batches) for ensemble average of infection and wood outcome (Herman)

 - Long run for time average
 
 - Need to decide which forest configurations/initial conditions we want to simulate

 - Run simulations to generate graphs/images for poster draft 10/12

 - Write draft text of results/conclusions/discussion for poster (Marcus)

 - Graph of ratio species A / species B for different forests?

 - Work on report/ research (Everyone)



# To ask Daniel on Wednesday:

## How are trees regrown? 
Assume naturally regrown (not planted), but how should we model this?
Trees regrown with a probability for each species or regrown based on the surrounding trees' species?






