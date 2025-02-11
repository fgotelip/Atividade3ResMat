import sympy as sp

x = sp.symbols('x')

def gera_wx(carga1, carga2,x1,x2):
    tam=x2-x1
    if carga1 == carga2:
        w = carga1
    elif carga1 == 0:
        carga = carga1 + carga2
        w = (carga/tam)*x
    elif carga2 == 0:
        carga = carga1 + carga2
        w = carga - (carga/tam)*x
    elif carga2 > carga1:
        carga = abs(carga1 - carga2)
        w = (carga/tam)*x + min(carga1,carga2)
    else:
        carga = abs(carga1 - carga2)
        w = - (carga/tam)*x + max(carga1,carga2)
    return w

def gera_vx(w,vant,tam):
    if isinstance(vant,sp.Basic):
        vant = vant.subs(x,tam)
    v = sp.integrate(-w,x) + vant
    return v

def gera_mx(v,mant,tam):
    if isinstance(mant,sp.Basic):
        mant = mant.subs(x,tam)
    
    m = sp.integrate(v,x) + mant
    return m

def gera_esforcos(carga1,carga2,x1,x2,vant,mant,x1ant):
    w = gera_wx(carga1,carga2,x1,x2)
    v = gera_vx(w,vant,x1-x1ant)
    m = gera_mx(v,mant,x1-x1ant)
    return v,m










