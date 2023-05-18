# main.py
import os
import base64
import io
import math
from flask import Flask, flash, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
import mysql.connector
import hashlib
import datetime
from datetime import datetime
from datetime import date
import random
from random import randint
from urllib.request import urlopen
import webbrowser
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import imagehash
import shutil
import PIL.Image
from PIL import Image

from werkzeug.utils import secure_filename
import urllib.request
import urllib.parse



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="photo_chain"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""
    ff=open("det.txt","w")
    ff.write("1")
    ff.close()

    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()

    #s="welcome"
    #v=s[2:5]
    #print(v)
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ds_register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password!'
    

    return render_template('index.html',msg=msg)



@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    vid=""
    nam=""
    email=""
    mess=""
    bdata=""
    bc=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM ds_register")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        aadhar=request.form['aadhar']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        
        mycursor.execute('SELECT count(*) FROM ds_register WHERE uname = %s || aadhar=%s', (uname,aadhar))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            now = datetime.now()
            rdate=now.strftime("%d-%m-%Y")

            
            adr=str(aadhar)
            rn=randint(50,90)
            v1=name[0:2]
            v2=str(rn)
            v3=adr[0:3]
            bkey=v1+str(maxid)+v2+v3

            f1=open("bc.txt","r")
            bc=f1.read()
            f1.close()

            
        
            sql = "INSERT INTO ds_register(id,name,gender,dob,email,aadhar,uname,pass,create_date,block_key) VALUES (%s,%s, %s, %s, %s, %s,%s,%s,%s,%s)"
            val = (maxid,name,gender,dob,email,aadhar,uname,pass1,rdate,bkey)
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "Registered Success")
            mess="Dear "+name+", Username: "+uname+", Password: "+pass1+", Block Key: "+bkey
            msg="success"
            vid=str(maxid)
            nam="1"

            mycursor.execute('SELECT * FROM ds_register WHERE uname=%s', (uname,))
            dd = mycursor.fetchone()
            dtime=str(dd[11])
            bdata="ID:"+str(maxid)+", Username:"+uname+", Status:Registered, Aadhar:"+aadhar+", Date: "+dtime
            
        else:
            msg='fail'
    return render_template('/register.html',msg=msg,nam=nam,vid=vid,mess=mess,email=email,bdata=bdata,bc=bc)

@app.route('/add_photo',methods=['POST','GET'])
def add_photo():
    nam=request.args.get("nam")
    vid = request.args.get('vid')
    uname=""
    if 'username' in session:
        uname = session['username']
        
    if nam=="1":
        session['username'] = nam
        uname=nam
        
    
    ff1=open("photo.txt","w")
    ff1.write("2")
    ff1.close()
    mycursor = mydb.cursor()
        
    ff=open("user.txt","w")
    ff.write(vid)
    ff.close()
    
    if request.method=='POST':
        vid=request.form['vid']
        fimg="v"+vid+".jpg"

        mycursor.execute('delete from ds_face WHERE vid = %s', (vid, ))
        mydb.commit()

        ff=open("det.txt","r")
        v=ff.read()
        ff.close()
        vv=int(v)
        v1=vv-1
        vface1="U"+vid+".jpg"
        i=2
        while i<vv:
            
            mycursor.execute("SELECT max(id)+1 FROM ds_face")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            vface=vid+"_"+str(i)+".jpg"
            sql = "INSERT INTO ds_face(id, vid, vface) VALUES (%s, %s, %s)"
            val = (maxid, vid, vface)
            print(val)
            mycursor.execute(sql,val)
            mydb.commit()
            i+=1

        
            
        #mycursor.execute('update cv_user set photo=%s WHERE id = %s', (vface1, vid))
        #mydb.commit()
        #shutil.copy('faces/f1.jpg', 'static/photo/'+vface1)
        return redirect(url_for('view_face',vid=vid,act='success'))
        

    return render_template('add_photo.html',vid=vid,uname=uname)

