import sys

import dimod
from hybrid.reference.kerberos import KerberosSampler

problem = sys.argv[1]
with open(problem) as fp:
    bqm = dimod.BinaryQuadraticModel.from_coo(fp)

energy_threshold = None
if len(sys.argv) > 2:
    energy_threshold = float(sys.argv[2])

# https://docs.ocean.dwavesys.com/en/stable/docs_hybrid/reference/reference.html#module-hybrid.reference.kerberos
solution = KerberosSampler().sample(bqm, max_iter=10, convergence=3,
                                    energy_threshold=energy_threshold)

print("Solution: {!r}".format(solution.record))
