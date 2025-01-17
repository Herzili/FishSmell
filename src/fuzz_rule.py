import shared
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def fuzz_rule_main(l_var):
    print('"模糊规则推算...')
    LVAR = l_var
    # 亮度方差（0，20） 大于20的可以不用处理了。
    if (LVAR > 17):
        print('\033[31m别勉强自己，这张图其实可以不用处理了(-  -)`\033[37m')#\033切换红色，然后再切回白色
        shared.循环次数 = 2
    l_var = ctrl.Antecedent(np.arange(0, 21, 1), 'l_var')
    #atwt的阈值（0，0.1）
    t = ctrl.Consequent(np.arange(0, 0.081, 0.001), 't')
    m = ctrl.Consequent(np.arange(0, 0.5, 0.001), 'm')
    # 生成输入隶属度函数，梯形
    l_var['很低'] = fuzz.trapmf(l_var.universe, [0, 0, 1, 2]) 
    l_var['低'] = fuzz.trapmf(l_var.universe, [1, 2,2, 3])
    l_var['中'] = fuzz.trapmf(l_var.universe, [2, 3, 3,5])
    l_var['高'] = fuzz.trapmf(l_var.universe, [4, 7, 7,12])
    l_var['很高'] = fuzz.trapmf(l_var.universe, [10, 12,20,20])
    # 生成输出隶属度函数， 梯形
    t['很低'] = fuzz.trapmf(t.universe, [0, 0,0.01, 0.02])
    t['低'] = fuzz.trapmf(t.universe, [0.01, 0.02,0.02, 0.03])
    t['中'] = fuzz.trapmf(t.universe, [0.02, 0.025,0.025, 0.04])
    t['高'] = fuzz.trapmf(t.universe, [0.035, 0.04,0.04, 0.05])
    t['很高'] = fuzz.trapmf(t.universe, [0.045, 0.065, 0.08,0.08])

    m['很低'] = fuzz.trapmf(m.universe, [0, 0, 0, 0.15])
    m['低'] = fuzz.trapmf(m.universe, [0.1, 0.15,0.15, 0.25])
    m['中'] = fuzz.trapmf(m.universe, [0.15, 0.25 ,0.25, 0.4])
    m['高'] = fuzz.trapmf(m.universe, [0.25, 0.35 ,0.35, 0.45])
    m['很高'] = fuzz.trapmf(m.universe, [0.35, 0.4,0.4, 0.5])

    #模糊规则
    rule1 = ctrl.Rule(l_var['很低'], t['很低'])
    rule2 = ctrl.Rule(l_var['低'], t['低'])
    rule3 = ctrl.Rule(l_var['中'], t['中'])
    rule4 = ctrl.Rule(l_var['高'], t['高'])
    rule5 = ctrl.Rule(l_var['很高'], t['很高'])

    rule6 = ctrl.Rule(l_var['很低'], m['很高'])
    rule7 = ctrl.Rule(l_var['低'], m['高'])
    rule8 = ctrl.Rule(l_var['中'], m['中'])
    rule9 = ctrl.Rule(l_var['高'], m['低'])
    rule10 = ctrl.Rule(l_var['很高'], m['很低'])

    #创建控制器
    control_system1 = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
    control_simulation1 = ctrl.ControlSystemSimulation(control_system1)
    control_system2 = ctrl.ControlSystem([rule6, rule7, rule8, rule9, rule10])
    control_simulation2 = ctrl.ControlSystemSimulation(control_system2)

    #计算结果
    control_simulation1.input['l_var'] = LVAR
    control_simulation1.compute() 
    control_simulation2.input['l_var'] = LVAR
    control_simulation2.compute() 

    # 9. 输出结果
    print(f"atwt阈值为: {control_simulation1.output['t']:.4f}")
    print(f"SGBNR蒙版值为: {control_simulation2.output['m']:.4f}")

    atwt_threshold = control_simulation1.output['t']
    ab_mask = control_simulation2.output['m']
    l_mask = control_simulation2.output['m']

    #经验值，不要改
    k_l = 1
    k_a = 10
    k_b = 10
    return atwt_threshold,ab_mask,l_mask,k_l,k_a,k_b