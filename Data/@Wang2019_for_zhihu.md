---
alias: Wang2019
tags: 特征上采样
rating: ⭐
share: false
ptype: article
---

# CARAFE: Content-Aware ReAssembly of FEatures
<cite>* Authors: [[Jiaqi Wang]], [[Kai Chen]], [[Rui Xu]], [[Ziwei Liu]], [[Chen Change Loy]], [[Dahua Lin]]</cite>

* DOI: [10.1109/ICCV.2019.00310](https://doi.org/10.1109/ICCV.2019.00310)

* [Local library](zotero://select/items/1_5UC2YFWK)

***

### 初读印象

comment:: (CARAFE)提出了一种新的上采样方法。


### 动机
特征上采样是深度神经网络中最基本的操作之一。
过去方法：
1. 最近邻和双线性插值：仅考虑了亚像素邻域，未能捕捉密集预测任务所需的丰富语义信息。
2. 反卷积：反卷积算子在整幅图像中应用相同的核，而不考虑内容，这限制了其应对局部变异的能力。参数量和计算量大。

### 方法 
提出了内容感知的特征重组CARAFE，有以下优点
1. 大感受野：不同于以往仅利用亚像素邻域的工作(例如双线性插值)，CARAFE可以在较大的感受野内聚合上下文信息。
2. 内容感知处理：CARAFE不对所有样本使用固定的内核(例如反卷积)，而是支持特定于实例的内容感知处理，从而实时生成自适应的内核。
3. 轻量、快速计算。

#### 内容感知的特征重组 

![Pasted image 20230113171311](https://raw.githubusercontent.com/INiid/Markdown4Zhihu/master/Data/@Wang2019/Pasted image 20230113171311.png)

给定一个大小为 <img src="https://www.zhihu.com/equation?tex=C × H × W" alt="C × H × W" class="ee_img tr_noresize" eeimg="1"> 的特征图 <img src="https://www.zhihu.com/equation?tex=X" alt="X" class="ee_img tr_noresize" eeimg="1"> 和一个上采样比率 <img src="https://www.zhihu.com/equation?tex=σ" alt="σ" class="ee_img tr_noresize" eeimg="1">  (假设 <img src="https://www.zhihu.com/equation?tex=σ" alt="σ" class="ee_img tr_noresize" eeimg="1"> 是一个整数)，CARAFE将产生一个新的大小为 <img src="https://www.zhihu.com/equation?tex=C × σH × σ W" alt="C × σH × σ W" class="ee_img tr_noresize" eeimg="1"> 的特征图 <img src="https://www.zhihu.com/equation?tex=X'" alt="X'" class="ee_img tr_noresize" eeimg="1"> 。
对于输出X′的任意目标位置 <img src="https://www.zhihu.com/equation?tex=l'=(i', j')" alt="l'=(i', j')" class="ee_img tr_noresize" eeimg="1"> ，在输入 <img src="https://www.zhihu.com/equation?tex=X" alt="X" class="ee_img tr_noresize" eeimg="1"> 处有相应的源位置 <img src="https://www.zhihu.com/equation?tex=l = ( i , j)" alt="l = ( i , j)" class="ee_img tr_noresize" eeimg="1"> ，其中 <img src="https://www.zhihu.com/equation?tex=i = [i'/ σ]，j = [j'/ σ]" alt="i = [i'/ σ]，j = [j'/ σ]" class="ee_img tr_noresize" eeimg="1"> 。用 <img src="https://www.zhihu.com/equation?tex=N(X_l, k)" alt="N(X_l, k)" class="ee_img tr_noresize" eeimg="1"> 来代指 <img src="https://www.zhihu.com/equation?tex=X" alt="X" class="ee_img tr_noresize" eeimg="1"> 中以位置 <img src="https://www.zhihu.com/equation?tex=l" alt="l" class="ee_img tr_noresize" eeimg="1"> 为中心的 <img src="https://www.zhihu.com/equation?tex=k×k" alt="k×k" class="ee_img tr_noresize" eeimg="1"> 子区域。
1. 根据每个目标位置的内容预测一个重组核：预测核模块 <img src="https://www.zhihu.com/equation?tex=ψ" alt="ψ" class="ee_img tr_noresize" eeimg="1"> 根据 <img src="https://www.zhihu.com/equation?tex=X_l" alt="X_l" class="ee_img tr_noresize" eeimg="1"> 的近邻预测每个位置 <img src="https://www.zhihu.com/equation?tex=l'" alt="l'" class="ee_img tr_noresize" eeimg="1"> 的位置核 <img src="https://www.zhihu.com/equation?tex=W_{l'}" alt="W_{l'}" class="ee_img tr_noresize" eeimg="1"> 。
![Pasted image 20230113160357](https://raw.githubusercontent.com/INiid/Markdown4Zhihu/master/Data/@Wang2019/Pasted image 20230113160357.png)

2. 用预测的核对特征进行重组: <img src="https://www.zhihu.com/equation?tex=φ" alt="φ" class="ee_img tr_noresize" eeimg="1"> 是内容感知的重组模块，它将 <img src="https://www.zhihu.com/equation?tex=X_l" alt="X_l" class="ee_img tr_noresize" eeimg="1"> 的邻居与内核 <img src="https://www.zhihu.com/equation?tex=W_{l'}" alt="W_{l'}" class="ee_img tr_noresize" eeimg="1"> 进行重组。
![Pasted image 20230113160513](https://raw.githubusercontent.com/INiid/Markdown4Zhihu/master/Data/@Wang2019/Pasted image 20230113160513.png)

#### Kernel Prediction Module
目标： <img src="https://www.zhihu.com/equation?tex=X" alt="X" class="ee_img tr_noresize" eeimg="1"> 中一个位置对应 <img src="https://www.zhihu.com/equation?tex=X'" alt="X'" class="ee_img tr_noresize" eeimg="1"> 中 <img src="https://www.zhihu.com/equation?tex=σ^2" alt="σ^2" class="ee_img tr_noresize" eeimg="1"> 个位置，每个目标位置要一个 <img src="https://www.zhihu.com/equation?tex=k_{up}\times k_{up}" alt="k_{up}\times k_{up}" class="ee_img tr_noresize" eeimg="1"> 大小的核，所以该模块最终生成的核大小为 <img src="https://www.zhihu.com/equation?tex=C_{up}*H \times W" alt="C_{up}*H \times W" class="ee_img tr_noresize" eeimg="1"> ,其中 <img src="https://www.zhihu.com/equation?tex=C_{up}=σ^2{k_{up}}^2" alt="C_{up}=σ^2{k_{up}}^2" class="ee_img tr_noresize" eeimg="1"> 。
有三个部分：
1. 通道压缩器减少了输入特征图的通道。
2. 内容编码器将压缩后的特征图作为输入，对内容进行编码，生成重组核。
3. 核正规化器对每个重组核应用一个softmax函数。

##### Channel Compressor
使用 <img src="https://www.zhihu.com/equation?tex=1\times 1" alt="1\times 1" class="ee_img tr_noresize" eeimg="1"> 卷积将维度压缩到 <img src="https://www.zhihu.com/equation?tex=C_m" alt="C_m" class="ee_img tr_noresize" eeimg="1"> 
##### Content Encoder
使用输入通道为 <img src="https://www.zhihu.com/equation?tex=C_m" alt="C_m" class="ee_img tr_noresize" eeimg="1"> ，输出通道为 <img src="https://www.zhihu.com/equation?tex=C_{up}" alt="C_{up}" class="ee_img tr_noresize" eeimg="1"> ，大小为 <img src="https://www.zhihu.com/equation?tex=k_{encoder}\times k_{encoder}" alt="k_{encoder}\times k_{encoder}" class="ee_img tr_noresize" eeimg="1"> 的卷积核，经验公式 <img src="https://www.zhihu.com/equation?tex=k_{encoder}=k_{up}-2" alt="k_{encoder}=k_{up}-2" class="ee_img tr_noresize" eeimg="1"> 。得到的特征图的大小为 <img src="https://www.zhihu.com/equation?tex=C_{up}\times H\times W" alt="C_{up}\times H\times W" class="ee_img tr_noresize" eeimg="1"> 
##### Kernel Normalizer

![Pasted image 20230113172542](https://raw.githubusercontent.com/INiid/Markdown4Zhihu/master/Data/@Wang2019/Pasted image 20230113172542.png)

 <img src="https://www.zhihu.com/equation?tex=C_{up}" alt="C_{up}" class="ee_img tr_noresize" eeimg="1"> 个通道分为 <img src="https://www.zhihu.com/equation?tex=σ^2" alt="σ^2" class="ee_img tr_noresize" eeimg="1"> 个块，块有 <img src="https://www.zhihu.com/equation?tex=k_{up}^2" alt="k_{up}^2" class="ee_img tr_noresize" eeimg="1"> 层。将这 <img src="https://www.zhihu.com/equation?tex=σ^2" alt="σ^2" class="ee_img tr_noresize" eeimg="1"> 个块进行重排列，得到 <img src="https://www.zhihu.com/equation?tex=σH\times σW" alt="σH\times σW" class="ee_img tr_noresize" eeimg="1"> 大小的特征图，通道数为 <img src="https://www.zhihu.com/equation?tex=k_{up}^2" alt="k_{up}^2" class="ee_img tr_noresize" eeimg="1"> ，位置 <img src="https://www.zhihu.com/equation?tex=l'=(i',j')" alt="l'=(i',j')" class="ee_img tr_noresize" eeimg="1"> 上的 <img src="https://www.zhihu.com/equation?tex=k_{up}^2" alt="k_{up}^2" class="ee_img tr_noresize" eeimg="1"> 个数就是对应 <img src="https://www.zhihu.com/equation?tex=X'" alt="X'" class="ee_img tr_noresize" eeimg="1"> 中 <img src="https://www.zhihu.com/equation?tex=l'" alt="l'" class="ee_img tr_noresize" eeimg="1"> 位置的重组核。
对每一个 <img src="https://www.zhihu.com/equation?tex=k_{up}\times k_{up}" alt="k_{up}\times k_{up}" class="ee_img tr_noresize" eeimg="1"> 大小的重组核，使用softmax对其正则化，归一化步骤迫使核值之和为1，这是一个跨越局部区域的软选择。

#### Content-aware Reassembly Module

![4f7432e9787d36f362891086fd6e89a](https://raw.githubusercontent.com/INiid/Markdown4Zhihu/master/Data/@Wang2019/4f7432e9787d36f362891086fd6e89a.jpg)


对 <img src="https://www.zhihu.com/equation?tex=X'" alt="X'" class="ee_img tr_noresize" eeimg="1"> 中每个点使用相应的重组核进行权重聚合 
![Pasted image 20230113180407](https://raw.githubusercontent.com/INiid/Markdown4Zhihu/master/Data/@Wang2019/Pasted image 20230113180407.png)


### 启发
带权重的上采样，还展示了在目标内容不变的情况下，如何生成不同的权重以产生不同的值。