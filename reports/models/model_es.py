"""Montgat 别墅"光伏+储能+算力"模型（欧元，千欧 k€）。纯 Python。
参数为 2026-09 西班牙/加泰罗尼亚区间中值，可在 SCENARIOS 调整。"""
import json

def irr(cfs, lo=-0.99, hi=2.0, tol=1e-7):
    def npv(r): return sum(cf/(1+r)**t for t, cf in enumerate(cfs))
    if npv(lo)*npv(hi) > 0: return None
    for _ in range(200):
        mid=(lo+hi)/2
        if npv(lo)*npv(mid) <= 0: hi=mid
        else: lo=mid
        if hi-lo<tol: break
    return (lo+hi)/2
def npv(cfs,r): return sum(cf/(1+r)**t for t,cf in enumerate(cfs))
def payback(cfs):
    cum=0
    for t,cf in enumerate(cfs):
        prev=cum; cum+=cf
        if cum>=0 and t>0: return t-1+(-prev/cf if cf else 0)
    return None

# ---------- 单栋别墅（k€，10 年） ----------
BASE=dict(
    land=250.0, build=640.0,          # 土地分摊 + 建安（280 m² × 2.3 k€/m²，加泰独栋中高品质）
    sale_price=1150.0,                # Montgat 独栋带泳池售价（k€）
    rent_month=3.8, occ=0.90, opex_ratio=0.20, rent_growth=0.02,
    house_terminal=1.0,
    pv_kwp=12.0, pv_eur_wp=1.2, pv_yield=1500, pv_self=0.45, pv_degr=0.005,
    grid_price=0.20, surplus_price=0.05, pv_opex_kwp=0.012,
    ess_kwh=30.0, ess_eur_kwh=0.60, ess_civil=8.0,   # 户用 30 kWh 室外柜 + 基础/隔声
    ess_selfuse_gain=0.30,            # 储能把自用比例再提高 30 个百分点
    ess_backup_value=0.6, ess_opex=0.3,
    servers=0, server_capex=300.0, server_kw_avg=7.0, pue=1.25,
    gpu_price_h=2.6, gpu_util=0.55, gpu_decline=0.18, gpus_per_server=8,
    room_capex=60.0, server_life=5, salvage=0.10,
    it_opex_year=12.0, network_year=6.0, elec_it=0.13,
    subsidy=0.0, horizon=10,
)
def run(p):
    p=dict(BASE,**p)
    capex_house=p['land']+p['build']
    capex_pv=p['pv_kwp']*p['pv_eur_wp']
    capex_ess=p['ess_kwh']*p['ess_eur_kwh']+(p['ess_civil'] if p['ess_kwh']>0 else 0)
    capex_it=p['servers']*p['server_capex']+(p['room_capex'] if p['servers']>0 else 0)
    capex=capex_house+capex_pv+capex_ess+capex_it-p['subsidy']
    cfs=[-capex]; rows=[]
    for y in range(1,p['horizon']+1):
        house=p['rent_month']*12*p['occ']*(1-p['opex_ratio'])*(1+p['rent_growth'])**(y-1)
        gen=p['pv_kwp']*p['pv_yield']*(1-p['pv_degr'])**(y-1)          # kWh
        it_kwh=p['servers']*p['server_kw_avg']*p['pue']*8760
        if p['servers']>0: self_ratio=1.0
        else: self_ratio=min(1.0,p['pv_self']+(p['ess_selfuse_gain'] if p['ess_kwh']>0 else 0))
        self_kwh=gen*self_ratio
        pv=(self_kwh*p['grid_price']+(gen-self_kwh)*p['surplus_price'])/1000-p['pv_kwp']*p['pv_opex_kwp']
        ess=(p['ess_backup_value']-p['ess_opex']) if p['ess_kwh']>0 else 0
        gen_idx=(y-1)//p['server_life']
        price=p['gpu_price_h']*(0.75**gen_idx)*(1-p['gpu_decline'])**((y-1)%p['server_life'])
        it_inc=p['servers']*p['gpus_per_server']*price*8760*p['gpu_util']/1000
        it_cost=(max(it_kwh-self_kwh,0)*p['elec_it']/1000+p['it_opex_year']+p['network_year']) if p['servers']>0 else 0
        reinv=0
        if p['servers']>0 and y>1 and (y-1)%p['server_life']==0:
            reinv=p['servers']*p['server_capex']*(0.7**gen_idx)-p['servers']*p['server_capex']*p['salvage']*(0.7**(gen_idx-1))
        cf=house+pv+ess+it_inc-it_cost-reinv
        if y==p['horizon']: cf+=capex_house*p['house_terminal']+(p['servers']*p['server_capex']*p['salvage']*(0.7**gen_idx) if p['servers']>0 else 0)
        cfs.append(cf); rows.append(dict(y=y,house=round(house,1),pv=round(pv,1),ess=round(ess,1),it=round(it_inc-it_cost,1),reinv=round(reinv,1),cf=round(cf,1)))
    r=irr(cfs)
    return dict(capex=round(capex,1),capex_house=capex_house,capex_pv=round(capex_pv,1),capex_ess=round(capex_ess,1),capex_it=round(capex_it,1),
                y1=rows[0],yield_y1=round(rows[0]['cf']/capex*100,1),irr=None if r is None else round(r*100,1),
                payback=None if payback(cfs) is None else round(payback(cfs),1),npv6=round(npv(cfs,0.06),1),rows=rows)

