import numpy as np
from PIL import Image
im = Image.open("C:/Users/USER/Downloads/test.jpg")
fil= (-0.25,-0.5,-0.25,-0.5,4,-0.5,-0.25,-0.5,-0.25)
fil=np.reshape(fil,(3,3))

v=[]
s=[]

def sharpen(width, height, v, hsv):

    v = np.reshape(v, (height,width))
            
    for i in range(1,height-1):
        for j in range(1,width-1):
            ker=[[v[i-1][j-1],v[i-1][j],v[i-1][j+1]],[v[i][j-1],v[i][j],v[i][j+1]],[v[i+1][j-1],v[i+1][j],v[i+1][j+1]]]
            v[i][j]=np.sum(np.multiply(ker,fil))

    k=0
    for i in range(0, height):
        for j in range(0, width):
            hsv[k][2] = v[i][j]
            k+=1
            
    return hsv

def saturation(a,hsv):
    new_hsv=[]
    for item in hsv:
        #s= s+a/100*(1-s)
        s=item[1]
        s=s*(1+a/100)
        if s>1:
            s=1
        new_hsv.append([item[0],s,item[2]])
    hsv=new_hsv
    return hsv
            

def hsv_rgb(hsv):

	rgb= list()
	for i in hsv:
		h = i[0]
		s = i[1]
		v = i[2]
		c = v * s
		x = c* (1- abs(((h / 60) %2)-1))
		m = v - c

		if h>=0 and h<60:
				r = c
				g = x
				b = 0

		elif h>=60 and h<120:
				r = x
				g = c
				b = 0

		elif h>=120 and h<180:
				r = 0
				g = c
				b = x

		elif h>=180 and h<240:
				r = 0
				g = x
				b = c

		elif h>=240 and h<300:
				r = x
				g = 0
				b = c

		elif h>=300 and h<360:
				r = c
				g = 0
				b = x

		R = (r+m)*255
		G = (g+m)*255
		B = (b+m)*255

		rgb.append((int(R),int(G),int(B)))
	return rgb

def startProcess():
    hsv=[]
    rgbim = Image.new('RGB', im.size)
    width,height = im.size
    pix_val=list(im.getdata())

    for i in pix_val:
        r= i[0]/255
        g= i[1]/255
        b= i[2]/255
                        
        Cmax = max(r,g,b)
        Cmin = min(r,g,b)
        delta = Cmax - Cmin

        #Hue Calculation:
        if delta == 0:
            h = 0
        elif Cmax == r:
            h = 60*(((g-b)/delta) % 6)
        elif Cmax == g:
            h = 60*(((b-r)/delta) + 2)
        elif Cmax == b:
            h = 60*(((r-g)/delta) + 4)

        # Saturation calculation:
        if Cmax == 0:
            sat = 0
        else:
            sat = delta/Cmax

        #Value calculation:
        val = Cmax

        #v vector for Value only:
        v.append(val)

        hsv.append([h , sat, val])
    
    
    print("\nMenu\n(1)Saturation\n(2)Sharpening\n(3)Save and Exit\n(4)Exit")
    choice=0
    while choice!=4:
        
        choice=int(input("Enter choice "))
        if choice==1:
            a=int(input("Enter the Saturation value to change the Saturation of Image:"))
            hsv=saturation(a,hsv)
            rgb=hsv_rgb(hsv)
            rgbim.putdata(rgb)
            rgbim.show()
            
        elif choice==2:
            hsv = sharpen(width, height, v, hsv)
            rgb=hsv_rgb(hsv)
            rgbim.putdata(rgb)
            rgbim.show()
            
        elif choice==3:
            print('OK')
        
        elif choice==4:
            print('Thanks for trying. Please buy our product for more features. xD')
        
        else:
            print("Invalid choice, please choose again")
            print("\n")
    print("Thank you")
    
    

    #Reconstructing the image
    #rgbim.putdata(rgb)
    #rgbim.show()
    #rgbim.save("C:/Users/Navin/Desktop/Image/ema.jpg")

startProcess()

