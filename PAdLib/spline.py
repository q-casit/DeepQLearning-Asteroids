import pygame

from .math_helpers import *

def draw(surface, color, closed, pointlist, steps, t=0.0,b=0.0,c=0.0, width=1):
    _internal_draw(surface, color, closed, pointlist, steps, t,b,c, False, width, False)
def aadraw(surface, color, closed, pointlist, steps, t=0.0,b=0.0,c=0.0, blend=True):
    _internal_draw(surface, color, closed, pointlist, steps, t,b,c, True, 0, blend)
def _internal_draw(surface, color, closed, pointlist, steps, t,b,c, aa, width, blend):
    #Kochanek-Bartels spline implementation, written long ago and updated.
    t_inc = 1.0/float(steps)

    #This allows us to draw through all visible control points (normal Kochanek-Bartels
    #splines do not draw through their last endpoints).
    if closed:
        pointlist = [pointlist[-2],pointlist[-1]] + pointlist + [pointlist[0],pointlist[1]]
    else:
        pointlist = [pointlist[0]] + pointlist + [pointlist[-1]]

    cona = (1-t)*(1+b)*(1-c)*0.5
    conb = (1-t)*(1-b)*(1+c)*0.5
    conc = (1-t)*(1+b)*(1+c)*0.5
    cond = (1-t)*(1-b)*(1-c)*0.5

    tans = []
    tand = []
    for x in range(len(pointlist)-2):
        tans.append([])
        tand.append([])
    i = 1
    while i < len(pointlist)-1:
        pa = pointlist[i-1]
        pb = pointlist[i  ]
        pc = pointlist[i+1]
        x1 = pb[0] - pa[0]
        y1 = pb[1] - pa[1]
        x2 = pc[0] - pb[0]
        y2 = pc[1] - pb[1]
        tans[i-1] = (cona*x1+conb*x2, cona*y1+conb*y2)
        tand[i-1] = (conc*x1+cond*x2, conc*y1+cond*y2)
        i += 1

    for i in range(1,len(pointlist)-2,1):
        p0 = pointlist[i  ]
        p1 = pointlist[i+1]
        m0 = tand[i-1]
        m1 = tans[i  ]
        
        #draw curve from p0 to p1
        lines = [(p0[0],p0[1])]
        t_iter = t_inc
        while t_iter < 1.0:
            h00 = ( 2*(t_iter*t_iter*t_iter)) - ( 3*(t_iter*t_iter)) + 1
            h10 = ( 1*(t_iter*t_iter*t_iter)) - ( 2*(t_iter*t_iter)) + t_iter
            h01 = (-2*(t_iter*t_iter*t_iter)) + ( 3*(t_iter*t_iter))
            h11 = ( 1*(t_iter*t_iter*t_iter)) - ( 1*(t_iter*t_iter))
            px = h00*p0[0] + h10*m0[0] + h01*p1[0] + h11*m1[0]
            py = h00*p0[1] + h10*m0[1] + h01*p1[1] + h11*m1[1]
            lines.append((px,py))
            t_iter += t_inc
        lines.append((p1[0],p1[1]))
        
        if aa:
            #This function can take floating-point values for endpoints.
            pygame.draw.aalines(surface,color,False,lines,blend)
        else:
            lines = [list(map(rndint,p)) for p in lines]
            pygame.draw.lines(surface,color,False,lines,width)
