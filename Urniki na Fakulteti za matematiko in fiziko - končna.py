import re
import requests
import matplotlib.pyplot as plt
import math

print('Pozdravljeni v programu za statistično obdelavo urnikov Oddelka za matematiko Fakultete za matematiko in fiziko Univerze v Ljubljani.')
print()
print('Branje podatkov iz spleta. Prosimo počakajte. Postopek traja približno 2 minuti.')
print()

####################################################################################################################################
#Branje podatkov iz spleta
#Avtor: Luka Šešet
####################################################################################################################################


# Funkcije za pridobivanje povezav, in urejanje le teh po
# pravilnih semestrih in programih (ker se stil povezave za tekoči urnik
# malo razlikuje od preteklih sem naredil posebej funkcije za trenutni in pretekle semestre):
'--------------------------------------------------------------------------------------------------------------------------------------------'

def seznam_koncnic_povezav_za_tekoce_leto():
    
    '''
        Vrne seznam oblike [končnica_1, ... , končnica_n],
        kjer je končnica_i oblike '/letnik/stevilo/'.
        Končnice bomo kasneje potrebovali pri
        zbiranju celotnega naslova za urnik.
    '''

    naslov = 'https://urnik.fmf.uni-lj.si'
    stran = requests.get(naslov).text
    stran = re.split(r'<div class="col s6 m3">', stran)[1]
    regularniIzraz = r'<a href=".*">.*</a>'
    iskanje = re.findall(regularniIzraz, stran)
    koncni_seznam = []
    for vrstica in iskanje:
        vrstica_ki_jo_dodamo = re.split(r'<a href="', vrstica)[1]
        koncni_seznam.append(re.split(r'">.*</a>', vrstica_ki_jo_dodamo)[0])
    return koncni_seznam


def slovar_povezav_za_tekoce_leto(): 

    '''
        Vrne slovar oblike:

        {
         Trenutni_semester:
            {
             Program_1:
                {1. letnik: 'spletni_naslov', ... , n. letnik: 'spletni_naslov'},
             ...,
             Program_n:
                {1. letnik: 'spletni_naslov', ... , n. letnik: 'spletni_naslov'}
             }
          }
          
        S takim slovarjem lahko potem zlahka poberemo podatke za določen program.
    '''
    
    koncni_slovar = dict()
    for koncnica in seznam_koncnic_povezav_za_tekoce_leto():
        # Pridobimo informacije o programu in letniku
        naslov = 'https://urnik.fmf.uni-lj.si' + koncnica
        stran = requests.get(naslov).text
        regularniIzraz = r'(<title>)(.*)(</title>)'
        iskanje = re.findall(regularniIzraz, stran)
        if iskanje != []:
            # Preuredimo podatke in jih ustrezno postavimo v slovar
            program = iskanje[0][1]
            leto = program[-24:]
            odrezano = program[13:-27] 
            odrezano = odrezano.split(',')
            if odrezano[0] not in koncni_slovar:
                koncni_slovar[odrezano[0]] = {odrezano[1][1:]:naslov}
            else:
                koncni_slovar[odrezano[0]].update({odrezano[1][1:]:naslov})
    return {leto:koncni_slovar}


def slovar_povezav_i_semestra(seznam_koncnic, i):
    
    '''
        Vrne slovar oblike:

        {
         Semester_i:
            {
             Program_1:
                {1. letnik: 'spletni_naslov', ... , n. letnik: 'spletni_naslov'},
             ...,
             Program_n:
                {1. letnik: 'spletni_naslov', ... , n. letnik: 'spletni_naslov'}
             }
          }
          
        S takim slovarjem lahko potem zlahka poberemo podatke za določen program.
        Deluje zelo podobno, kot funkcija za letošnji semester, vendar zaradi
        razlike v dolžini besede 'Zimski semester' in 'Poletni semester' obdeluje
        podatke malo drugače.
    '''
    koncni_slovar = dict()
    for koncnica in seznam_koncnic: 
        naslov = 'https://urnik.fmf.uni-lj.si' + koncnica
        stran = requests.get(naslov).text
        regularniIzraz = r'(<title>)(.*)(</title>)'
        iskanje = re.findall(regularniIzraz, stran)
        if iskanje != []:
            # Ustrezno preuredimo podatke in jih damo v slovar
            program = iskanje[0][1]
            if i % 2 == 0:
                leto = program[-24:]
                odrezano = program[13:-27]
                odrezano = odrezano.split(',')
            else:
                leto = program[-23:]
                odrezano = program[13:-26] 
                odrezano = odrezano.split(',')
            if odrezano[0] not in koncni_slovar:
                koncni_slovar[odrezano[0]] = {odrezano[1][1:]:naslov}
            else:
                koncni_slovar[odrezano[0]].update({odrezano[1][1:]:naslov})
    return {leto:koncni_slovar}


