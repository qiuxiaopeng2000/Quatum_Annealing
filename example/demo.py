import sys

import dimod
import hybrid_test


# load a problem
problem = sys.argv[1]
with open(problem) as fp:
    bqm = dimod.BinaryQuadraticModel.from_coo(fp)


# define the workflow
workflow = hybrid.Loop(
    hybrid.Race(
        hybrid.InterruptableTabuSampler(),
        hybrid.EnergyImpactDecomposer(size=50, rolling=True, traversal='bfs')
        | hybrid.QPUSubproblemAutoEmbeddingSampler()
        | hybrid.SplatComposer()) | hybrid.ArgMin(), convergence=3)


# create a dimod sampler that runs the workflow and sample
result = hybrid.HybridSampler(workflow).sample(bqm)

# show results
print("Solution: sample={.first}".format(result))
