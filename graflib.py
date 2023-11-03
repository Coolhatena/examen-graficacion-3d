from PIL import Image,ImageDraw
import math

def drawPoint(x,y,color,canvas):
    width, height = canvas.size
    xn=int(width/2+x)
    yn=int(height/2-y)
    #print(x,y,xn,yn)
    canvas.putpixel((xn, yn),color)

def swap(P0,P1):
    aux=P0
    P0=P1
    P1=aux
    return P0, P1

def interpolate(i0,d0,i1,d1):
    if i0 == i1:
       return [d0 for i in range(i0,i1+1)]
    values = []
    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(i0,i1+1):
        values.append(d)
        d = d + a
    return values

def drawLine(P0,P1,color,canvas):
    x0=P0[0]
    y0=P0[1]
    x1=P1[0]
    y1=P1[1]
    if abs(P1[0]-P0[0])>abs(P1[1]-P0[1]):
        #lineas horizontales
        if P0[0]>P1[0]:
            (x0,y0), (x1,y1) = swap(P0,P1)
        ys = interpolate(x0, y0, x1, y1)
        for x in range(x0,x1+1):
            drawPoint(x, ys[x - x0], color,canvas)
    else:
        #lineas verticales    
        if P0[1]>P1[1]:
            (x0,y0), (x1,y1) = swap(P0,P1)
        xs = interpolate(y0, x0, y1, x1)
        for y in range(y0,y1+1):
            drawPoint(xs[y - y0],y, color,canvas)

def drawWireframeTriangle (P0, P1, P2, color, canvas):
    drawLine(P0, P1, color, canvas)
    drawLine(P1, P2, color, canvas)
    drawLine(P2, P0, color, canvas)

def drawFilledTriangle (P0, P1, P2, color,canvas):
    # Sort the points so that y0 <= y1 <= y2
    if P1[1] < P0[1]:
        P1, P0 = swap(P1,P0)
    if P2[1] < P0[1]:
        P2, P0 = swap(P2,P0)
    if P2[1] < P1[1]:
        P2, P1 = swap(P2,P1)
        
    x0=P0[0]
    y0=P0[1]
    x1=P1[0]
    y1=P1[1]
    x2=P2[0]
    y2=P2[1]
        
    # Compute the x coordinates of the triangle edges
    x01 = interpolate(y0, x0, y1, x1)
    x12 = interpolate(y1, x1, y2, x2)
    x02 = interpolate(y0, x0, y2, x2)
    
    #Concatenate the short sides
    #remove_last(x01)
    x01.pop(-1)
    x012 = x01 + x12
    #Determine which is left and which is right
    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        x_left = x02
        x_right = x012
    else:
        x_left = x012
        x_right = x02
    
    # Draw the horizontal segments
    for y in range(y0,y2+1):
        a=round(x_left[y - y0])
        b=round(x_right[y - y0])
        for x in range(a,b):
            drawPoint(x,y,color,canvas)

def drawShadedTriangle (P0, P1, P2, color,canvas):
    # Sort the points so that y0 <= y1 <= y2
   
    c=P0
    if P1[1] < P0[1]:
        P1, P0 = swap(P1,P0)
        
    if P2[1] < P0[1]:
        P2, P0 = swap(P2,P0)
 
    if P2[1] < P1[1]:
        P2, P1 = swap(P2,P1)
    
    if c == P0:
        h0=1
        h1=0
        h2=0
    elif c==P1:
        h0=0
        h1=1
        h2=0
    else:
        h0=0
        h1=0
        h2=1    
    
    x0=P0[0]
    y0=P0[1]
    x1=P1[0]
    y1=P1[1]
    x2=P2[0]
    y2=P2[1]
    
    # Compute the x coordinates and h values of the triangle edges
    x01 = interpolate(y0, x0, y1, x1)
    h01 = interpolate(y0, h0, y1, h1)
    
    x12 = interpolate(y1, x1, y2, x2)
    h12 = interpolate(y1, h1, y2, h2)
    
    x02 = interpolate(y0, x0, y2, x2)
    h02 = interpolate(y0, h0, y2, h2)

    #Concatenate the short sides
    x01.pop(-1)
    x012 = x01 + x12
    
    h01.pop(-1)
    h012 = h01 + h12

    #Determine which is left and which is right
    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        x_left = x02
        h_left = h02
        
        x_right = x012
        h_right = h012
    else:
        x_left = x012
        h_left = h012
        
        x_right = x02
        h_right = h02
    
    # Draw the horizontal segments
    for y in range(y0,y2+1):
        xl=round(x_left[y - y0])
        hl=h_left[y - y0]
        
        xr=round(x_right[y - y0])
        hr=h_right[y - y0]
        
        h_segment = interpolate(xl,hl,xr,hr)
        
        for x in range(xl,xr):
            sh_color0 = round(color[0] * h_segment[x - xl])
            sh_color1 = round(color[1] * h_segment[x - xl])
            sh_color2 = round(color[2] * h_segment[x - xl])
            shaded_color = (sh_color0,sh_color1,sh_color2)
            drawPoint(int(x),int(y),shaded_color,canvas)
            
def viewportToCanvas(x, y):
    Cw=501
    Vw=501
    Ch=501
    Vh=501
    return (int(x * Cw/Vw), int(y * Ch/Vh))

def projectVertex(v):
    d=100
    vx=v[0]
    vy=v[1]
    vz=v[2]
    px=vx * d / vz
    py=vy * d / vz
    #print('px: ',px,' py: ', py)
    return viewportToCanvas(px, py)
    
def renderObject(vertices, triangles,canvas):
    projected = []
    for V in vertices:
        projected.append(projectVertex(V))
    for T in triangles:
        renderTriangle(T, projected,canvas)

def renderTriangle(triangle, projected,canvas):
    drawWireframeTriangle(projected[triangle[0]],
                             projected[triangle[1]],
                             projected[triangle[2]],
                             triangle[3],canvas)
    

