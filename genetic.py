import random

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


from itertools import repeat
from collections import Sequence

def mutCustom(individual, mu, sigma, indpb):

    size = len(individual)


    #custom part
    degisim=1
    ileri=random.randint(0,1)
    if(ileri==1):
        s=random.randint(0,12-2)
        individual[s] -=degisim
        individual[s+1] +=degisim
    else:
        s=random.randint(1,12-1)
        individual[s] -=degisim
        individual[s-1] +=degisim       
    #custom part end
        
    if not isinstance(mu, Sequence):
        mu = repeat(mu, size)
    elif len(mu) < size:
        raise IndexError("mu must be at least the size of individual: %d < %d" % (len(mu), size))
    if not isinstance(sigma, Sequence):
        sigma = repeat(sigma, size)
    elif len(sigma) < size:
        raise IndexError("sigma must be at least the size of individual: %d < %d" % (len(sigma), size))
    
    for i, m, s in zip(range(size), mu, sigma):
        if random.random() < indpb:
            individual[i] += random.gauss(m, s)
    
    return individual,


def cxCustom(ind1, ind2):
    size = 12 #min(len(ind1), len(ind2))
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
   
    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
        = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]

    ind1[12+cxpoint1:12+cxpoint2], ind2[12+cxpoint1:12+cxpoint2] \
        = ind2[12+cxpoint1:12+cxpoint2], ind1[12+cxpoint1:12+cxpoint2]

    ind1[24+cxpoint1:24+cxpoint2], ind2[24+cxpoint1:24+cxpoint2] \
        = ind2[24+cxpoint1:24+cxpoint2], ind1[24+cxpoint1:24+cxpoint2]
    return ind1, ind2

def cxCustomOne(ind1, ind2):
    size = 12
    cxpoint = random.randint(1, size - 1)
    ind1[cxpoint:12], ind2[cxpoint:12] = ind2[cxpoint:12], ind1[cxpoint:12]
    ind1[12+cxpoint:24], ind2[12+cxpoint:24] = ind2[12+cxpoint:24], ind1[12+cxpoint:24]
    ind1[24+cxpoint:36], ind2[24+cxpoint:36] = ind2[24+cxpoint:36], ind1[24+cxpoint:36]
    
    return ind1, ind2
   
    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
        = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]

    ind1[12+cxpoint1:12+cxpoint2], ind2[12+cxpoint1:12+cxpoint2] \
        = ind2[12+cxpoint1:12+cxpoint2], ind1[12+cxpoint1:12+cxpoint2]

    ind1[24+cxpoint1:24+cxpoint2], ind2[24+cxpoint1:24+cxpoint2] \
        = ind2[24+cxpoint1:24+cxpoint2], ind1[24+cxpoint1:24+cxpoint2]
    return ind1, ind2

#uretim gunu sayisi
aylik_uretim_gunu = [22,20,23,19,22,22,20,23,11,22,22,18]
#birikimli talep ve guvenlik stogu miktari
yedinci_sutun = [7800,11500,15500,20800,28200,37500,49100,57500,63600,69400,74300,79300]

#maliyetler
m_elde_bulundurma=51
m_elde_bulundurmama=342
m_isgucu_degistirme=200
m_fazla_mesai=10
m_fason_uretim=15

#kisitlar
#TODO 350 yap
normal_mesai_kapasite=350
fazla_mesai_kapasite=60
baslangic_stogu=2800


print("starting...")


def evalPlan(plan,verbose=False):
    #sanitize, kısıtları uygula
    for i in range(0,12):
        plan[i]=round(plan[i])
    for i in range(12,24):
        plan[i]=abs(round(plan[i]))
        if(plan[i]>fazla_mesai_kapasite):
            plan[i]=fazla_mesai_kapasite
    for i in range(24,36):
        plan[i]=abs(round(plan[i]))
    
    uretim_hizi_degistirme=plan[:12]
    fazla_mesai_uretim_gunluk=plan[12:24]
    fason_uretim_gunluk=plan[24:]

#uretim miktari hesaplari:
#uretim hizi (o ay icin gunluk)
    uretim_hizi= []
#toplam uretim hizi degistirme miktari
    toplam_uretim_hizi_degistirme=0
#fazla mesaide uretilen toplam urun
    fazla_mesaide_uretilen_toplam=0
#fason uretimle uretilen toplam urun
    fason_uretim_toplam=0
    
    normal_mesai_uretim_hizi=normal_mesai_kapasite #normal mesai kapasite
    for i in range(12):
        #if(uretim_hizi_degistirme[i]!=0):
        normal_mesai_uretim_hizi+=uretim_hizi_degistirme[i]
        if(normal_mesai_uretim_hizi>350):
            normal_mesai_uretim_hizi=350
            if(verbose):
                print("normal mesai kapasitesi düzeltildi, ay:",i)
        if(i!=0):
            toplam_uretim_hizi_degistirme+=abs(uretim_hizi_degistirme[i])

        fazla_mesaide_uretilen_toplam+=fazla_mesai_uretim_gunluk[i]*aylik_uretim_gunu[i]
        fason_uretim_toplam+=fason_uretim_gunluk[i]*aylik_uretim_gunu[i]

        uretim_hizi.append(normal_mesai_uretim_hizi+fazla_mesai_uretim_gunluk[i]+fason_uretim_gunluk[i])


    if(verbose):
        print("toplam uretim hizi degistirme")
        print(toplam_uretim_hizi_degistirme)
        print("fazla mesaide toplam")
        print(fazla_mesaide_uretilen_toplam)
        print("fason uretilen toplam")
        print(fason_uretim_toplam)
        print("sonuc uretim hizi")
        print(uretim_hizi)

