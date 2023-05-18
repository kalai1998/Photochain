import base64 
image = open('sample/myface.jpg', 'rb') #open binary file in read mode
image_read = image.read()
image_64_encode = base64.b64encode(image_read)

'''value=str(image_64_encode)

fp=open("sample/hash.txt","w")
fp.write(value)
fp.close()

fp1=open("sample/hash.txt","r")
val=fp1.read()
fp1.close()'''

#image_64_encode=val

image_64_decode = base64.b64decode(image_64_encode) 
image_result = open('sample/face.jpg', 'wb') 
image_result.write(image_64_decode)
