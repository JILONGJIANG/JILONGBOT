"""单栋别墅"光伏+储能+算力"持有型模型（纯Python，无第三方依赖）
所有金额单位：万元；年度现金流；参数以2026年市场区间为准，可在 SCENARIOS 中调整。
"""
import json

def irr(cfs, lo=-0.99, hi=1.0, tol=1e-7):
    def npv(r): return sum(cf/(1+r)**t for t, cf in enumerate(cfs))
    if npv(lo)*npv(hi) > 0: return None
    for _ in range(200):
        mid=(lo+hi)/2
        if npv(lo)*npv(mid) <= 0: hi=mid
        else: lo=mid
        if hi-lo<tol: break
    return (lo+hi)/2

def payback(cfs):
    cum=0
    for t,cf in enumerate(cfs):
        prev=cum; cum+=cf
        if cum>=0 and t>0:
            return t-1 + (-prev/cf if cf else 0)
    return None

BASE = dict(
    # --- 地产 ---
    land_cost=180.0,        # 分摊土地成本/栋
    build_cost=200.0,       # 别墅建安（含精装、含机房土建加强、隔声、消防）
    house_rent_month=1.2,   # 月租金 万元
    house_occ=0.85,         # 出租率
    house_opex_ratio=0.15,  # 物业/维修/税费占房租比例
    # --- 光伏 ---
    pv_kw=20.0, pv_capex_per_w=0.30,   # 万元/kW = 3.0元/W
    pv_hours=1100,          # 等效满发小时（华东）
    pv_self_ratio=0.95,     # 自发自用比例（算力负荷把自用率拉满）
    grid_price=0.85,        # 替代电价 元/kWh（一般工商业/含峰段加权）
    feed_price=0.30,        # 余电上网电价 元/kWh
    pv_degrade=0.006, pv_opex_per_kw=0.003,  # 万元/kW/年
    # --- 储能 ---
    ess_kwh=60.0, ess_capex_per_kwh=0.13,     # 万元/kWh = 1.0元/Wh
    ess_cycles=330, ess_spread=0.50,          # 峰谷价差 元/kWh
    ess_rte=0.88, ess_degrade=0.02, ess_opex=0.3,
    # --- 算力 ---
    servers=2, server_capex=115.0,     # 8卡H20推理服务器 万元/台
    server_kw=5.0,                     # 每台IT功耗 kW（H20典型4-6kW）
    pue=1.3,
    gpu_rent_month=3.0,                # 8卡H20长租 万元/月（2.3-3.3区间中值）
    gpu_util=0.75,                     # 出租率
    gpu_rent_decline=0.12,             # 年租金降幅
    room_capex=25.0,                   # 机房机电（配电、制冷、UPS、网络、消防）
    server_life=5, server_salvage=0.10,
    network_year=3.0, it_opex_year=4.0,   # 专线+运维 万元/年
    elec_price_it=0.75,                # 算力用电电价 元/kWh（自用光伏外的电网购电）
    # --- 资金 ---
    subsidy=20.0,             # 政府补助（绿建+算力+光储合计）
    horizon=15,
    exit_multiple=None,       # 若为None：期末按地产残值+设备残值
    house_terminal_ratio=1.0, # 期末地产价值/初始（土地+建安）
)

