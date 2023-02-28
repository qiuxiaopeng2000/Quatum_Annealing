# Exp. Outline

## E1. Single-Objective TTS

* penalty -> TTS
* annealing time -> TTS

## E2. SOQA-SA Comp.

* Comparison: p_value, means, std, TTS
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