def slovar_povezav_za_pretekla_leta():

    '''
        Vrne slovar oblike:

        {
         Semester_1:
            {
             Program_1:
                {1. letnik: 'spletni_naslov', ... , n. letnik: 'spletni_naslov'},
             ...,
             Program_n:
                {1. letnik: 'spletni_naslov', ... , n. letnik: 'spletni_naslov'}
             },
        ...,
        Semester_n:
            {
             Program_1:
                {1. letnik: 'spletni_naslov', ... , n. letnik: 'spletni_naslov'},
             ...,
             Program_n:
                {1. letnik: 'spletni_naslov', ... , n. letnik: 'spletni_naslov'}
             }
          }
          
        S takim slovarjem lahko potem zlahka poberemo podatke za določen program.
    '''
    
    slovar_preteklih_povezav = dict()
    for i in range(1, 6):
        # i je v takih mejah, ker je trenutno objavljeno 5 preteklih semsetrov.
        seznam_koncnic = []
        naslov = 'https://urnik.fmf.uni-lj.si/semester/' + str(i) + '/'
        stran = requests.get(naslov).text
        stran  = re.split(r'<div class="col s6 m3">', stran)[1]
        regularniIzraz = r'<a href=".*">.*</a>'
        iskanje = re.findall(regularniIzraz, stran)
        for vrstica in iskanje:
            # Ustvarimo seznam končnic povezav i-ti semester.
            vrstica_ki_jo_dodamo = re.split(r'<a href="',vrstica)[1]
            seznam_koncnic.append(re.split(r'">.*</a>',vrstica_ki_jo_dodamo)[0])
        # Pokličemo funkcijo, ki nam iz teh končnic ustvari slovar povezav za i-ti semester.
        slovar_preteklih_povezav.update(slovar_povezav_i_semestra(seznam_koncnic,i))
    return slovar_preteklih_povezav

'--------------------------------------------------------------------------------------------------------------------------------------------'
# Funkcije za pridobivanje podatkov:
'--------------------------------------------------------------------------------------------------------------------------------------------'

def podatki_za_teden(naslov):

    '''
        Vrne seznam oblike [[parametri, predmet_1], ... ,[parametri, predmet_n]].
        Parametri so opisani v predhodnji funkciji.
    '''
    
    tedenski_urnik = []
    stran = requests.get(naslov).text
    stran  = re.split(r'<div id="srecanja" class="poravnaj-na-termine">', stran)[1]
    stran = re.split(r'<div class="vertical-space hide-on-med-and-up"></div>', stran)[0]
    stran = re.split(r'</div>\n</div>', stran)
    for i in range(0, len(stran) - 1):
        parameter_in_predmet = pari_parametrov_in_predmeta(stran[i])
        #Termine kolokvijev ne obravnavamo kot predmete
        if 'Kolokvij' not in parameter_in_predmet[1] and 'KOLOKVIJ' not in parameter_in_predmet[1]: 
            tedenski_urnik.append(parameter_in_predmet)
    return tedenski_urnik

def pari_parametrov_in_predmeta(neurejeno_besedilo):
    '''
        Iz neurejenega spletnega besedila izlušči in vrne
        par podatkov oblike [parametri, predmet].
        V parametrih so podatki o tem kje na spletni strani
        se nahaja naš predmet:
            'left: X%; width: Y%; top: Z%; height: U%'
        To nam bo pomagalo pri določanju na kateri dan in uro se izvaja.
    '''
    neurejeno_besedilo = re.sub(r'\n      \n        \n','',neurejeno_besedilo)
    neurejeno_besedilo = re.sub(r'\n      \n        \n','',neurejeno_besedilo)
    neurejeno_besedilo = re.sub(r'\n\n','',neurejeno_besedilo)
    neurejeno_besedilo = re.sub(r'\n','',neurejeno_besedilo)
    poisci_parametre = re.findall(r'<div class="srecanje-absolute-box .*" style=".*;"><div class=',neurejeno_besedilo)
    poisci_parametre = re.split(r';"><div class=',poisci_parametre[0])[0]
    parametri = re.split(r'<div class="srecanje-absolute-box .*" style="',poisci_parametre)[1]
    
    poisci_predmet = re.findall(r'<div class="srecanje" style="background: repeating-linear-gradient.*<a href=".*">.*</a>.*<span class="tip">', neurejeno_besedilo)
    poisci_predmet = re.findall(r'<a href=".*">.*</a>',poisci_predmet[0])[0]
    poisci_predmet = re.split(r'<a href=".*">',poisci_predmet)[1]
    poisci_predmet = re.split(r'</a>',poisci_predmet)[0]
    predmet = poisci_predmet.strip()
    
    return [parametri,predmet]

    