def run(p):
    p=dict(BASE, **p)
    capex_house=p['land_cost']+p['build_cost']
    capex_pv=p['pv_kw']*p['pv_capex_per_w']
    capex_ess=p['ess_kwh']*p['ess_capex_per_kwh']
    capex_it=p['servers']*p['server_capex']+p['room_capex']
    capex=capex_house+capex_pv+capex_ess+capex_it-p['subsidy']
    cfs=[-capex]; detail=[]
    for y in range(1,p['horizon']+1):
        # 地产
        rent=p['house_rent_month']*12*p['house_occ']*(1+0.02)**(y-1)
        house_net=rent*(1-p['house_opex_ratio'])
        # 算力负荷电量
        it_kwh=p['servers']*p['server_kw']*p['pue']*p['gpu_util']*8760
        # 光伏
        gen=p['pv_kw']*p['pv_hours']*(1-p['pv_degrade'])**(y-1)
        self_use=min(gen*p['pv_self_ratio'], gen)
        pv_income=(self_use*p['grid_price']+(gen-self_use)*p['feed_price'])/1e4 - p['pv_kw']*p['pv_opex_per_kw']
        # 储能
        ess_income=p['ess_kwh']*(1-p['ess_degrade'])**(y-1)*0.9*p['ess_cycles']*p['ess_spread']*p['ess_rte']/1e4 - p['ess_opex']
        # 算力
        life_cycle=(y-1)%p['server_life']
        gen_idx=(y-1)//p['server_life']
        rent_factor=(0.7**gen_idx)*(1-p['gpu_rent_decline'])**life_cycle
        gpu_income=p['servers']*p['gpu_rent_month']*12*p['gpu_util']*rent_factor
        it_elec_cost=max(it_kwh-self_use,0)*p['elec_price_it']/1e4
        it_net=gpu_income-it_elec_cost-p['network_year']-p['it_opex_year']
        # 设备更新（第6、11年重置服务器，按当时价格下降30%）
        reinvest=0
        if y>1 and (y-1)%p['server_life']==0:
            reinvest=p['servers']*p['server_capex']*(0.7**((y-1)//p['server_life'])) - p['servers']*p['server_capex']*p['server_salvage']
        cf=house_net+pv_income+ess_income+it_net-reinvest
        if y==p['horizon']:
            cf+=capex_house*p['house_terminal_ratio']
        cfs.append(cf)
        detail.append(dict(year=y,house=round(house_net,1),pv=round(pv_income,1),ess=round(ess_income,1),it=round(it_net,1),reinvest=round(reinvest,1),cf=round(cf,1)))
    r=irr(cfs)
    y1=detail[0]
    return dict(capex=round(capex,1),capex_house=round(capex_house,1),capex_pv=round(capex_pv,1),capex_ess=round(capex_ess,1),capex_it=round(capex_it,1),
                y1_house=y1['house'],y1_pv=y1['pv'],y1_ess=y1['ess'],y1_it=y1['it'],y1_total=round(y1['cf'],1),
                yield_y1=round(y1['cf']/capex*100,1),irr=None if r is None else round(r*100,1),payback=None if payback(cfs) is None else round(payback(cfs),1),detail=detail)

SCENARIOS = {
 'S0 仅地产持有（对照）': dict(pv_kw=0,ess_kwh=0,servers=0,room_capex=0,subsidy=0),
 'S1 地产+光储（无算力）': dict(servers=0,room_capex=0,subsidy=8,pv_self_ratio=0.40),
 'S2 基准：别墅内2台8卡H20': {},
 'S2a 别墅内4台8卡H20（50kW机房）': dict(servers=4,room_capex=45,network_year=4,it_opex_year=6),
 'S2b 别墅内2台8卡H100（训练卡）': dict(server_capex=210,gpu_rent_month=6.0,server_kw=8.0,room_capex=35),
 'S3 悲观：租金-40%、年降20%、出租率60%': dict(gpu_rent_month=1.8,gpu_rent_decline=0.20,gpu_util=0.6),
 'S3b 悲观+房租-30%': dict(gpu_rent_month=1.8,gpu_rent_decline=0.20,gpu_util=0.6,house_rent_month=0.84),
 'S4 乐观：租金稳（年降5%）、出租率90%': dict(gpu_rent_decline=0.05,gpu_util=0.9),
 'S5 集中算力站（别墅仅光储+预留，算力按栋分摊2台）': dict(room_capex=8,network_year=1.0,it_opex_year=2.0,subsidy=28,elec_price_it=0.65),
 'S5b 集中算力站+西部低电价0.4': dict(room_capex=8,network_year=1.0,it_opex_year=2.0,subsidy=28,elec_price_it=0.40,pv_hours=1350,land_cost=60,build_cost=160,house_rent_month=0.6),
}

if __name__=='__main__':
    out={}
    for k,v in SCENARIOS.items():
        out[k]=run(v)
    print(f"{'情景':<40}{'总投资':>8}{'首年净现金':>10}{'首年收益率%':>10}{'IRR%':>8}{'回收期(年)':>10}")
    for k,r in out.items():
        print(f"{k:<40}{r['capex']:>8}{r['y1_total']:>10}{r['yield_y1']:>10}{str(r['irr']):>8}{str(r['payback']):>10}")
    print()
    b=out['S2 基准：别墅内2台8卡H20']
    print('基准投资构成:',{k:b[k] for k in ['capex_house','capex_pv','capex_ess','capex_it']})
    print('基准首年分项:',{k:b[k] for k in ['y1_house','y1_pv','y1_ess','y1_it']})
    for d in b['detail']: print(d)
    json.dump(out,open('model_out.json','w'),ensure_ascii=False,indent=1)

# ---------- 算力资产独立测算（5年） ----------
def compute_only(capex=115.0, room=12.5, rent=3.0, util=0.75, decline=0.12, kw=5.0, pue=1.3,
                 elec=0.75, pv_kwh=0, net=1.5, opex=2.0, salvage=0.10, years=5, subsidy=0.0):
    cfs=[-(capex+room)+subsidy]
    for y in range(1,years+1):
        income=rent*12*util*(1-decline)**(y-1)
        kwh=kw*pue*util*8760
        cost=max(kwh-pv_kwh,0)*elec/1e4+net+opex
        cf=income-cost+(capex*salvage if y==years else 0)
        cfs.append(cf)
    return irr(cfs), cfs

def breakeven_rent(target, **kw):
    lo,hi=0.5,15.0
    for _ in range(60):
        mid=(lo+hi)/2
        r,_=compute_only(rent=mid,**kw)
        if r is None or r<target: lo=mid
        else: hi=mid
    return round(hi,2)

if __name__=='__main__':
    print('\n=== 单台8卡H20算力资产（5年、每栋分摊机房12.5万）IRR ===')
    cases={
     '基准：租金3.0万/月、出租率75%、年降12%、电价0.75':dict(),
     '5年闭口包销：租金2.6万/月固定、出租率100%':dict(rent=2.6,util=1.0,decline=0.0),
     '5年闭口包销+算力券20%补贴':dict(rent=2.6,util=1.0,decline=0.0,subsidy=23.0),
     '集中站：电价0.65、机房分摊5万、运维减半':dict(room=5.0,elec=0.65,net=0.8,opex=1.0),
     '集中站+西部电价0.40+闭口合同':dict(room=5.0,elec=0.40,net=0.8,opex=1.0,rent=2.6,util=1.0,decline=0.0),
     '悲观：租金1.8、出租率60%、年降20%':dict(rent=1.8,util=0.6,decline=0.2),
     'H100训练卡：210万、6.0万/月、8kW、年降12%':dict(capex=210,rent=6.0,kw=8.0,room=17.5),
    }
    for k,v in cases.items():
        r,cfs=compute_only(**v)
        print(f"{k:<45} IRR={None if r is None else round(r*100,1)}%  现金流={[round(c,1) for c in cfs]}")
    print('\n=== 达到目标IRR所需的8卡H20月租金（万元/月）===')
    for label,kw in [('户内节点（出租率75%、年降12%）',dict()),('集中站（出租率75%、年降12%）',dict(room=5.0,elec=0.65,net=0.8,opex=1.0)),('集中站闭口合同（出租率100%、年降0）',dict(room=5.0,elec=0.65,net=0.8,opex=1.0,util=1.0,decline=0.0))]:
        print(label, {f'IRR{t}%':breakeven_rent(t/100,**kw) for t in (8,12,15)})
