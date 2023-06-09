# Exp. Outline

data: 
NRP: 'ms'-50, 'Baan'-100, 'classic-1'-240, 'classic-2'-1120, 'classic-3'-2000, 'classic-5'-2500
> 在MOQA上运行到classic-2时，量子计算机就会无法求解

FSP: 'BerkeleyDB'-13, 'WebPortal'-43, 'Drupal'-48, 'E-Shop'-290, 'eCos'-1244, 'Fiasco'-1638, 'uClinux'-1850

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
NRP：'rp'-25, 'ms'-50, 'classic-1'-240
FSP：'ERS'-36, 'WebPortal'-43, 'E-Shop'-290

RQ2： small-scale problems
NRP：'rp'-25, 'ms'-50, 'classic-1'-240
FSP：'ERS'-36, 'WebPortal'-43, 'E-Shop'-290

RQ3：medium-large scale problems

分两个表格：MOQA可以求解的
NRP：'classic-1'-240, 'Baan'-100
FSP：'E-Shop'-290, 'Amazon'-79
MOQA无法求解的数据
NRP：'classic-2'-1120, 'classic-3'-2000
FSP：'eCos'-1244, 'uClinux'-1850

RQ4: medium-large scale problems, decomposer: [0.3, 0.5, 0.7]
NRP：'classic-3'-2000, 
FSP：'uClinux'-1396

RQ5: large scale problems, solve bound
1. 探寻dwave的求解能力，则hybrid的子问题规模大小不能超过这个值
2. 数据规模多大时，hybrid的求解能力下降
sub-size: [100, 300, 500, 700]
NRP：'classic-3'-2000
FSP：'uClinux'-1850

大规模分解的subsize用最大embed的大小
RQ1: FSP large-scale, small-scale
RQ2: NRP large-scale, small-scale
RQ3: 相容性：rate, 
确定合适的sub_size

**随问题规模增长的求解时间曲线**
单目标一个图、多目标一个图
大规模和小规模的问题参数不同，用不同的曲线描述，不同的算法用不同的曲线描述

小规模可解，大规模可解，超大规模效果不好


**change**
> 注意承上启下，为什么要建模成QUBO的形式
> intro 一页、back一页、QA两页半、
1. 方法缺少一个整体的描述图，算法符号不能与原文一样，横着放
2. 3.2.3例子用数学符号代替进行简化，并增加一些推导，重点强调约束转化和QUBO建模，用一个统一的公式贯穿全文
3. MOQA和CQHA举例，用符号阐述，并将两个算法结合起来画一个统一的流程图，延续之前的符号转化
4. Related Work 描述NRP、FSP的工作（各两段，在薛老师之后还有两三篇相关的），强调其没有用QA进行求解，再引入QA工作介绍，强调我们的创新点是引用QA求解软件工程领域的FSP和NRP，总共四分之三页，子标题但不用空行
5. 图片和表格都置顶，表格撑满一栏，项目名和指标名称
6. S 和 NS放在指标中


**Hybrid**
initial thoughts:
1. 随机生成一个初始解，并计算该解的能量
2. 使用基于最大能量影响的方法与classic算法（从初始解开始搜寻）并行求解，选取能量最小结果，然后交给tabu进行局部搜索得到一个循环的结果。
> 只选取部分变量、每次一个子问题、下一个循环返回下一个子问题，每次从头和尾部同时选取一个，若相遇则从头开始，若收敛则退出算法，
> 若该子问题包含的变量发生改变则取代该变量在初始解中的值作为本次循环的量子退火解
> 问题越大越能保持数据的特征结构，选取的子问题一开始尽可能大，若子问题无法嵌入则减少子问题大小，每次减少10
3. 若一个循环的结果比原结果好，则替换原结果；若不如原结果，则记录一次，若记录的次数超过一定数值，则视为收敛，返回最终结果。

> 本质上是一个带权图（边和顶点都有权值，且权值有正有负）的分解
> 当前还需解决的问题是
> 1. 分解的子问题如何选取
> 2. 算法结构进一步优化