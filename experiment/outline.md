# Exp. Outline

data: 
NRP: 'rp'-25, 'ms'-50, 'Baan'-100, 'classic-1'-240, 'classic-2'-1120, 'classic-3'-2000, 'classic-4'-4000, 'classic-5'-2500
> 在MOQA上运行到classic-2时，量子计算机就会无法求解
```
Traceback (most recent call last):
  File "MOQA.py", line 35, in <module>
    result = MOQASolver.solve(qp, sample_times=10, num_reads=100)
  File "/home/qiu/optimization/Quatum_Annealing/nen/Solver/MOQASolver.py", line 48, in solve
    sampleset, elapsed = sampler.sample(qubo, num_reads=num_reads)
  File "/home/qiu/optimization/Quatum_Annealing/nen/Solver/EmbeddingSampler.py", line 96, in sample
    embedding, bqm_embedded = self.embed(bqm)
  File "/home/qiu/optimization/Quatum_Annealing/nen/Solver/EmbeddingSampler.py", line 56, in embed
    raise ValueError("no embedding found")
ValueError: no embedding found
```

FSP: 'BerkeleyDB'-13, 'ERS'-36, 'WebPortal'-43, 'Drupal'-48, 'Amazon'-79, 'E-shop'-290, 'eCos'-1244, 'Freebsd'-1396(MemoryError), 
     'Fiasco'-1638, 'uClinux'-1850, 'LinuxX86'-6888

将数据从变量规模从小到大排列
     

## E1. Single-Objective TTS

* penalty -> TTS
* annealing time -> TTS

## E2. SOQA-SA Comp.

* Comparison: p_value, means, std, TTS
* SOQA: num_reads = 100, sample_times = 10
> 由于样本没有服从正态分布且是匹配的，因此使用[Wilcoxon ranksum test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ranksums.html#scipy.stats.ranksums)检验
> 
> 若样本满足正态分布且是匹配的，则使用[t-test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html#scipy.stats.ttest_rel)
> 
> 使用``stats.levene``判断是否具有
> 
> ``scipy.stats.ranksums(x, y)``
> 若p_value < 阈值，则统计结果有效，
> 若statistic 为正则代表右端大于左端，若为负则代表左端大于右端

## E3. MOQA

* Comparison: TTS ,hv, igd, sp
* MOQA: num_reads = 100, sample_times = 10
* NSGA-II: large-scale maxvalue = 10000, small-scale maxvalue = 10000

1. 将NRP和FSP问题分开讨论，将MOQA、Hybrid从一个表中分解成四个表
2. 跑完NRP问题的失效的数据，从老师的以前论文中找
3. 重点描述清楚decomposer的结构内容
4. 增加一个RQ，探究decomposer分解成多组子问题的，初步计算：100规模数据分解成10 * 10 的数据，探究其与只选用前5个数据相比效果差异
5. 增加一个RQ，探究Hybrid什么时候求解能力太差，探究边界问题


实验设计：

约定：数据规模小于100的为小规模问题，大于100的为大规模问题

RQ1： small-scale problems
NRP：'rp'-25, 'ms'-50, 'Baan'-100
FSP：'ERS'-36, 'WebPortal'-43, 'Drupal'-48

RQ2： small-scale problems
NRP：'rp'-25, 'ms'-50, 'Baan'-100
FSP：'ERS'-36, 'WebPortal'-43, 'Drupal'-48

RQ3：medium-large scale problems
NRP：'classic-1'-240, 'classic-2'-1120, 'classic-3'-2000
FSP：'E-shop'-290, 'eCos'-1244, 'uClinux'-1850

RQ4: medium-large scale problems, decomposer: [0.3, 0.5, 0.7]
NRP：'classic-2'-1120, 'classic-3'-2000
FSP：'eCos'-1244, 'uClinux'-1396, 'Fiasco'-1638

RQ5: large scale problems, solve bound
1. 探寻dwave的求解能力，则hybrid的子问题规模大小不能超过这个值
2. 数据规模多大时，hybrid的求解能力下降
sub-size: [100, 300, 500, 700]
NRP：'classic-4'-4000
FSP：'LinuxX86'-6888