###Preprocessing
@app.route('/view_face',methods=['POST','GET'])
def view_face():
    uname=""
    if 'username' in session:
        uname = session['username']
    vid=request.args.get("vid")
       
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()

    vid = request.args.get('vid')
    value=[]
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_face where vid=%s",(vid, ))
    value = mycursor.fetchall()

    if request.method=='POST':
        print("Training")
        vid=request.form['vid']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM ds_face where vid=%s",(vid, ))
        dt = cursor.fetchall()
        for rs in dt:
            ##Preprocess
            path="static/frame/"+rs[2]
            path2="static/process1/"+rs[2]
            mm2 = PIL.Image.open(path).convert('L')
            rz = mm2.resize((200,200), PIL.Image.ANTIALIAS)
            rz.save(path2)
            
            '''img = cv2.imread(path2) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            path3="static/process2/"+rs[2]
            cv2.imwrite(path3, dst)'''
            ######
            img = cv2.imread(path2)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # noise removal
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/"+rs[2]
            segment.save(path3)
            
            #####
            image = cv2.imread(path2)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            image = Image.fromarray(image)
            edged = Image.fromarray(edged)
            path4="static/process3/"+rs[2]
            edged.save(path4)
            ##
            #shutil.copy('static/images/11.png', 'static/process4/'+rs[2])
       
        return redirect(url_for('process1',vid=vid))
        
    return render_template('view_face.html', result=value,vid=vid,uname=uname)

