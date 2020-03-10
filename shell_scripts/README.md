# shell_scripts

Copyright (c) 2020 马成 All rights reserved.
E-mail:15810063661@163.com
Last_modified:2020/3/10

Here I will elaborate the functions of each scripts：

vasp_environment:创建一些环境变量，使一些脚本在当前shell生效(source)，编辑添加PATH环境变量

relax:根据计算结构判断是否收敛。如果收敛则将原POSCAR备份后拷贝CONTCAR为新的POSCAR。

encut_converge:以元素中最大ENMAX为标准，从0.9倍到2倍的标准值以0.1倍为间隔计算后提取总能信息。当总能收敛到给定值（默认值为0.002）后停止。

kpoints_converge:根据POSCAR中各个晶轴长度，分别以10、15、25、40为积计算得到k_mesh。分别计算后提取总能信息。当总能收敛到给定值（默认值为0.002）后停止。

sigma_converge:SIGMA从0以0.01的间隔一直取到0.2分别计算并提取总能，最后取总能差最小值（经测试该值会先减小后增大）。

density_of_states:将计算后的DoS信息按原子提取出来，并自动整合一个所有原子的总DoS。

specified_dos:将选择的原子的DoS整合。

u_test:根据给定的目标gap，U从0开始每次增大给定值（默认为0.5）后计算并计算得到gap，最终得到最接近目标的U。