def vrne_vse_kar_rabis():
    '''
        Vrne slovar primeren za obdelovanje in analizo podatkov.
        Slovar je oblike:
        {Program_1:
                   {letnik_1:
                       {semester_1:
                           [[parametri, predmet], ... , [parametri, predmet]],
                        ...,
                        semester_n:
                           [[parametri, predmet], ... , [parametri, predmet]]
                        },
                    ...,
                    {letnik_n:
                       {semester_1:
                           [[parametri, predmet], ... , [parametri, predmet]],
                        ...,
                        semester_n:
                           [[parametri, predmet], ... , [parametri, predmet]]
                         }},
            ...,
            Program_n:
                   {letnik_1:
                       {semester_1:
                           [[parametri, predmet], ... , [parametri, predmet]],
                        ...,
                        semester_n:
                           [[parametri, predmet], ... , [parametri, predmet]]
                        },
                    ...,
                    {letnik_n:
                       {semester_1:
                           [[parametri, predmet], ... , [parametri, predmet]],
                        ...,
                        semester_n:
                           [[parametri, predmet], ... , [parametri, predmet]]
                         }}}
        Iz takšnega slovarja lahko zlahka razbiramo podatke.
    '''
    slovar_vseh_povezav = dict()
    vse_kar_rabis = dict()
    slovar_vseh_povezav = slovar_povezav_za_pretekla_leta()
    slovar_vseh_povezav.update(slovar_povezav_za_tekoce_leto())
    for keys1 in slovar_vseh_povezav:
        for keys2 in slovar_vseh_povezav[keys1]:
            for keys3 in slovar_vseh_povezav[keys1][keys2]:
                # Beremo podatke in jih dodajamo v slovar
                if keys2 not in vse_kar_rabis:
                        vse_kar_rabis[keys2] = {keys3:{keys1:podatki_za_teden(slovar_vseh_povezav[keys1][keys2][keys3])}}
                else:
                    if keys3 not in vse_kar_rabis[keys2]:
                        vse_kar_rabis[keys2].update({keys3:{keys1:podatki_za_teden(slovar_vseh_povezav[keys1][keys2][keys3])}})
                    else:
                        vse_kar_rabis[keys2][keys3].update({keys1:podatki_za_teden(slovar_vseh_povezav[keys1][keys2][keys3])})
    return vse_kar_rabis

####################################################################################################################################
#Statistični parametri in statistična obdelava
#Avtor: Denis Benčič
#Vir: Spletne učilnice FMF: Statistika (Praktična matematika, Jaka Smrekar) 
####################################################################################################################################

def moment(seznam, stopnja):
    '''Za dan številski seznam izračuna moment dane stopnje.'''
    vsota = 0
    for i in seznam:
        vsota = vsota + i ** stopnja
    return vsota / len(seznam)
    
def povprečje(seznam):
    '''Izračuna povprečje vrednosti danega številskega seznama.'''
    return moment(seznam, 1)

def centralniMoment(seznam, stopnja):
    '''Za dan številski seznam izračuna centralni moment dane stopnje.'''
    povprečjeSeznama = povprečje(seznam)
    vsota = 0
    for i in range(len(seznam)):
        if stopnja > 1:
            vsota = vsota + (i - povprečjeSeznama) ** stopnja
        elif stopnja == 1:
            vsota = vsota + abs(i - povprečjeSeznama)
    return vsota / len(seznam)

def standardniOdklon(seznam):
    '''Izračuna standardni odklon seznama.'''
    return math.sqrt(centralniMoment(seznam, 2))

