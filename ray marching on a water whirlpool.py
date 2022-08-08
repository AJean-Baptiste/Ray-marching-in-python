import matplotlib.pyplot as plt
import math
import numpy as np

D = 5 #study zone in meter
N = 100000 #resolution of simulation (iteration for D meter)

"""propriété du rayon"""
y0 = 2.45
angle = 6

longueur = 100000 #longueur totale parcouru par le rayon en nombre de pas
nombreRayon = 1
deltaY = 0
""""""""""""""""""""""""

"""whirlpool property"""
hi = 2.25
g = 9.81
rc = 0.016
gamma = 0.265
""""""""""""""""""""""""""

def f (r): #whirlpool function
    h = np.zeros(N)
    for k in range (0, N):
        if r[k] < -(rc) or r[k] > rc :
            h[k] = hi - (gamma*gamma)/(8*(math.pi)*(math.pi)*g*r[k]*r[k])
        else:
            h[k] = (((gamma*r[k])*(gamma*r[k]))/(8*g*(math.pi)*(math.pi)*rc*rc*rc*rc))+hi-(gamma*gamma)/(4*g*(math.pi)*(math.pi)*rc*rc)     
    return h

def fp (r, h): #dérivative of whirlpool function
    hp = np.zeros(N)
    for k in range(0, N-1): 
        hp[k] = (h[k+1] - h[k]) / (r[k+1] - r[k])
    return hp


def difference (y0, y1, h0, h1): #collision function 
    y0 = y0-h0
    y1 = y1-h1
    if y0*y1 > 0:
        return False
    else:
        return True
    
    

"""plot of whirlpool"""
r = np.linspace(-D/2, D/2, N)
h = np.zeros(N)
h = f(r)
hp = np.zeros(N)
hp = fp(r,h)
plt.plot (r,h)
""""""""""""""""""""
newY = y0
varTest = False
for w in range (nombreRayon):
    newY = newY-deltaY
    y0 = newY
    """------------------------------------Ray tracing--------------------------------------------"""
    angleIncidence = angle*math.pi/180
    milieu = 0
    if y0 <= h[0]:
        milieu = 1
    x0 = -D/2
    x1 = x0
    y1 = y0
    
    xRayon = np.zeros(longueur)
    yRayon = np.zeros(longueur)
    xRayon[0] = x0
    yRayon[0] = y0
    collision = False
    reflexion = False
    
    
    for k in range (1,longueur):    
       
        """ray tracing in air"""
        if milieu == 0:
            if int(((x1+(D/2))/D)*N)>=N or int(((x1+(D/2))/D)*N)<0: #for "out of bound exception"
                xRayon[k] = x0
                yRayon[k] = y0
            else:
                
                
                """test if change air -> water"""
                if collision:
                    
                    milieu = 1
                    
                    """refraction""" 
                    coefDirTangente = hp[int(((x1+(D/2))/D)*N)]
                        
                    angleTangente = abs(math.atan(coefDirTangente))
                    angleIncidenceCorr = angleIncidence+angleTangente
                        
                    angleIncidence = math.acos((math.cos(angleIncidenceCorr))/(1.33))-angleTangente
                        
                else:
                    
                    x1 = x0 + (D/N)*math.cos(-angleIncidence)
                    y1 = y0 + (D/N)*math.sin(-angleIncidence)
                    
                xRayon[k] = x1
                yRayon[k] = y1
                if 0 <= int(((x1+(D/2))/D)*N) < N:
                    collision = difference(y0, y1, h[int(((x0+(D/2))/D)*N)], h[int(((x1+(D/2))/D)*N)])
                    
                
                x0 = x1
                y0 = y1
    
        """ray in water"""
        if milieu == 1:
            
            if int(((x1+(D/2))/D)*N)>=N or int(((x1+(D/2))/D)*N)<0: #verif de "out of bound exception"
                xRayon[k] = x0
                yRayon[k] = y0
            else:
                
                """test change water -> air"""
                if collision:
                    milieu = 0
                
                    """refraction angle or reflection angle"""
                    coefDirTangente = hp[int(((x1+(D/2))/D)*N)]
                
                    angleTangente = abs(math.atan(coefDirTangente))
                    angleIncidenceCorr = angleIncidence+angleTangente
                    if -1 <= (math.cos(angleIncidenceCorr))*1.33 <= 1:
                        angleIncidence = math.acos((math.cos(angleIncidenceCorr))*1.33)-angleTangente
    
                    else:
                        milieu = 1
                        angleIncidence = -angleIncidenceCorr-angleTangente
                        reflexion = True
    
                else:
               
                    x1 = x0 + (D/N)*math.cos(-angleIncidence)
                    y1 = y0 + (D/N)*math.sin(-angleIncidence)
               
                xRayon[k] = x1
                yRayon[k] = y1
                
                if 0 <= int(((x1+(D/2))/D)*N) < N:
                    collision = difference(y0, y1, h[int(((x0+(D/2))/D)*N)], h[int(((x1+(D/2))/D)*N)])
                
                if collision and reflexion:
                    collision = False
                    reflexion = False
                    
                x0 = x1
                y0 = y1
                
                
    #plt.clf()
    #plt.plot (r,h)
    plt.plot(xRayon, yRayon)
    #plt.axis('equal')
    plt.xlim(-0.1, 0.1)
    plt.ylim(1.5, 2.3)
    #plt.savefig('plot/' + str(w) + '.png', dpi = 250)
    """----------------------------------------------------------------------------------------------"""
plt.savefig('plot/' + str(w) + '.png', dpi = 250)
