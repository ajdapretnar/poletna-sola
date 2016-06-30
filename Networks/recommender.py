# encoding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import os
from nmf import NMF


try:
    datapath = os.path.join("data", sys.argv[1])
    assert os.path.exists(datapath)
except:
    print("Enostaven priporočilni sistem. ")
    print()
    print("Uporaba:")
    print("\t %s <datoteka s podatki >" % sys.argv[0])
    print()
    print("Primer:")
    print("\t %s vprasalnik.txt " % sys.argv[0])
    quit(1)




# Parametri vprasalnik
if sys.argv[1] == "vprasalnik.txt":
    k = 5                       # Stevilo priporocil
    rank = 3                    # Dimenzija modela
    eta = 1e-3                  # Ucni korak
    max_iter = 500              # Stevilo iteracij
    compute_error=True          # Izracun napake
    symmetric=False             # Simetircni podatki: NE
    min_prior_connections = 1   # Minimalni stevilo povezav, da je neko vozlisce priporoceno
elif sys.argv[1] == "euro2016.processed.txt":
    # Parametri Euro
    k = 10                       # Stevilo priporocil
    rank = 10                   # Dimenzija modela
    eta = 1e-2                  # Ucni korak
    max_iter = 500              # Stevilo iteracij
    compute_error=True          # Izracun napake
    symmetric=True              # Simetircni podatki: DA
    min_prior_connections = 2   # Minimalni stevilo povezav, da je neko vozlisce priporoceno
else:
    # Parametri GoT
    k = 5                       # Stevilo priporocil
    rank = 5                    # Dimenzija modela
    eta = 1e-3                  # Ucni korak
    max_iter = 500              # Stevilo iteracij
    compute_error=True          # Izracun napake
    symmetric=True              # Simetircni podatki: DA
    min_prior_connections = 1   # Minimalni stevilo povezav, da je neko vozlisce priporoceno



X = np.loadtxt(open(datapath, encoding="utf-8"), skiprows=1, delimiter=",")
naslovi = csv.DictReader(open(datapath, encoding="utf-8"), delimiter=",").fieldnames


print("Prilagajanje modela podatkom ...")
model = NMF(compute_error=compute_error, rank=rank, eta=eta, max_iter=max_iter,
            symmetric=symmetric)
model.fit(X)
Xp = model.predict_all()
print("Učenje koncano!")

Y = X.copy()
f, axes = plt.subplots(ncols=2, nrows=1, figsize=(20, 10))
axes[0].set_xlabel("Vozlisce")
axes[0].set_ylabel("Vozlisce")
axes[1].set_xlabel("Vozlisce")
axes[0].pcolor(Y, cmap='Oranges', vmin=0, vmax=X.max())
axes[0].set_title("Podatki")

axes[1].pcolor(Xp, cmap='Oranges', vmin=0, vmax=X.max())
axes[1].set_title("Model")
axes[1].set_xlim(0, X.shape[1])
axes[1].set_ylim(0, X.shape[0])
axes[0].set_xlim(0, X.shape[1])
axes[0].set_ylim(0, X.shape[0])
basename = os.path.splitext(os.path.basename(datapath))[0]
fout=os.path.join("results", "%s_model.png" % basename)
plt.savefig(fout, dpi=150)
plt.close()
print("Slika podatkov shranjena v %s." % fout)


while True:
    try:
        i = input("Vnesi št. ali ime uporabnika/vozlišča (-1 za izhod): ")
        if i in naslovi:
            i = naslovi.index(i)
        else:
            i = int(i)
        if i == -1:
            print("Izhod")
            quit(1)
        seznam = model.recommend(i=i, X=X, k=k, min_c = min_prior_connections)
    except:
        print("Napačen vnos.")
        print()
    else:
        print("Do %d najprimernejsih priporocil/povezav:" % k)
        for j, l in enumerate(seznam):
            print("\t%d. %s (napovedana ocena: %.3f)" % (j+1,naslovi[l], Xp[i, l] ))
        print()
