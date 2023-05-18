import base64
  
  
'''with open("sample/myface.jpg", "rb") as image2string:
    converted_string = base64.b64encode(image2string.read())
print(converted_string)
  
with open('sample/encode.bin', "wb") as file:
    file.write(converted_string)'''


file = open('sample/encode.bin', 'rb')
byte = file.read()
file.close()
  
decodeit = open('sample/hello.jpg', 'wb')
decodeit.write(base64.b64decode((byte)))
decodeit.close()