def mediana(seznam):
    '''Določi mediano danega številskega seznama.'''
    urejenSeznam = [None] + sorted(seznam) #Za ustreznost indeksov dodamo None kot prvi element zaradi Pythonovega štetja od 0 dalje.
    dolžina = len(urejenSeznam) - 1 #None ne upoštevamo kot pravi element seznama
    if(dolžina % 2 == 0):
        return povprečje([urejenSeznam[dolžina // 2], urejenSeznam[dolžina // 2 + 1]])
    else:
        return urejenSeznam[(dolžina + 1) // 2]

def modus(seznam):
    '''Določi modus danega številskega seznama. Če se vsi elementi seznama pojavijo enako mnogokrat ali če je elementov, ki se pojavijo najpogosteje, več, vrne None.'''
    urejenSeznam = sorted(seznam)
    slovarPojavitev = dict() #Ključi predstavljajo elemente seznama, vrednosti pa njihovo število pojavitev
    seznamRazličnih = list(set(seznam)) #Tako se znebimo elementov, ki se podvajajo v seznamu
    for i in seznamRazličnih:
        slovarPojavitev[i] = urejenSeznam.count(i)
    if(len(set(slovarPojavitev.values())) == 1): #Vsi elementi seznami se pojavijo enako mnogokrat
        return None
    else:
        najpogosteje = max(list(slovarPojavitev.values()))
        if (list(slovarPojavitev.values())).count(najpogosteje) > 1: #Elementov, ki se pojavijo najpogosteje, je več
            return None
        else:
            obrnjenSlovar = dict((vrednost, ključ) for ključ, vrednost in slovarPojavitev.items())
            return obrnjenSlovar[najpogosteje]

def kvantil(seznam, delež):
    '''Vrne splošen kvantil danega številksega seznama za dan delež intervala (0, 1) z linearno interpolacijo.'''
    if(0 < delež < 1):
        urejenSeznam = [None] + sorted(seznam) #Za ustreznost indeksov dodamo None kot prvi element zaradi Pythonovega štetja od 0 dalje.
        dolžina = len(urejenSeznam) - 1 #None ne upoštevamo kot pravi element seznama
        kvantilniRang = dolžina * delež + 1 / 2
        kvantil = urejenSeznam[math.floor(kvantilniRang)] + (kvantilniRang - math.floor(kvantilniRang)) * (urejenSeznam[math.floor(kvantilniRang) + 1] - urejenSeznam[math.floor(kvantilniRang)])
        return kvantil

def variacijskiRazmik(seznam):
    '''Vrne variacijski razmik danega številskega seznama.'''
    return max(seznam) - min(seznam)

def interkvartilniRazmik(seznam):
    '''Vrne kvartilni razmik danega številskega seznama.'''
    return kvantil(seznam, 3 / 4) - kvantil(seznam, 1 / 4)

def koeficientAsimetričnosti(seznam):
    '''Vrne koeficient asimetričnosti danega številskega seznama.'''
    return centralniMoment(seznam, 3) / (standardniOdklon(seznam) ** 3)

def sploščenost(seznam):
    '''Vrne koeficient sploščenosti oz. kurtozis danega številskega seznama.'''
    return centralniMoment(seznam, 4) / (centralniMoment(seznam, 2) ** 2)

def ekscesnaSploščenost(seznam):
    '''Vrne koeficient ekscesne sploščenosti oz. ekscesne kurtozis danega številskega seznama.'''
    return sploščenost(seznam) - 3

####################################################################################################################################
#Statistična obdelava
#Avtor: Denis Benčič
####################################################################################################################################

def tabelaUrnika(slovar, smer, letnik, semester):
    '''Vrne tabelo urnika.'''
    return slovar[smer][letnik][semester]

def stUrZaPredmet(predmet):
    '''Za posamezen predmet v tabeli vrne, koliko ur je trajal.'''
    parametri = predmet[0]
    parametri = parametri.split(';')
    trajanje = parametri[3] #zanima nas 'height'
    trajanje = trajanje.split() #ločujem po presledku
    trajanje = trajanje[1] #zanima nas količina pred %
    trajanje = int(float((trajanje[:-1]))) #odstranimo % in postopno pretvorimo v celo število
    return trajanje // 7 #ker je 7 enota za eno uro
    
def DanPredmeta(predmet):
    '''Za posamezen predmet v tabeli vrne, katerega dne se je izvajal.'''
    parametri = predmet[0]
    parametri = parametri.split(';')
    trajanje = parametri[0] #zanima nas 'left'
    trajanje = trajanje.split() #ločujem po presledku
    trajanje = trajanje[1] #zanima nas količina pred %
    trajanje = int(float((trajanje[:-1]))) #odstranimo % in postopno pretvorimo v celo število
    if 0 <= trajanje < 20:
        return 'Ponedeljek'
    elif 20 <= trajanje < 40:
        return 'Torek'
    elif 40 <= trajanje < 60:
        return 'Sreda'
    elif 60 <= trajanje < 80:
        return 'Četrtek'
    elif 80 <= trajanje < 100:
        return 'Petek'
    
def SlovarUrZaDanVTednu(urnik):
    '''Za dano tabelo urnika vrne slovar, katerega ključi predstavljajo dneve v tednu, vrednosti pa pripadajoče število ur na ta dan.'''
    slovar = {'Ponedeljek' : 0, 'Torek' : 0, 'Sreda' : 0, 'Četrtek' : 0, 'Petek' : 0}
    for predmet in urnik:
        dan = DanPredmeta(predmet)
        slovar[dan] = slovar[dan] + stUrZaPredmet(predmet)
    return slovar

def ImePredmeta(predmet):
    '''Za posamezen predmet v tabeli vrne njegovo ime.'''
    return predmet[1]

def SlovarPredmetovPoUrahVTednu(urnik):
    '''Za dano tabelo urnika vrne slovar, katerega ključi predstavljajo po abecednem vrstnem redu urejene predmete, vrednosti pa pripadajoče število ur v tednu.'''
    slovar = {}
    for predmet in urnik:
        ime = ImePredmeta(predmet)
        if ime in slovar:
            slovar[ime] = slovar[ime] + stUrZaPredmet(predmet)
        else:
            slovar[ime] = stUrZaPredmet(predmet)
    #Vsa čast FMF urnikom za razlikovanje med Računalniškim Praktikumom in RP
    if 'Računalniški praktikum' and 'RP' in list(slovar.keys()):
        slovar['Računalniški praktikum'] = slovar['Računalniški praktikum'] + slovar['RP']
        del slovar['RP']
    return slovar
            
def NajboljPogostPredmet(slovar):
    '''V slovarju predmetov po urah v tednu vrne po tedenskem vrstnem redu prvo ime predmeta, ki je najbolj pogosto izvajan.'''
    najpogostejši = list(slovar.keys())[0] #začetna vrednost
    for predmet in slovar:
        if slovar[predmet] > slovar[najpogostejši]:
            najpogostejši = predmet
    return najpogostejši

def NajmanjPogostPredmet(slovar):
    '''V slovarju predmetov po urah v tednu vrne po tedenskem vrstnem redu prvo ime predmeta, ki je najmanj pogosto izvajan.'''
    najredkejši = list(slovar.keys())[0] #začetna vrednost
    for predmet in slovar:
        if slovar[predmet] < slovar[najredkejši]:
            najredkejši = predmet
    return najredkejši

####################################################################################################################################
#Glavni del programa
#Avtor: Denis Benčič
####################################################################################################################################

slovar = vrne_vse_kar_rabis()
print('Branje končano.')

prekini = False
nepravilenVnos = 'Nepravilen vnos. Poskusite znova.'

while not prekini:
    smer = None
    while smer not in slovar:
        print()
        print('Vnesite poljubno smer izmed naslednjih:')
        print()
        for i in list(slovar.keys()):
            print(i)
        print()
        smer = input()
        if smer not in slovar:
            print()
            print(nepravilenVnos)
    novSlovar = slovar[smer]
    letnik = None
    while letnik not in novSlovar:
        print()
        print('Vnesite poljuben letnik izmed naslednjih:')
        print()
        for i in list(novSlovar.keys()):
            print(i)
        print()
        letnik = input()
        if letnik not in novSlovar:
            print()
            print(nepravilenVnos)
    novSlovar = novSlovar[letnik]
    semester = None
    while semester not in novSlovar:
        print()
        print('Vnesite poljuben semester izmed naslednjih:')
        print()
        for semester in list(novSlovar.keys()):
            print(semester)
        print()
        semester = input()
        if semester not in novSlovar:
            print()
            print(nepravilenVnos)
    novSlovar = novSlovar[semester]
    print()
    urnik = novSlovar

    tabelaŠtevilaUr = list(SlovarUrZaDanVTednu(urnik).values())
    slovarPredmetov = SlovarPredmetovPoUrahVTednu(urnik)

    print("{0:>90s} | {1:s} {2:s}".format(smer, letnik, semester.lower()))
    print("{0:>90s} | {1:d}".format("Število tedensko izvajanih ur", sum(tabelaŠtevilaUr)))
    if sum(tabelaŠtevilaUr) > 0: #Nekateri urniki na spletu so tudi prazni
        print("{0:>90s} | {1:s}".format("Najbolj pogosto izvajan predmet", NajboljPogostPredmet(slovarPredmetov)))
        print("{0:>90s} | {1:s}".format("Najmanj pogosto izvajan predmet", NajmanjPogostPredmet(slovarPredmetov)))
        print("{0:>90s} | {1:f}".format("Povprečje dnevno izvajanih ur", povprečje(tabelaŠtevilaUr)))
        print("{0:>90s} | {1:f}".format("Standardni odklon", standardniOdklon(tabelaŠtevilaUr)))
        print("{0:>90s} | {1:s}".format("Modus", str(modus(tabelaŠtevilaUr))))
        print("{0:>90s} | {1:d}".format("Mediana", mediana(tabelaŠtevilaUr)))
        print("{0:>90s} | {1:f}".format("Prvi kvartil", kvantil(tabelaŠtevilaUr, 1 / 4)))
        print("{0:>90s} | {1:f}".format("Tretji kvartil", kvantil(tabelaŠtevilaUr, 3 / 4)))
        print("{0:>90s} | {1:f}".format("Interkvartilni razmik", interkvartilniRazmik(tabelaŠtevilaUr)))
        print("{0:>90s} | {1:d}".format("Variacijski razmik", variacijskiRazmik(tabelaŠtevilaUr)))
        print("{0:>90s} | {1:f}".format("Koeficient asimetričnosti", koeficientAsimetričnosti(tabelaŠtevilaUr)))
        print("{0:>90s} | {1:f}".format("Sploščenost", sploščenost(tabelaŠtevilaUr)))
        print("{0:>90s} | {1:f}".format("Ekscesna sploščenost", ekscesnaSploščenost(tabelaŠtevilaUr)))
      
        x1 = range(1,6)
        y1 = tabelaŠtevilaUr
  
        oznakeDni = list(SlovarUrZaDanVTednu(urnik).keys())
        barveDni = ['red','blue','green', 'yellow', 'purple']
   
        plt.bar(x1, y1, tick_label = oznakeDni, 
        width = 0.8, color = barveDni) 

        plt.ylabel('Število ur') 
        plt.title("{0:s} {1:s} {2:s}".format(smer, letnik, semester.lower()))

        plt.show()
  
        plt.pie(tabelaŠtevilaUr, labels = oznakeDni, colors = barveDni,  
            startangle=90, shadow = True, explode = (0, 0, 0, 0, 0), 
            radius = 1.2, autopct = '%1.1f%%')

        plt.show()

        x2 = range(len(slovarPredmetov))
        y2 = list(slovarPredmetov.values())

        oznakePredmetov = list(slovarPredmetov.keys())
        barvePredmetov = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'brown', 'gray', 'pink', 'cyan', 'midnightblue', 'ghostwhite', 'olive', 'darksalmon', 'khaki', 'violet', 'coral', 'darkturquoise', 'royalblue', 'lime']
        #Predpostavljamo, da ima vsak semester kvečjemu 20 različnih predmetov

        plt.bar(x2, y2, tick_label = oznakePredmetov, 
        width = 0.5, color = barvePredmetov[:len(oznakePredmetov)])

        plt.ylabel('Število ur') 
        plt.title("{0:s} {1:s} {2:s}".format(smer, letnik, semester.lower()))

        plt.show()

        plt.pie(y2, labels = oznakePredmetov, colors = barvePredmetov,  
        startangle=90, shadow = True, explode = tuple([0] * len(slovarPredmetov)), 
        radius = 1.2, autopct = '%1.1f%%')

        plt.show()
        
    nadaljuj = str(None)
    seznamDaNe = 'da, ne, Da, Ne, DA, NE,dA, nE' #Recimo, da dopuščamo tudi CapsLock možnosti.
    while nadaljuj not in seznamDaNe:
        print()
        print('Želite ponoviti statistično obdelavo? Vnesite "da" ali "ne". Branje iz spleta ne bo ponovno izvedeno.')
        print()
        nadaljuj = input()
        if nadaljuj not in seznamDaNe:
            print()
            print(nepravilenVnos)
    if nadaljuj == 'ne':
        prekini == True