#stok hesaplarini yapalim
#birikimli uretim miktari
    birikimli_uretim_miktari=[]
#ikinci_yedinci_sutun
    ikinci_yedinci_sutun=[]
    for i in range(12):
        aylik_uretim_miktari=uretim_hizi[i]*aylik_uretim_gunu[i]
        if i==0:
            birikimli_uretim_temp=aylik_uretim_miktari+baslangic_stogu
        else:
            birikimli_uretim_temp=aylik_uretim_miktari+birikimli_uretim_miktari[i-1]
        birikimli_uretim_miktari.append(birikimli_uretim_temp)
        aylik_stok=birikimli_uretim_temp-yedinci_sutun[i]
        ikinci_yedinci_sutun.append(aylik_uretim_gunu[i]*aylik_stok)

    if(verbose):
        print("birikimli uretim miktari")
        print(birikimli_uretim_miktari)
        print("ikinci_yedinci_sutun")
        print(ikinci_yedinci_sutun)



#toplam maliyet hesaplari
#    uretim_hizini_degistirme_maliyeti=
    m1=toplam_uretim_hizi_degistirme*m_isgucu_degistirme
#   fazla mesai maliyeti
    m2=fazla_mesaide_uretilen_toplam*m_fazla_mesai
#   fason uretim maliyeti
    m3=fason_uretim_toplam*m_fason_uretim
#   elde bulundurma / bulundurmama
    toplam_stok_elde=0
    toplam_ay_elde=0
    toplam_gun_elde=0
    toplam_stok_yok=0
    toplam_ay_yok=0
    toplam_gun_yok=0
    for i in range(12):
        s=ikinci_yedinci_sutun[i]
        if(s>0):
            toplam_ay_elde+= 1
            toplam_stok_elde+=s
            toplam_gun_elde+=aylik_uretim_gunu[i]
        if(s<0):
            toplam_ay_yok+= 1
            toplam_stok_yok += abs(s)
            toplam_gun_yok+=aylik_uretim_gunu[i]

    m4=0
    if(toplam_ay_elde>0):
        m4=(toplam_stok_elde/toplam_gun_elde)*(toplam_ay_elde/12)*m_elde_bulundurma
        if(verbose):
            print("toplam_gun_elde:",toplam_gun_elde,"toplam_stok_elde:",toplam_stok_elde)
            print("toplam_ay_elde:",toplam_ay_elde)
    m5=0
    if(toplam_ay_yok>0):
        m5=(toplam_stok_yok/toplam_gun_yok)*(toplam_ay_yok/12)*m_elde_bulundurmama
        if(verbose):
            print("toplam_gun_yok:",toplam_gun_yok,"toplam_stok_yok:",toplam_stok_yok)
            print("toplam_ay_yok:",toplam_ay_yok)

    maliyet=m1+m2+m3+m4+m5
    if(verbose):
        print("*maliyetler")
        print(m1,m2,m3,m4,m5)
        print("*toplam")
        print(maliyet)
    return maliyet,  #this means return tuple with one element




hof= tools.HallOfFame(1)

def getNewPlan():

    ind=[-122, 0, 9, 97, 16, 0, 0, 0, 0, -86, -17, 0, 0, 0, 0, 0, 0, 60, 60, 60, 60, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 51, 0, 0, 0]

    return mutCustom(ind,mu=0,sigma=1,indpb=0.3)[0]

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual , getNewPlan )
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalPlan)
toolbox.register("mate", cxCustomOne)
toolbox.register("mutate", mutCustom, mu=0,sigma=1,indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=10)

    

def main():

    file=open("results.txt","a")
    
    '''    plan2=[0,0,0,120,0,0, 0,0,0,-120,0,0,
          0,0,0,56,56,56, 56,56,0,0,0,23,
          0,0,0,0,0,0, 0,0,0,0,0,0]
    print(evalPlan(plan2))
'''
    plan= [-145, 26, 69, 33, 16, 0, 1, 0, -1, -32, -69, 0,
   20,  0,  0,  1,  1, 8,44,26, 60,   0,   0, 0,
   2,   0,  0,  0,  0, 0, 0, 0, 15,   0,   0, 0]



    
    print(evalPlan(plan,verbose=True))
    #return





    pop = toolbox.population(n=500)
    
    hof= tools.HallOfFame(1)


    print(pop[0])

    #deap.algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen[, stats, halloffame, verbose])
    #algorithms.eaSimple(pop, toolbox, 0.4, 0.8,1000, halloffame=hof,verbose=True)
    algorithms.eaMuPlusLambda(pop,toolbox,50,300,   0.5, 0.5 ,  1000  , halloffame=hof)
    

    print(hof)
    print(hof,file=file)


    print("***best plan results")
    evalPlan(hof[0],verbose=True) 
    print(evalPlan(hof[0]),file=file)
    



main()
