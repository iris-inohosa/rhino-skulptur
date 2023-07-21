#Modul: 11790 | Decode - Digitales Entwerfen | SoSe 17
#Name: Iris Inokhosa
#Matrikelnummer: 3612590
#
#Das Modul beschaeftigt sich mit digitaler Formfindung 
#und der Rekonstruktion kuenstlerischer Werke mittels Software-Algorithmen
#
#Title des Werkes: Assemble Construct
#Autor: DannyDkArt (Nickname), Grossbritanien
#Material: Holz und Scrauben
#Time: 8 Stunde
#Information - A Large scale sculpture made by sawing pieces of wood into various sizes, 
#nail gunned them together to form this assemblage of wood, overlapping and creating an overdrawn outcome.
#Alle Groesse sin in cm!
#80x55mm

import rhinoscriptsyntax as rs
import Rhino
import random
import math

#Variablen
#Waehlen eine Kurve
kurve = rs.GetObject("Waehlen Sie eine Kurve: ", 4)
count = int(input("Geben Sie eine Zahl ein: "))# -> 
planes = []

#Gliedern die Kurve und bekommen Planar Surfaces
doms = rs.CurveDomain(kurve)
minDom = doms[0]
maxDom = doms[1]
#print(minDom, maxDom)

#Funktion_createPlaneSrf
#Die Funktion gliedert die ausgewaelte Kurve in count-Teile
#In jeder Punkte jedes Teiles wird eine normale Ebene geschafft
#Normale Ebene - eine Ebene die senktrecht zum Tangent - Vektor ist
#Gibt Normale Ebene zurueck
def createPlaneSrf (minDom, maxDom, count, kurve, i):
    param = (maxDom - minDom)/count * i
    tan = rs.CurveTangent(kurve, param)
    tan = rs.VectorScale(tan, random.randint(12,30))                   #Tangent-Vector
    point = rs.EvaluateCurve(kurve, param)
    rs.AddPoint(point)
    #rs.AddPoint(tan)                               #Tangent Points
    tanPt = rs.VectorAdd(point, tan)
    rs.AddLine(tanPt, point)                        #Tangent Lines - RICHTUNG!!!
    normPlane = rs.PlaneFromNormal(point, tan)
    normPlaneSrf = rs.AddPlaneSurface(normPlane, 3, 3)
    return normPlaneSrf, tan

#Funktion_pointsOnSurface
#Die Funktion bekommt als Argumenten die Normale Ebene (sehen: Funktion createPlaneSrf)
#Und Tangent - Vektoren
#Auf jede Ebene wird die random Mehrheit von Punkten gebaut
#Gibt Vektoren und Punkten zurueck
def pointsOnSurface(normPlaneSrf, tan, i):
    param = math.pow(i, 1.7)/15
    pointsOnPlane = rs.EvaluateSurface(normPlaneSrf, random.uniform(-10+(param),10-(param)), random.uniform(-10+(param),10-(param)))
    pointsCloud = rs.AddPoints([pointsOnPlane]) #Liste der Punkten
    richtung = rs.VectorAdd(pointsOnPlane, tan)
    return richtung, pointsOnPlane

#Funktion_rotateRandomVectors
def rotateRandomVectors(richtung, a , i):
    b = a * a
    c = a * b
    d = c * a
    x = random.uniform(-5/a,5/a)    #!!!
    y = random.uniform(-3/a,3/a)  #!!!
    z = random.uniform(-5/a,5/a)    #!!!
    param = math.pow(a, 2.5)/12
    winkel = random.uniform(random.uniform(-60/param, -20/param),random.uniform(20/param, 60/param))
    rotateVectors = rs.VectorRotate(richtung, winkel, [x,y,z])
    return rotateVectors

#Funktion_createSurface
#Die Funktion bekommst als Argumenten die Mehrheit von Vektoren
#und Anfangspunkten von diesen Vektoren
#Schafft die Rechtecke die nachfolgend extrudiert werden muessen
#Gibt Mehrheit von Boxen zurueck
def createSolid (normal, basePt, path2, i): 
    #basePlane = rs.CurvePerpFrame(normal, 1)
    basePlane = rs.CurvePerpFrame([path2], 1)
    #basePlane = rs.PlaneFromNormal(basePt, normal)    #Basisebene fuer Rechtecke
    k = i + 1
    m = k*k
    param = math.pow((math.log10(k) + 1), 2.1)
    b = round(random.uniform(0.8,8/param),1)
    h = round(random.uniform(0.5,5/param),1)
    #rechtecke = rs.AddRectangle(basePlane, b, h)    #Hier b - Breite, h - Hoehe
    rechtecke = rs.AddPlaneSurface(basePlane, b, h)
    solid = rs.ExtrudeSurface(rechtecke, path2)
    return solid

#Ueberpruefen ob die Solids sich einander ueberschneiden
def intersection():
    intersect = []
    breps = rs.GetObjects("Waehlen Sie Polysurfaces: ",16)
    deletedObj = 0
    for i in range (0, len(breps)-1):
        intersection = 0
        for k in range (i+1, len(breps)-1):
            clashlist = (Rhino.Geometry.Intersect.Intersection.BrepBrep(rs.coercebrep(breps[i]),rs.coercebrep(breps[k]),0.0))
            if clashlist[1]:
                intersection +=1
            else:
                continue
        if intersection == 0:
            rs.DeleteObject(breps[i])
            deletedObj +=1
        else:
            continue
    print (deletedObj)
    

#intersect = []
#Rekursion
for i in range (0,count+1):
    #Funktion Aufruf
    normPlaneSrf, tan = createPlaneSrf(minDom, maxDom, count, kurve, i)
    pointsCount = random.randint(8, 19)
    for k in range (1,pointsCount + 1):       
        #Funktion Aufruf
        richtung, pointsOnPlane = pointsOnSurface(normPlaneSrf, tan, i)
        for a in range (1, pointsCount+1):
        #Funktion Aufruf
            rotateVectors = rotateRandomVectors(richtung, a, i)
        path2 = rs.AddLine(rotateVectors, pointsOnPlane) #gedrehende Vektoren
        #print(rs.CurveLength(path2))
        #Funktion createSolid Aufruf 
        createSolid(rotateVectors, pointsOnPlane, path2, k)
        #solid = createSolid(rotateVectors, pointsOnPlane, path2, i)
        #intersect.append(solid)
        #rs.SplitBrep(solid,solid)
intersection()
#print(intersect)

#Unroll Polysurfaces
#breps = rs.GetObjects("Waehlen Sie Polysurfaces: ",16)
#for i in range (0, len(breps)-1):
#    rs.UnrollSurface(breps[i], explode=True)



