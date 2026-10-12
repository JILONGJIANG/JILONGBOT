"""单台 NVIDIA HGX B300（8 卡）部署在 Montgat 别墅的经济模型。欧元，纯 Python。

口径说明
- 只算算力 SPV。光伏与储能归能源 SPV，算力 SPV 按电价向其购电，因此本模型不含光储 capex。
- gpu_price 是「主机实收价」，即已扣除平台佣金后落到我们账上的价格，不是挂牌价。
- 电耗按利用率加权：满载功率 × 利用率 + 空载功率 × (1-利用率)，再乘冷却系数。
- 硬件价格 650 k€ 为占位值，须由 TD SYNNEX / Lenovo 正式报价替换。

运行： python3 model_b300.py
"""
import json

def irr(cfs, lo=-0.95, hi=3.0, tol=1e-9):
    def f(r): return sum(cf / (1 + r) ** t for t, cf in enumerate(cfs))
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2

def npv(cfs, r):
    return sum(cf / (1 + r) ** t for t, cf in enumerate(cfs))

BASE = dict(
    # ---- 资本支出（k€）----
    hw=650.0,            # HGX B300 8 卡整机，待正式报价替换
    cooling=30.0,        # CDU + 室外干冷器 + 管路 + 试压调试
    electrical=8.0,      # 单相 14.49 kW → 三相 43.64 kW：配电商费用 + 内部工程 + boletín
    room=20.0,           # 车库/地下室：防火分区、防静电地板、通风、除湿、环境监控
    ups_net=15.0,        # UPS + PDU + 交换机 + 布线 + 远程管理
    fire=13.0,           # 气体灭火 + 探测（住宅地下空间 CTE-DB-SI）
    install=15.0,        # 安装、调试、72 h 满载测试
    contingency=0.10,    # 不可预见费，按前述合计计提

    # ---- 收入 ----
    gpus=8,
    gpu_price=4.50,      # USD/GPU·小时，主机实收价（已扣平台佣金）
    util=0.45,
    price_decline=0.20,  # 年降价幅度
    fx=1.08,             # USD per EUR

    # ---- 用电 ----
    kw_full=16.0,        # 整机满载（8×1400W GPU + CPU/网卡/风扇/电源损耗），待报价确认
    kw_idle_ratio=0.35,  # 空载功率占满载比例
    cooling_overhead=1.08,  # 液冷 CDU 与干冷器附加能耗
    elec_price=0.15,     # €/kWh，含容量费摊销

    # ---- 其他运营（k€/年）----
    internet=3.6,
    insurance=8.0,       # 住宅内 650 k€ 设备，商业财产 + 责任险
    maint=6.0,           # 远程运维、监控软件、现场巡检
    support_from_y4=30.0,  # 原厂支持前 3 年随机器，第 4 年起单买

    # ---- 融资 ----
    ltv=0.70,
    rate=0.06,
    term_years=5,

    # ---- 退出 ----
    horizon=5,
    salvage_ratio=0.20,  # 5 年后整机二手残值占硬件原价比例
)

def capex(p):
    sub = p['hw'] + p['cooling'] + p['electrical'] + p['room'] + p['ups_net'] + p['fire'] + p['install']
    return sub * (1 + p['contingency'])

def annuity(principal, rate, years):
    if rate == 0:
        return principal / years
    m = rate / 12
    n = years * 12
    pay = principal * m / (1 - (1 + m) ** -n)
    return pay * 12

def run(p=None):
    p = dict(BASE, **(p or {}))
    total_capex = capex(p)
    debt = total_capex * p['ltv']
    equity = total_capex - debt
    debt_service = annuity(debt, p['rate'], p['term_years'])

    kw_avg = p['kw_full'] * (p['util'] + (1 - p['util']) * p['kw_idle_ratio']) * p['cooling_overhead']
    mwh = kw_avg * 8760 / 1000
    elec = mwh * p['elec_price']          # k€/年

    rows = []
    equity_cfs = [-equity]
    project_cfs = [-total_capex]
    for y in range(1, p['horizon'] + 1):
        price = p['gpu_price'] * (1 - p['price_decline']) ** (y - 1)
        rev_usd = p['gpus'] * price * 8760 * p['util']
        rev = rev_usd / p['fx'] / 1000      # k€
        opex = elec + p['internet'] + p['insurance'] + p['maint'] + (p['support_from_y4'] if y >= 4 else 0.0)
        noi = rev - opex
        ds = debt_service if y <= p['term_years'] else 0.0
        eq_cf = noi - ds
        rows.append(dict(year=y, price=round(price, 2), revenue=round(rev, 1), opex=round(opex, 1),
                         noi=round(noi, 1), debt_service=round(ds, 1), equity_cf=round(eq_cf, 1)))
        equity_cfs.append(eq_cf)
        project_cfs.append(noi)

    salvage = p['hw'] * p['salvage_ratio']
    debt_left = max(0.0, debt - sum(min(debt_service, debt) for _ in range(min(p['horizon'], p['term_years']))) * 0)
    # 5 年期贷款在 horizon=5 时恰好还清；若 term > horizon 需扣未偿余额
    if p['term_years'] > p['horizon']:
        m = p['rate'] / 12
        n_total = p['term_years'] * 12
        n_paid = p['horizon'] * 12
        pay_m = debt * m / (1 - (1 + m) ** -n_total)
        debt_left = pay_m * (1 - (1 + m) ** -(n_total - n_paid)) / m
    else:
        debt_left = 0.0
    equity_cfs[-1] += salvage - debt_left
    project_cfs[-1] += salvage

    return dict(
        capex=round(total_capex, 1), debt=round(debt, 1), equity=round(equity, 1),
        debt_service=round(debt_service, 1), kw_avg=round(kw_avg, 2),
        mwh_year=round(mwh, 1), elec_year=round(elec, 1),
        rows=rows, salvage=round(salvage, 1),
        equity_irr=irr(equity_cfs), project_irr=irr(project_cfs),
        equity_npv10=round(npv(equity_cfs, 0.10), 1),
        cum_equity_cf=round(sum(equity_cfs[1:]), 1),
        y1_equity_cf=round(equity_cfs[1], 1),
    )