SCENARIOS={
 'V0 别墅持有出租（对照）':dict(pv_kwp=0,ess_kwh=0),
 'V1 别墅 + 12 kWp 光伏':dict(ess_kwh=0),
 'V2 别墅 + 光伏 + 30 kWh 室外储能':dict(),
 'V2s 同 V2，售出别墅（开发利润，对照）':dict(horizon=1,house_terminal=0,rent_month=0,pv_kwp=0,ess_kwh=0),
 'V3 别墅 + 光储 + 1 台 HGX H200（试点）':dict(servers=1),
 'V4 别墅 + 光储 + 3 台 HGX H200':dict(servers=3,room_capex=180.0,it_opex_year=30.0,network_year=10.0),
 'V4p 同 V4 悲观：实收 $2.25、利用率 40%':dict(servers=3,room_capex=180.0,it_opex_year=30.0,network_year=10.0,gpu_price_h=1.95,gpu_util=0.40),
 'V4o 同 V4 乐观：实收 $3.75、利用率 70%、年降 10%':dict(servers=3,room_capex=180.0,it_opex_year=30.0,network_year=10.0,gpu_price_h=3.25,gpu_util=0.70,gpu_decline=0.10),
}

# ---------- 算力资产独立测算（1 台 8×H200，5 年，k€） ----------
def compute_only(capex=300.0,room=60.0,price=2.6,util=0.55,decline=0.18,kw=7.0,pue=1.25,elec=0.13,
                 pv_kwh=0,net=6.0,opex=12.0,salvage=0.10,years=5,subsidy=0.0,lease_rate=None):
    cfs=[-(capex+room)+subsidy]
    for y in range(1,years+1):
        inc=8*price*(1-decline)**(y-1)*8760*util/1000
        kwh=kw*pue*8760*util/0.55 if False else kw*pue*8760
        cost=max(kwh-pv_kwh,0)*elec/1000+net+opex
        cfs.append(inc-cost+(capex*salvage if y==years else 0))
    return irr(cfs),cfs
def breakeven_price(target,**kw):
    lo,hi=0.3,15.0
    for _ in range(60):
        mid=(lo+hi)/2; r,_=compute_only(price=mid,**kw)
        if r is None or r<target: lo=mid
        else: hi=mid
    return round(hi,2)

if __name__=='__main__':
    print(f"{'情景':<46}{'总投资k€':>9}{'首年净现金':>10}{'首年收益率%':>10}{'IRR%':>7}{'回收期':>7}{'NPV@6%':>9}")
    out={}
    for k,v in SCENARIOS.items():
        r=run(v); out[k]=r
        print(f"{k:<46}{r['capex']:>9}{r['y1']['cf']:>10}{r['yield_y1']:>10}{str(r['irr']):>7}{str(r['payback']):>7}{r['npv6']:>9}")
    b=out['V4 别墅 + 光储 + 3 台 HGX H200']
    print('\nV4 投资构成 k€:',{k:b[k] for k in ['capex_house','capex_pv','capex_ess','capex_it']})
    for r in b['rows']: print(r)
    print('\n=== 单台 8×H200 算力资产 5 年 IRR ===')
    cases={
     '基准：实收 $2.6(€2.4)/GPU·h、利用率 55%、年降 18%':dict(),
     '保守：$2.25、40%':dict(price=1.95,util=0.40),
     '乐观：$3.75、70%、年降 10%':dict(price=3.25,util=0.70,decline=0.10),
     '乐观 + ACCIÓ 10% 补贴':dict(price=3.25,util=0.70,decline=0.10,subsidy=36.0),
     '集团自用替代云成本（等效 $3.5、利用率 65%、无销售成本）':dict(price=3.0,util=0.65,decline=0.10,opex=6.0),
     '3 年闭口合同 $3.0 固定、利用率 100%（企业客户，需 T3 机房）':dict(price=2.6,util=1.0,decline=0.0,room=90.0),
     '集中站（terciario 用地）：分摊机房 40、运维 8、专线 3、6.1TD 电价 0.10':dict(room=40.0,opex=8.0,net=3.0,elec=0.10),
     '集中站 + 3 年闭口 $3.0、100%':dict(room=40.0,opex=8.0,net=3.0,elec=0.10,price=2.6,util=1.0,decline=0.0),
    }
    for k,v in cases.items():
        r,cfs=compute_only(**v); print(f"{k:<52} IRR={None if r is None else round(r*100,1)}%  现金流={[round(c) for c in cfs]}")
    print('\n=== 达到目标 IRR 所需实收价 €/GPU·h ===')
    for label,kw in [('别墅节点（利用率 55%、年降 18%）',dict()),('别墅节点闭口合同（100%、年降 0）',dict(util=1.0,decline=0.0))]:
        print(label,{f'IRR{t}%':breakeven_price(t/100,**kw) for t in (6,10,15)})
    pass


