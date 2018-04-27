
#http://www.euclideanspace.com/maths/algebra/vectors/angleBetween/
from math import *

def rndint(num): return int(num+0.5)

def vec_add(v1,v2):
    return [v1[i]+v2[i] for i in range(len(v1))]
def vec_sub(v1,v2):
    return [v1[i]-v2[i] for i in range(len(v1))]
def vec_dot(v1,v2):
    return sum([v1[i]*v2[i] for i in range(len(v1))])
def vec_scale(sc,v):
    return [sc*v[i] for i in range(len(v))]
def vec_negate(v):
    return [-v[i] for i in range(len(v))]

def vec_length_sq(vec):
    return vec_dot(vec,vec)
def vec_length(vec):
    return vec_dot(vec,vec) ** 0.5
def vec_norm(vec):
    return vec_scale(1.0/vec_length(vec),vec)

def vec_reflect(vec, norm):
    v_dot_n = vec_dot(vec,norm)
    sc = 2 * v_dot_n
    return [sc*norm[i]-vec[i] for i in range(len(vec))]

def point_project_line(p, l1,l2):
    #Adapted from http://www.gamedev.net/topic/444154-closest-point-on-a-line/
    p_l1 = vec_sub(p,l1)
    l2_l1 = vec_sub(l2,l1)
    t = vec_dot(p_l1,l2_l1) / vec_dot(l2_l1,l2_l1)

    return vec_add(l1,vec_scale(t,l2_l1))

def point_square_distance(v1,v2):
    v_t = vec_sub(v1,v2)
    return vec_dot(v_t,v_t)

def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return sqrt(dotproduct(v, v))

def angle_radian(v1, v2):
    return acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
