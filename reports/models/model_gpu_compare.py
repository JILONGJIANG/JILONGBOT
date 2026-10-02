"""8 卡 GPU 服务器横向对比：H100 / H200 / B200 / B300 / RTX PRO 6000。欧元，纯 Python。

两种口径
- 自有成本：我们自己买机器、付电费、付利息，生产 100 万个 token 要花多少钱。
- 市场租金：按 2026-10 市场 GPU 小时租金折算的每百万 token 价格，相当于"商场零售价"。

吞吐量取 MLPerf Inference v5.1 / v6.0 / v6.1 封闭组的实测值（每 GPU 每秒输出 token，offline 场景）。
offline 是满批量的上限，交互式在线服务通常只有它的 30–60%，两种口径同比例缩小，
所以比较各型号的相对高低仍然成立。

运行： python3 model_gpu_compare.py
"""

FX = 1.08            # USD per EUR
YEARS = 5            # 摊销年限
RATE = 0.06          # 融资利率
ELEC = 0.15          # €/kWh
LOAD = 0.80          # 满负荷运行时的平均功率 / 铭牌最大功率
OPS = 0.03           # 保险 + 维护，按总投资每年计
GRID_KW = 100.0      # 别墅并网点上限

PUE = {'air': 1.45, 'liquid': 1.15}
INFRA_PER_KW = {'air': 2000.0, 'liquid': 2600.0}   # €/kW：机柜、配电、UPS、冷却、网络、消防、安装

# 每台 8 卡服务器。price 为美元整机价（市场中位），kw 为铭牌最大功率
SERVERS = {
    'H100':         dict(price=285_000, kw=10.2, mem=80,  rent_mid=3.38, rent_low=1.30),
    'H200':         dict(price=370_000, kw=10.2, mem=141, rent_mid=4.38, rent_low=2.09),
    'B200':         dict(price=450_000, kw=14.3, mem=180, rent_mid=6.25, rent_low=3.75),
    'B300':         dict(price=600_000, kw=14.5, mem=288, rent_mid=8.88, rent_low=4.99),
    'RTX PRO 6000': dict(price=195_000, kw=9.1,  mem=96,  rent_mid=2.19, rent_low=0.65),
}

# MLPerf 封闭组，每 GPU 每秒输出 token（offline）。None = 无公开结果
TPS = {
    'Llama 2 70B (稠密 70B，相当于企业自用模型)': {
        'H100': 3897, 'H200': 4380, 'B200': 12691, 'B300': 14119, 'RTX PRO 6000': 3739},
    'gpt-oss-120B (MoE 中型模型)': {
        'H100': None, 'H200': 3585, 'B200': 11436, 'B300': 13330, 'RTX PRO 6000': 1967},
    'DeepSeek-R1 671B (MoE 大模型，最接近 Kimi)': {
        'H100': None, 'H200': 2400, 'B200': 7364, 'B300': 8767, 'RTX PRO 6000': None},
}
# H200 的 DeepSeek-R1 没有 MLPerf 封闭组成绩。按 SemiAnalysis 同口径 B200 / H200 ≈ 3.05 倍推算，属估计值
ESTIMATED = {('DeepSeek-R1 671B (MoE 大模型，最接近 Kimi)', 'H200')}


def annuity_factor(rate, years):
    return rate / (1 - (1 + rate) ** -years)


def eur_per_server_hour(name, cooling, util=1.0):
    """一台服务器每运行一小时的自有成本（€）。util 为利用率，空闲时间的固定成本摊到干活时间上。"""
    s = SERVERS[name]
    hw = s['price'] / FX
    infra = INFRA_PER_KW[cooling] * s['kw']
    capex = hw + infra
    fixed_year = capex * annuity_factor(RATE, YEARS) + capex * OPS
    fixed_hour = fixed_year / (8760 * util)
    power_hour = s['kw'] * LOAD * PUE[cooling] * ELEC
    return fixed_hour + power_hour, capex


