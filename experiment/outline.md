# Exp. Outline

data: 
NRP: 'Baan'-100, 'ms'-50, 'rp'-25, 'classic-1'-240, 'classic-2'-1120, 'realistic-e1'-4038, 'realistic-g1'-3135,'realistic-m1'-4828
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

FSP: ''BerkeleyDB'-13, 'ERS'-36, 'WebPortal'-43, 'Drupal'-48, Amazon'-79, 'E-shop'-290

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