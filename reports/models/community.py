"""社区级模型：100栋低密住宅 + 社区能源算力站（商业配套用地）。金额：万元。"""
from model import irr, payback

def community(n=100, sell_ratio=0.0, sale_price=520.0, land=180, build=200,
              rent=1.2, occ=0.85, opex_ratio=0.15,
              pv_kw_house=20, pv_kw_carport=1000, pv_price=0.28, pv_hours=1100,
              ess_kwh=2000, ess_price=0.11, ess_spread=0.6, ess_cycles=330,
              it_mw=1.0, server_kw=5.0, server_price=115, rent_server=2.6, util=0.9, decline=0.0,
              pue=1.2, station_civil=1500, station_me_per_kw=0.6,  # 机电 6000元/kW IT
              elec=0.65, opex_station=250, net_station=60,
              sub_building=0.0, sub_capex_ratio=0.0, sub_voucher_ratio=0.0,
              horizon=10, house_terminal=1.0, server_life=5):
    n_hold=n*(1-sell_ratio); n_sell=n*sell_ratio
    capex_house=n*(land+build)
    pv_kw=n*pv_kw_house+pv_kw_carport
    capex_pv=pv_kw*pv_price; capex_ess=ess_kwh*ess_price
    servers=int(it_mw*1000/server_kw)
    capex_srv=servers*server_price
    capex_station=station_civil+it_mw*1000*station_me_per_kw
    capex=capex_house+capex_pv+capex_ess+capex_srv+capex_station
    subsidy=sub_building+sub_capex_ratio*(capex_srv+capex_station+capex_pv+capex_ess)
    cfs=[-(capex-subsidy)+n_sell*sale_price]
    rows=[]
    for y in range(1,horizon+1):
        house=n_hold*rent*12*occ*(1-opex_ratio)*(1.02**(y-1))
        gen=pv_kw*pv_hours*(1-0.006)**(y-1)/1e4  # 万kWh
        it_kwh=it_mw*1000*pue*util*8760/1e4
        pv_val=min(gen,it_kwh)*elec + max(gen-it_kwh,0)*0.3 - pv_kw*0.003
        ess_val=ess_kwh*0.9*ess_cycles*ess_spread*0.88/1e4*(1-0.02)**(y-1) - ess_kwh*0.0005
        gen_idx=(y-1)//server_life
        it_income=servers*rent_server*12*util*(0.7**gen_idx)*(1-decline)**((y-1)%server_life)*(1+sub_voucher_ratio)
        it_cost=max(it_kwh-gen,0)*elec+opex_station+net_station
        reinvest=0
        if y>1 and (y-1)%server_life==0:
            reinvest=capex_srv*(0.7**gen_idx)-capex_srv*0.1*(0.7**(gen_idx-1))
        cf=house+pv_val+ess_val+it_income-it_cost-reinvest
        if y==horizon: cf+=capex_house*(1-sell_ratio)*house_terminal + capex_srv*0.1*(0.7**gen_idx)
        cfs.append(cf); rows.append((y,round(house),round(pv_val),round(ess_val),round(it_income-it_cost),round(reinvest),round(cf)))
    r=irr(cfs)
    npv8=round(sum(cf/(1.08**t) for t,cf in enumerate(cfs)))
    return dict(npv8=npv8,capex=round(capex),subsidy=round(subsidy),servers=servers,capex_house=round(capex_house),capex_pv=round(capex_pv),capex_ess=round(capex_ess),capex_srv=round(capex_srv),capex_station=round(capex_station),
                equity0=round(-cfs[0]),y1=rows[0],irr=None if r is None else round(r*100,1),payback=None if payback(cfs) is None else round(payback(cfs),1),rows=rows)

CASES={
 'C1 全部自持，无补贴，市场化租金':dict(),
 'C2 全部自持 + 补贴（建筑300元/㎡=900万；设备补贴20%；算力券抬价15%）':dict(sub_building=900,sub_capex_ratio=0.2,sub_voucher_ratio=0.15),
 'C3 出售70%别墅回笼资金，自持30%+能源算力站，含补贴':dict(sell_ratio=0.7,sub_building=900,sub_capex_ratio=0.2,sub_voucher_ratio=0.15),
 'C4 C3 + 算力站扩到2MW':dict(sell_ratio=0.7,sub_building=900,sub_capex_ratio=0.2,sub_voucher_ratio=0.15,it_mw=2.0,pv_kw_carport=2000,opex_station=400),
 'C5 C3 悲观：租金1.8/出租率65%/年降15%/无算力券':dict(sell_ratio=0.7,sub_building=900,sub_capex_ratio=0.2,rent_server=1.8,util=0.65,decline=0.15),
 'C6 只做地产+光储（不建算力站），出售70%':dict(sell_ratio=0.7,it_mw=0.001,station_civil=0,station_me_per_kw=0,opex_station=0,net_station=0,sub_building=900,sub_capex_ratio=0.2),
}
if __name__=='__main__':
    print(f"{'情景':<62}{'总投资':>7}{'补贴':>6}{'台数':>5}{'首年净现金':>9}{'IRR%':>7}{'回收期':>7}{'NPV@8%':>9}")
    for k,v in CASES.items():
        r=community(**v)
        print(f"{k:<62}{r['capex']:>7}{r['subsidy']:>6}{r['servers']:>5}{r['y1'][6]:>9}{str(r['irr']):>7}{str(r['payback']):>7}{r['npv8']:>9}")
    b=community(**CASES['C3 出售70%别墅回笼资金，自持30%+能源算力站，含补贴'])
    print('\nC3 投资构成:',{k:b[k] for k in ['capex_house','capex_pv','capex_ess','capex_srv','capex_station','subsidy','equity0']})
    print('C3 年度: (年,房租净,光伏,储能,算力净,再投资,合计)')
    for r in b['rows']: print(r)
    b=community(**CASES['C1 全部自持，无补贴，市场化租金'])
    print('\nC1 投资构成:',{k:b[k] for k in ['capex_house','capex_pv','capex_ess','capex_srv','capex_station','subsidy','equity0']})
    print('C1 年度:'); 
    for r in b['rows']: print(r)