# ---------- Montgat 10 套别墅社区（k€，10 年） ----------
def community(n=10, sell=7, sale_price=1150.0, land=250.0, build=640.0, rent_month=3.8, occ=0.9, opex_ratio=0.2,
              pv_kwp_house=12.0, pv_eur_wp=1.1, pv_yield=1500, ess_kwh_house=30.0, ess_eur_kwh=0.6, ess_civil=8.0,
              station_servers=0, server_capex=300.0, station_civil=0.0, station_me_per_server=40.0,
              price=2.6, util=0.55, decline=0.18, kw=7.0, pue=1.2, elec=0.10, opex_per_server=8.0, net=3.0,
              subsidy=0.0, horizon=10, server_life=5, salvage=0.10, grid_price=0.20, surplus=0.05):
    hold=n-sell
    capex_house=n*(land+build)
    capex_pv=n*pv_kwp_house*pv_eur_wp
    capex_ess=n*(ess_kwh_house*ess_eur_kwh+ess_civil)
    capex_it=station_servers*server_capex+station_civil+station_servers*station_me_per_server
    capex=capex_house+capex_pv+capex_ess+capex_it
    cfs=[-(capex-subsidy)+sell*sale_price*0.0]   # 预售回款在第1年计入
    rows=[]
    for y in range(1,horizon+1):
        sales=sell*sale_price if y==1 else 0
        house=hold*rent_month*12*occ*(1-opex_ratio)*(1.02**(y-1))
        gen=n*pv_kwp_house*pv_yield*(1-0.005)**(y-1)
        it_kwh=station_servers*kw*pue*8760
        self_kwh=min(gen, gen*0.7+it_kwh) if station_servers>0 else gen*0.7
        # 出售的别墅光储归业主：只计自持部分+算力站消纳
        pv=(min(self_kwh,gen)*grid_price*(hold/n)+(gen-self_kwh)*surplus*(hold/n))/1000
        gen_idx=(y-1)//server_life
        p=price*(0.75**gen_idx)*(1-decline)**((y-1)%server_life)
        it_inc=station_servers*8*p*8760*util/1000
        it_cost=(max(it_kwh-gen*(1-0.7),0)*elec/1000+station_servers*opex_per_server+net) if station_servers>0 else 0
        reinv=0
        if station_servers>0 and y>1 and (y-1)%server_life==0:
            reinv=station_servers*server_capex*(0.7**gen_idx)-station_servers*server_capex*salvage*(0.7**(gen_idx-1))
        cf=sales+house+pv+it_inc-it_cost-reinv
        if y==horizon: cf+=hold*(land+build)+(station_servers*server_capex*salvage*(0.7**gen_idx) if station_servers>0 else 0)
        cfs.append(cf); rows.append((y,round(sales),round(house),round(pv),round(it_inc-it_cost),round(reinv),round(cf)))
    r=irr(cfs)
    return dict(capex=round(capex),subsidy=subsidy,capex_house=capex_house,capex_pv=round(capex_pv),capex_ess=round(capex_ess),capex_it=round(capex_it),
                irr=None if r is None else round(r*100,1),npv6=round(npv(cfs,0.06)),rows=rows)

CCASES={
 'M0 10 套全部自持出租，光储，无算力':dict(sell=0),
 'M1 售 7 持 3，光储，无算力':dict(),
 'M2 M1 + 1 台 H200 试点（自持别墅内，方案 B 弱化）':dict(station_servers=1,station_me_per_server=60.0,opex_per_server=12.0,net=6.0,elec=0.13),
 'M3 M1 + 集中站 8 台 H200（terciario 用地，≈100 kW IT）':dict(station_servers=8,station_civil=250.0),
 'M3o M3 乐观：$3.75、70%、年降 10%':dict(station_servers=8,station_civil=250.0,price=3.25,util=0.70,decline=0.10),
 'M3c M3 + 3 年闭口 $3.0 固定 100% + ACCIÓ 10%':dict(station_servers=8,station_civil=250.0,price=2.6,util=1.0,decline=0.0,subsidy=290.0),
 'M3p M3 悲观：$2.25、40%':dict(station_servers=8,station_civil=250.0,price=1.95,util=0.40),
}
if __name__=='__main__':
    print('\n=== Montgat 10 套社区（k€，10 年）===')
    print(f"{'情景':<52}{'总投资':>8}{'IRR%':>7}{'NPV@6%':>9}")
    for k,v in CCASES.items():
        r=community(**v); print(f"{k:<52}{r['capex']:>8}{str(r['irr']):>7}{r['npv6']:>9}")
    b=community(**CCASES['M3c M3 + 3 年闭口 $3.0 固定 100% + ACCIÓ 10%'])
    print('M3c 构成:',{k:b[k] for k in ['capex_house','capex_pv','capex_ess','capex_it']})
    for r in b['rows']: print(r)