@app.route('/process1',methods=['POST','GET'])
def process1():
    uname=""
    if 'username' in session:
        uname = session['username']
    vid=""
    value=[]
    vid=request.args.get("vid")

    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_register where id=%s",(vid, ))
    value = mycursor.fetchone()
    
    data="ID:"+vid+",Username:"+value[6]+",Status:Registered"

    if request.method=='GET':
        vid = request.args.get('vid')
        
        mycursor.execute("SELECT * FROM ds_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('process1.html', result=value,vid=vid,uname=uname,bc=bc,data=data)

@app.route('/process2',methods=['POST','GET'])
def process2():
    uname=""
    if 'username' in session:
        uname = session['username']
    vid=""
    value=[]

    vid=request.args.get("vid")

    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM ds_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('process2.html', result=value,vid=vid,uname=uname)    

@app.route('/process3',methods=['POST','GET'])
def process3():
    uname=""
    if 'username' in session:
        uname = session['username']
    vid=""
    value=[]

    vid=request.args.get("vid")

    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM ds_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('process3.html', result=value,vid=vid,uname=uname)

@app.route('/process4',methods=['POST','GET'])
def process4():
    vid=""
    value=[]
    vid=request.args.get("vid")
    uname=""
    if 'username' in session:
        uname = session['username']
    print("getname")
    print(uname)
    mycursor = mydb.cursor()
    #mycursor.execute("update cv_user set photo_st=1 where uname=%s",(name,))
    #mydb.commit()
    
    return render_template('process4.html', vid=vid,uname=uname)

def blurImage(img,pid):
    #plt.imshow(img, cmap="gray")
    #plt.axis('off')
    #plt.style.use('seaborn')
    #plt.show()
  
    #########
    image1 = cv2.imread("static/comments/"+img)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    j=1
    apos1=[]
    for (x, y, w, h) in faces:
            mm=cv2.rectangle(image1, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #cv2.imwrite("static/comments/"+img, mm)
            image = cv2.imread("static/comments/"+img)
            #pp1=str(x)+"-"+str(y)
            #apos1.append(pp1)
            #cropped = image[y:y+h, x:x+w]
            #gg="g"+pid+"_"+str(j)+".jpg"
            #cv2.imwrite("static/group/"+gg, cropped)
            j+=1
    '''dd3=",".join(apos1)
    fm3="H"+pid+".txt"
    fz3=open("static/group/"+fm3,"w")
    fz3.write(dd3)
    fz3.close()'''
    #########
    # Reading an image using OpenCV
    # OpenCV reads images by default in BGR format
    image = cv2.imread("static/comments/"+img)
    # Converting BGR image into a RGB image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      
    # plotting the original image
    #plotImages(image)
      
    face_detect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    face_data = face_detect.detectMultiScale(image, 1.3, 5)
      
    # Draw rectangle around the faces which is our region of interest (ROI)
    apos=[]
    j=1
    for (x, y, w, h) in face_data:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi = image[y:y+h, x:x+w]
        pp=str(x)+"-"+str(y)
        apos.append(pp)
        cropped = image[y:y+h, x:x+w]
        gg="g"+pid+"_"+str(j)+".jpg"
        cv2.imwrite("static/group/"+gg, cropped)
        ##
        
        # applying a gaussian blur over this new rectangle area
        roi = cv2.GaussianBlur(roi, (23, 23), 30)
        # impose this blurred image on original image to get final image
        image[y:y+roi.shape[0], x:x+roi.shape[1]] = roi
        j+=1

    jj=j-1
    dd=str(jj)
    fm="F"+pid+".txt"
    fz=open("static/group/"+fm,"w")
    fz.write(dd)
    fz.close()

    '''dd2=",".join(apos)
    fm2="G"+pid+".txt"
    fz2=open("static/group/"+fm2,"w")
    fz2.write(dd2)
    fz2.close()'''
        
    fn="F"+img
    cv2.imwrite("static/comments/"+fn, image)
    fng="G"+img
    shutil.copy("static/comments/"+fn,"static/comments/"+fng)

def fullBlur(img,pid):
    # bat.jpg is the batman image.
    img1 = cv2.imread("static/comments/"+img)
       
    # make sure that you have saved it in the same folder
    # Averaging
    # You can change the kernel size as you want
    fn="B"+img
        
    avging = cv2.blur(img1,(20,20))
    cv2.imwrite("static/comments/"+fn, avging)



@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    cnt=0
    uname=""
    mess=""
    act=request.args.get("act")
    st=""
    fn2=""
    pmode=""
    bdata=""
    bc=""
    pid=""
    pre_id=""
    ss=""
    msg1=""
    bdata2=[]
    if 'username' in session:
        uname = session['username']
    #uname="raj"
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_register where uname=%s",(uname,))
    data = mycursor.fetchone()
    vid=data[0]

    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()

            

    ########
    if request.method == 'POST':
        detail= request.form['detail']
        if 'file' not in request.files:
            flash('No file Part')
            return redirect(request.url)
        file= request.files['file']

        file_name=""
        mycursor.execute("SELECT max(id)+1 FROM ds_post")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        pid=str(maxid)
        if file.filename == '':
            flash('No Select file')
            #return redirect(request.url)
        if file:
            fname1 = file.filename
            fname = secure_filename(fname1)
            file_name="P"+str(maxid)+fname
            file.save(os.path.join("static/comments/", file_name))

            with open("static/comments/"+file_name, "rb") as image2string:
                converted_string = base64.b64encode(image2string.read())
            print(converted_string)
            bfile="P"+str(maxid)+".bin"
            with open('static/upload/'+bfile, "wb") as file:
                file.write(converted_string)

            ##########
            mycursor.execute('SELECT * FROM ds_post')
            dt = mycursor.fetchall()
            cutoff=10
            for rr in dt:
                hash0 = imagehash.average_hash(Image.open("static/comments/"+rr[8])) 
                hash1 = imagehash.average_hash(Image.open("static/comments/"+file_name))
                cc1=hash0 - hash1
                print("cc="+str(cc1))
                if cc1<=cutoff:
                    ss="ok"
                    pre_id=str(rr[0])
                    
                    break
                else:
                    ss="no"
            
            pmode= request.form['photo_mode']
            if pmode=="2":
                fullBlur(file_name,pid)
                fn2=file_name
                fn1="B"+file_name
            else:
                fn2=file_name
                fn1="F"+file_name
                shutil.copy("static/comments/"+file_name,"static/comments/"+fn1)
                blurImage(file_name,pid)
            
        else:
            file_name=""
            
        today = date.today()
        rdate = today.strftime("%d-%m-%Y")

        
        
        sql = "INSERT INTO ds_post (id,uname,detail,photo,rdate,status,photo_mode,pimage) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,detail,fn1,rdate,'0',pmode,fn2)
        mycursor.execute(sql,val)
        print(sql,val)
        mydb.commit()
        #msg="success"
        ###########
        if ss=="ok":
            mycursor.execute('SELECT * FROM ds_post where id=%s',(maxid,))
            sp3 = mycursor.fetchone()
            dtime=str(sp3[5])
            mycursor.execute('SELECT * FROM ds_post where id=%s',(pre_id,))
            sp1 = mycursor.fetchone()
            pre_user=sp1[1]
            mycursor.execute('SELECT * FROM ds_register where uname=%s',(pre_user,))
            sp2 = mycursor.fetchone()
            pre_vid=sp2[0]
            

            bdata1="ID:"+str(pre_vid)+", Username:"+pre_user+", Status:Attack Found, Similar Post by "+uname+", Post ID:"+str(maxid)+", (Previous ID:"+str(pre_id)+"), Date:"+dtime
            bdata11="ID:"+str(vid)+", Username:"+uname+", Status:image already exist, PID:"+str(maxid)+", Date:"+dtime
            msg1="attack"
            bdata2.append(bdata1)
            bdata2.append(bdata11)
        ########
        ###
        mycursor.execute('SELECT * FROM ds_post where id=%s',(maxid,))
        pdd1 = mycursor.fetchone()
        dtime=str(pdd1[5])

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:Post, PID:"+str(maxid)+", Date:"+dtime
        ###
        if pmode=="1":
            msg="suc"
            pid=str(maxid)
            #return redirect(url_for('set_photo',pid=str(maxid)))
        else:
            msg="success"

    ###post####
    #mycursor.execute('SELECT * FROM ds_post u,ds_register r where u.uname=r.uname order by u.id desc')
    #pdata = mycursor.fetchall()

    mycursor.execute('SELECT * FROM ds_post u,ds_register r where u.uname=r.uname order by u.id desc')
    dp1 = mycursor.fetchall()
    pdata=[]
    for dr1 in dp1:
        
        if dr1[1]==uname:
            pdata.append(dr1)
        else:
            mycursor.execute('SELECT count(*) FROM ds_contact where uname=%s && cname=%s && status=1',(uname,dr1[1]))
            tn = mycursor.fetchone()[0]
            mycursor.execute('SELECT count(*) FROM ds_contact where cname=%s && uname=%s && status=1',(uname,dr1[1]))
            tn2 = mycursor.fetchone()[0]
            if tn>0 and tn2>0:
                dt1="1"
                
                pdata.append(dr1)
            
                
       

    print(pdata)
    ###frnd req####
    s1=""
    s2=""
    s3=""
    j=0
    data2=[]
    uu2=[]
    mycursor.execute('SELECT * FROM ds_contact where uname=%s && status=0',(uname,))
    dd2 = mycursor.fetchall()
    for ds2 in dd2:
        
        mycursor.execute('SELECT * FROM ds_register where uname=%s',(ds2[2],))
        dd21 = mycursor.fetchone()
        data2.append(dd21)
        j+=1

    cn=j
    #######confirm############
    if act=="confirm":
        cname=request.args.get("cname")
        mycursor.execute("update ds_contact set status=1 where uname=%s && cname=%s && status=0",(uname,cname))
        mydb.commit()
        mycursor.execute("update ds_contact set status=1 where uname=%s && cname=%s && status=0",(cname,uname))
        mydb.commit()
        ###
        mycursor.execute('SELECT * FROM ds_contact where uname=%s && cname=%s && status=1',(cname,uname))
        cbq = mycursor.fetchone()
        dtime=str(cbq[4])

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:Confirm to "+cname+", Date:"+dtime
        ###
        msg="confirm"
        #return redirect(url_for('userhome',))


    if act=="reject":
        cname=request.args.get("cname")
        mycursor.execute("delete from ds_contact where cname=%s && uname=%s",(uname,cname))
        mydb.commit()
        mycursor.execute("delete from ds_contact where uname=%s && cname=%s",(uname,cname))
        mydb.commit()
        ###
        mycursor.execute("update ds_register set dstatus=0 where uname=%s",(uname,))
        mydb.commit()

        mycursor.execute('SELECT * FROM ds_register where uname=%s',(uname,))
        cbq2 = mycursor.fetchone()
        dtime=str(cbq2[11])

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:Reject to "+cname+", Date:"+dtime
        ###
        msg="reject"
        #return redirect(url_for('userhome'))

    if act=="no":
        cname=request.args.get("cname")
        mycursor.execute("delete from ds_contact where cname=%s && uname=%s",(uname,cname))
        mydb.commit()
        mycursor.execute("delete from ds_contact where uname=%s && cname=%s",(uname,cname))
        mydb.commit()
        ###
        mycursor.execute("update ds_register set dstatus=0 where uname=%s",(uname,))
        mydb.commit()

        mycursor.execute('SELECT * FROM ds_register where uname=%s',(uname,))
        cbq3 = mycursor.fetchone()
        dtime=str(cbq3[11])

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:Unfriend to "+cname+", Date:"+dtime
        ###
        msg="no"
        #return redirect(url_for('userhome'))
        
    ####new frnd#####
    data3=[]
    uu=[]
    mycursor.execute('SELECT * FROM ds_register where uname!=%s',(uname,))
    dd3 = mycursor.fetchall()
    for ds3 in dd3:
        
        mycursor.execute('SELECT count(*) FROM ds_contact where uname=%s && cname=%s',(uname,ds3[6]))
        cn1 = mycursor.fetchone()[0]
        mycursor.execute('SELECT count(*) FROM ds_contact where cname=%s && uname=%s',(uname,ds3[6]))
        cn2 = mycursor.fetchone()[0]

        if cn1>0 or cn2>0:
            ss=""
        else:
            ss="1"
            uu.append(ds3[6])
            
    cn3=len(uu)
    if cn3>0:
        for u1 in uu:
            mycursor.execute('SELECT * FROM ds_register where uname=%s',(u1,))
            dd4 = mycursor.fetchone()
            data3.append(dd4)

    
    #####send req######
    if act=="send":
        cname=request.args.get("cname")
        mycursor.execute("SELECT max(id)+1 FROM ds_contact")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO ds_contact(id,uname,cname,status) VALUES(%s,%s,%s,%s)"
        val = (maxid,uname,cname,'1')
        mycursor.execute(sql,val)
        mydb.commit()
        maxid2=maxid+1
        sql = "INSERT INTO ds_contact(id,uname,cname,status) VALUES(%s,%s,%s,%s)"
        val = (maxid2,cname,uname,'0')
        mycursor.execute(sql,val)
        mydb.commit()
        
        msg="sent"
        ###
        mycursor.execute('SELECT * FROM ds_contact where id=%s',(maxid,))
        cbq4 = mycursor.fetchone()
        dtime=str(cbq4[4])

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:Request to "+cname+", Date:"+dtime
        ### 
    #######my frnds############
    data4=[]
    u4=[]
    mycursor.execute('SELECT * FROM ds_register where uname!=%s',(uname,))
    dd4 = mycursor.fetchall()
    for ds4 in dd4:
        
        mycursor.execute('SELECT count(*) FROM ds_contact where uname=%s && cname=%s && status=1',(ds4[6],uname))
        ca1 = mycursor.fetchone()[0]
        mycursor.execute('SELECT count(*) FROM ds_contact where uname=%s && cname=%s && status=1',(uname,ds4[6]))
        ca2 = mycursor.fetchone()[0]

        if ca1>0 and ca2>0:           
            ss="1"
            u4.append(ds4[6])

    
    cn4=len(u4)
    if cn4>0:
        for u41 in u4:
            mycursor.execute('SELECT * FROM ds_register where uname=%s',(u41,))
            dd41 = mycursor.fetchone()
            data4.append(dd41)

    ###########request for view post#############################
    cn5=0
    s4=""
    
    data5=[]
    mycursor.execute('SELECT count(*) FROM ds_request where cname=%s && status=0',(uname,))
    cn5 = mycursor.fetchone()[0]
    
    if cn5>0:
        s4="1"
        mycursor.execute('SELECT * FROM ds_request where cname=%s && status=0',(uname,))
        dd5 = mycursor.fetchall()
        for ds5 in dd5:
            dt5=[]
            dt5.append(ds5[0])
            dt5.append(ds5[1])
            dt5.append(ds5[2])
            dt5.append(ds5[3])
            dt5.append(ds5[4])
            dt5.append(ds5[5])
            
            mycursor.execute('SELECT * FROM ds_register where uname=%s',(ds5[2],))
            dd51 = mycursor.fetchone()

            dt5.append(dd51[9])
            data5.append(dt5)

    ##
    if act=="acc":
        req_id=request.args.get("req_id")
        mycursor.execute("update ds_request set status=1 where id=%s",(req_id,))
        mydb.commit()
        ###
        mycursor.execute('SELECT * FROM ds_request where id=%s',(req_id,))
        cbq41 = mycursor.fetchone()
        dtime=str(cbq41[5])

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:Post Request Accepted for "+cbq41[2]+", PID:"+str(cbq41[1])+", Date:"+dtime
        ### 
        msg="acc"
    if act=="dec":
        req_id=request.args.get("req_id")
        mycursor.execute("update ds_request set status=2 where id=%s",(req_id,))
        mydb.commit()
        ###
        mycursor.execute('SELECT * FROM ds_request where id=%s',(req_id,))
        cbq42 = mycursor.fetchone()
        dtime=str(cbq42[5])

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:Post Request Declined for "+cbq42[2]+", PID:"+str(cbq42[1])+", Date:"+dtime
        ### 
        msg="dec"
    ######
    if cn>0:
        s1="1"
    if cn3>0:
        s2="1"
    if cn4>0:
        s3="1"
  

    return render_template('userhome.html',msg=msg,data=data,mess=mess,act=act,st=st,pdata=pdata,vid=vid,data2=data2,data3=data3,data4=data4,s1=s1,s2=s2,s3=s3,s4=s4,bc=bc,bdata=bdata,pid=pid,data5=data5,msg1=msg1,bdata2=bdata2)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    msg=""
    cnt=0
    uname=""
    mess=""
    bdata=""
    bc=""
    act=request.args.get("act")
    st=""
    pmode=""
    if 'username' in session:
        uname = session['username']
    #uname="raj"
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_register where uname=%s",(uname,))
    data = mycursor.fetchone()
    vid=data[0]

    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()

    ###post####
    mycursor.execute('SELECT * FROM ds_post u,ds_register r where u.uname=r.uname && u.uname=%s order by u.id desc',(uname,))
    dp1 = mycursor.fetchall()
    pdata=[]
    for dr1 in dp1:
        
        if dr1[1]==uname:
            pdata.append(dr1)
        else:
            mycursor.execute('SELECT count(*) FROM ds_contact where uname=%s && cname=%s && status=1',(uname,dr1[1]))
            tn = mycursor.fetchone()[0]
            mycursor.execute('SELECT count(*) FROM ds_contact where cname=%s && uname=%s && status=1',(uname,dr1[1]))
            tn2 = mycursor.fetchone()[0]
            if tn>0 and tn2>0:
                pdata.append(dr1)

    if act=="del":
        did=request.args.get("did")
        ###
        mycursor.execute("update ds_register set dstatus=0 where id=%s",(did,))
        mydb.commit()
        
        mycursor.execute('SELECT * FROM ds_post where id=%s',(did,))
        cbq6 = mycursor.fetchone()
        dtime=str(cbq6[5])

        mycursor.execute("delete from ds_post where id=%s",(did,))
        mydb.commit()

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:Remove Post (ID:"+str(did)+"), Date:"+dtime
        ### 
        msg="del"
        
        

    return render_template('profile.html',msg=msg,data=data,mess=mess,act=act,st=st,pdata=pdata,vid=vid,bc=bc,bdata=bdata)


    

@app.route('/set_photo', methods=['GET', 'POST'])
def set_photo():
    msg=""
    act=""
    bdata=""
    bc=""
    pid=request.args.get("pid")
    if 'username' in session:
        uname = session['username']
    #uname="raj"
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_register where uname=%s",(uname,))
    data = mycursor.fetchone()
    vid=data[0]

    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()

    mycursor.execute("SELECT * FROM ds_post where id=%s",(pid,))
    pdata = mycursor.fetchone()

    fn=pdata[8]
    
    dd="F"+pid+".txt"
    fz=open("static/group/"+dd,"r")
    num=fz.read()
    fz.close()
    nn=int(num)
    j=1
    fmg=[]
    while j<=nn:
        gg="g"+pid+"_"+str(j)+".jpg"
        fmg.append(gg)
        j+=1
    garr=[]
    if request.method == 'POST':
        gx=request.form.getlist("gx[]")
        print(gx)
        for g1 in gx:
            g2=g1.split(".")
            g3=g2[0].split("_")
            garr.append(g3[1])

        '''print(garr)
        c="2"
        if c in garr:
            print("yes")
        else:
            print("no")'''
        ##
        image = cv2.imread("static/comments/"+fn)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_detect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        face_data = face_detect.detectMultiScale(image, 1.3, 5)
        k=1
        print(garr)
        
        for (x, y, w, h) in face_data:
            kk=str(k)            
            print(x)
            print(y)
            print("**")
            if kk in garr:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = image[y:y+h, x:x+w]
                roi = cv2.GaussianBlur(roi, (23, 23), 30)
                image[y:y+roi.shape[0], x:x+roi.shape[1]] = roi
            else:
                roi = image[y:y+h, x:x+w]
                image[y:y+roi.shape[0], x:x+roi.shape[1]] = roi
                

            k+=1
        fnn="G"+fn
        cv2.imwrite("static/comments/"+fnn, image)
        ##
        mycursor.execute("update ds_post set pimage=%s where id=%s",(fn,pid))
        mydb.commit()

        mycursor.execute('SELECT * FROM ds_post where id=%s',(pid,))
        cbq5 = mycursor.fetchone()
        dtime=str(cbq5[5])
        uu=cbq5[1]

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:unblur image, Posted by "+uu+", Date:"+dtime
        ##
        msg="success"
        #return redirect(url_for('userhome'))
        
        
        
    return render_template('set_photo.html',msg=msg,data=data,act=act,fn=fn,fmg=fmg,bc=bc,bdata=bdata)

@app.route('/change_photo', methods=['GET', 'POST'])
def change_photo():
    msg=""
    cnt=0
    uname=""
    mess=""
    act=request.args.get("act")
    st=""
    
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_register where uname=%s",(uname,))
    data = mycursor.fetchone()
    vid=data[0]

    if request.method == 'POST':
    
        if 'file' not in request.files:
            flash('No file Part')
            return redirect(request.url)
        file= request.files['file']
        fname = uname+".jpg"
        file_name = secure_filename(fname)
        file.save(os.path.join("static/photo/", file_name))
        mycursor.execute("update ds_register set profile_st=1 where uname=%s",(uname,))
        mydb.commit()
        return redirect(url_for('userhome',vid=vid))

    if act=="rem":
        mycursor.execute("update ds_register set profile_st=0 where uname=%s",(uname,))
        mydb.commit()
        return redirect(url_for('userhome',vid=vid))

    return render_template('change_photo.html',msg=msg,data=data,act=act,vid=vid)


@app.route('/view', methods=['GET', 'POST'])
def view():
    msg=""
    cnt=0
    uname=""
    mess=""
    cname=request.args.get("cname")
    act=request.args.get("act")
    st=""
    pmode=""
    bc=""
    bdata=""

    f1=open("bc.txt","r")
    bc=f1.read()
    f1.close()
    
    if 'username' in session:
        uname = session['username']
    #uname="raj"
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_register where uname=%s",(uname,))
    data = mycursor.fetchone()
    vid=data[0]

    mycursor.execute("SELECT * FROM ds_register where uname=%s",(cname,))
    data2 = mycursor.fetchone()

    mycursor.execute('SELECT count(*) FROM ds_contact where uname=%s && cname=%s && status=1',(uname,cname))
    tn = mycursor.fetchone()[0]
    mycursor.execute('SELECT count(*) FROM ds_contact where cname=%s && uname=%s && status=1',(uname,cname))
    tn2 = mycursor.fetchone()[0]
    if tn>0 and tn2>0:
        st="1"
    else:
        st="2"
    ###post####
    mycursor.execute('SELECT * FROM ds_post u,ds_register r where u.uname=r.uname && u.uname=%s order by u.id desc',(cname,))
    pdata = mycursor.fetchall()
    #dp1 = mycursor.fetchall()
    '''pdata=[]


    
    for dr1 in dp1:
        
        if dr1[1]==cname:
            pdata.append(dr1)
        else:
            mycursor.execute('SELECT count(*) FROM ds_contact where uname=%s && cname=%s && status=1',(uname,dr1[1]))
            tn = mycursor.fetchone()[0]
            mycursor.execute('SELECT count(*) FROM ds_contact where cname=%s && uname=%s && status=1',(uname,dr1[1]))
            tn2 = mycursor.fetchone()[0]
            if tn>0 and tn2>0:
                pdata.append(dr1)'''

    if act=="req":
        pid=request.args.get("pid")
        mycursor.execute("SELECT * FROM ds_post where id=%s",(pid,))
        pp = mycursor.fetchone()
        uu=pp[1]
        ###
        mycursor.execute("SELECT max(id)+1 FROM ds_request")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO ds_request(id,pid,uname,cname,status) VALUES(%s,%s,%s,%s,%s)"
        val = (maxid,pid,uname,uu,'0')
        mycursor.execute(sql,val)
        mydb.commit()

        mycursor.execute("SELECT * FROM ds_post where id=%s",(pid,))
        pp2 = mycursor.fetchone()
        dtime=str(pp2[5])

        bdata="ID:"+str(vid)+", Username:"+uname+", Status:Request for view Post (PID:"+str(pid)+"), Date:"+dtime
        ### 
        msg="req"

        

    return render_template('view.html',msg=msg,data=data,mess=mess,act=act,st=st,pdata=pdata,vid=vid,data2=data2,bc=bc,bdata=bdata)


@app.route('/user_block', methods=['GET', 'POST'])
def user_block():
    msg=""
    cnt=0
    uname=""
    mess=""
    act=request.args.get("act")
    st=""
    pmode=""
    if 'username' in session:
        uname = session['username']
    #uname="raj"
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_register where uname=%s",(uname,))
    data = mycursor.fetchone()
    vid=data[0]
    key=data[10]
    
    return render_template('user_block.html',msg=msg,data=data,mess=mess,act=act,uname=uname,key=key)



def gen(camera):

    cursor = mydb.cursor()
    while True:
        frame = camera.get_frame()


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')






@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)