def servers_in_grid(name, cooling):
    s = SERVERS[name]
    return int(GRID_KW // (s['kw'] * PUE[cooling]))


def fmt(x, d=2):
    return '—' if x is None else f'{x:,.{d}f}'


def main():
    names = list(SERVERS)
    print('== 1. 100 kW 并网点能放几台（按铭牌最大功率 × PUE，不靠电池）==')
    print('型号 | 风冷台数 | 液冷台数 | 风冷满载 kW | 液冷满载 kW')
    for n in names:
        a, l = servers_in_grid(n, 'air'), servers_in_grid(n, 'liquid')
        print(f"{n} | {a} | {l} | {a * SERVERS[n]['kw'] * PUE['air']:.0f} | {l * SERVERS[n]['kw'] * PUE['liquid']:.0f}")

    print('\n== 2. 自有成本：每百万输出 token（€），风冷，5 年摊销，6% 利息，电价 0.15 €/kWh ==')
    for util in (1.0, 0.6):
        print(f'\n-- 利用率 {util:.0%} --')
        print('模型 | ' + ' | '.join(names))
        for wl, row in TPS.items():
            cells = []
            for n in names:
                tps = row[n]
                if tps is None:
                    cells.append('—')
                    continue
                cost, _ = eur_per_server_hour(n, 'air', util)
                per_m = cost / (tps * 8 * 3600 / 1e6)
                tag = '*' if (wl, n) in ESTIMATED else ''
                cells.append(f'{per_m:.3f}{tag}')
            print(wl + ' | ' + ' | '.join(cells))

    print('\n== 3. 市场零售口径：按 2026-10 中位租金折算的每百万输出 token（$）==')
    print('模型 | ' + ' | '.join(names))
    for wl, row in TPS.items():
        cells = []
        for n in names:
            tps = row[n]
            cells.append('—' if tps is None else f"{SERVERS[n]['rent_mid'] / (tps * 3600 / 1e6):.3f}")
        print(wl + ' | ' + ' | '.join(cells))

    print('\n== 4. 同一个 100 kW 并网点，装满后的总产出与总投资（风冷）==')
    print('型号 | 台数 | 卡数 | 总投资 k€ | Llama70B 级 百万token/天 | 每百万 token 自有成本 €（60% 利用率）')
    wl = 'Llama 2 70B (稠密 70B，相当于企业自用模型)'
    for n in names:
        k = servers_in_grid(n, 'air')
        cost, capex = eur_per_server_hour(n, 'air', 0.6)
        tokens_day = TPS[wl][n] * 8 * k * 86400 * 0.6 / 1e6
        per_m = cost / (TPS[wl][n] * 8 * 3600 / 1e6)
        print(f'{n} | {k} | {k * 8} | {capex * k / 1000:,.0f} | {tokens_day:,.0f} | {per_m:.3f}')

    print('\n== 5. 出租回报：单台年租金收入 / 整机投资（60% 出租率）==')
    print('型号 | 整机投资 k€ | 低价档 $/卡时 | 年收入 k€ | 毛回报率 | 中位档 $/卡时 | 年收入 k€ | 毛回报率 | 年电费 k€')
    for n in names:
        s = SERVERS[n]
        _, capex = eur_per_server_hour(n, 'air')
        rows = []
        for p in (s['rent_low'], s['rent_mid']):
            rev = p / FX * 8 * 8760 * 0.6
            rows += [f'{p:.2f}', f'{rev / 1000:,.0f}', f'{rev / capex:.0%}']
        elec_year = s['kw'] * (LOAD * 0.6 + 0.35 * 0.4) * PUE['air'] * ELEC * 8760
        print(f"{n} | {capex / 1000:,.0f} | " + ' | '.join(rows) + f' | {elec_year / 1000:,.0f}')
    print('\n* 估计值：H200 跑 DeepSeek-R1 无 MLPerf 封闭组成绩，按 SemiAnalysis 同口径 B200/H200≈3.05 倍推算。')


if __name__ == '__main__':
    main()