SCENARIOS = {
    '悲观': dict(gpu_price=3.00, util=0.30, price_decline=0.25, hw=700.0, salvage_ratio=0.15),
    '基准': dict(),
    '乐观': dict(gpu_price=6.00, util=0.65, price_decline=0.15, hw=600.0, salvage_ratio=0.25),
}

def breakeven(p=None, target='debt_service'):
    """求第 1 年覆盖还本付息所需的 价格×利用率 组合。"""
    p = dict(BASE, **(p or {}))
    out = []
    for util in (0.30, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80):
        lo, hi = 0.5, 30.0
        for _ in range(200):
            mid = (lo + hi) / 2
            q = dict(p, util=util, gpu_price=mid)
            r = run(q)
            if r['rows'][0]['noi'] - r['rows'][0]['debt_service'] >= 0:
                hi = mid
            else:
                lo = mid
        out.append((util, round((lo + hi) / 2, 2)))
    return out

def term_sensitivity(p=None):
    out = []
    for yrs in (3, 5, 7):
        for ltv in (0.60, 0.70, 0.80):
            r = run(dict(p or {}, term_years=yrs, ltv=ltv, horizon=max(5, yrs)))
            out.append(dict(term=yrs, ltv=ltv, debt_service=r['debt_service'],
                            y1_equity_cf=r['y1_equity_cf'], equity=r['equity'],
                            equity_irr=None if r['equity_irr'] is None else round(r['equity_irr'] * 100, 1)))
    return out

if __name__ == '__main__':
    print('=== 单台 HGX B300 · 别墅部署 · 算力 SPV ===\n')
    base = run()
    print(f"总投资 {base['capex']} k€ | 债 {base['debt']} | 股本 {base['equity']} | 年还本付息 {base['debt_service']} k€")
    print(f"加权平均功率 {base['kw_avg']} kW | 年用电 {base['mwh_year']} MWh | 年电费 {base['elec_year']} k€\n")

    for name, ov in SCENARIOS.items():
        r = run(ov)
        irr_s = 'n/a' if r['equity_irr'] is None else f"{r['equity_irr']*100:.1f}%"
        print(f"--- {name} ---")
        print(f"  总投资 {r['capex']} k€ | 股本 {r['equity']} k€ | 年还本付息 {r['debt_service']} k€")
        for row in r['rows']:
            print(f"   Y{row['year']}  价 ${row['price']}/h  收入 {row['revenue']}  运营 {row['opex']}"
                  f"  NOI {row['noi']}  还贷 {row['debt_service']}  股本现金流 {row['equity_cf']}")
        print(f"  5 年股本累计现金流 {r['cum_equity_cf']} k€ | 残值 {r['salvage']} k€ | 股本 IRR {irr_s}\n")

    print('=== 第 1 年覆盖还本付息所需的最低实收价（USD/GPU·小时）===')
    for util, price in breakeven():
        print(f"  利用率 {util:.0%}  →  需要 ${price}/GPU·小时")

    print('\n=== 融资条件敏感性（基准运营假设，第 1 年股本现金流 k€）===')
    for d in term_sensitivity():
        irr_s = 'n/a' if d['equity_irr'] is None else f"{d['equity_irr']}%"
        print(f"  {d['term']} 年 / LTV {d['ltv']:.0%}  股本 {d['equity']} k€"
              f"  年供 {d['debt_service']} k€  Y1 股本现金流 {d['y1_equity_cf']} k€  IRR {irr_s}")

    with open('model_b300_out.json', 'w') as f:
        json.dump({k: run(v) for k, v in SCENARIOS.items()}, f, ensure_ascii=False, indent=1)
