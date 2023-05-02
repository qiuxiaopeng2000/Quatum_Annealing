import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from nen import Problem



problem = Problem('classic-2')
print(problem.variables_num, problem.constraints_num)

  