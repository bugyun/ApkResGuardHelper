#!/usr/bin/python  
#-*-coding:utf-8-*-

# /**
#  * ================================================
#  * 作    者：若云
#  * 版    本：1.0.0
#  * 更新日期： 2018年02月28日
#  * 邮    箱：zyhdvlp@gmail.com
#  * ================================================
#  */

import os
import sys
#from lib import config
import platform
import shutil

#获取脚本文件的当前路径
def curFileDir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，
     #如果是脚本文件，则返回的是脚本的目录，
     #如果是编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

#判断当前系统
def isWindows():
  sysstr = platform.system()
  if("Windows" in sysstr):
    return 1
  else:
    return 0

#兼容不同系统的路径分隔符
def getBackslash():
	if(isWindows() == 1):
		return "\\"
	else:
		return "/"  

#当前脚本文件所在目录
parentPath = curFileDir() + getBackslash()

#config
libPath = parentPath + "lib" + getBackslash()
andResGuardPath = libPath + "AndResGuard-cli-1.2.12.jar"
outAndResGuardPath = parentPath + "andResGuard"
#protectedSourceApkPath = parentPath + config.protectedSourceApkName
moveApkOutResGuardPath = parentPath+"out"

t = []#创建一个唯一字符的集合
#读文件，判断是否之后一个后缀为apk的文件
apkFiles= os.listdir(parentPath) #得到文件夹下的所有文件名称
print ("**** 正在检测目录apk数量 ****")
for apkFile in apkFiles:
    if  "apk" in apkFile :
        t.append(apkFile)
        
if len(t) == 0:
  print ("**** 未发现apk，请把apk放入到当前目录中 ****")
elif len(t) > 1:
  print ("**** 请删除多余的apk文件，仅保留现有的apk ****")
else:
  print ("**** 正常执行代码 ****")
  protectedSourceApkName = t[0]
  protectedSourceApkPath = parentPath+protectedSourceApkName
  apkOutAndResGuardName = outAndResGuardPath+getBackslash()+protectedSourceApkName[0 : -4]+"_unsigned.apk"
  moveApkOutResGuardName=moveApkOutResGuardPath+getBackslash()+protectedSourceApkName[0 : -4]+"_resguard.apk"
  #AndResGuard资源混淆
  #java -jar /Users/fanpu/Desktop/ProtectedApkResignerForWalle-master/lib/AndResGuard-cli-1.2.10.jar /Users/fanpu/Desktop/ProtectedApkResignerForWalle-master/app-123-123.apk -out /Users/fanpu/Desktop/ProtectedApkResignerForWalle-master/andResGuard
  andResGuardShell = "java -jar " + andResGuardPath + " " + protectedSourceApkPath + " -out " + outAndResGuardPath
  #print(andResGuardShell)
  os.system(andResGuardShell)

  #创建目录
  if not os.path.exists(moveApkOutResGuardPath):
   os.mkdir(moveApkOutResGuardPath)
  else:
    shutil.rmtree(moveApkOutResGuardPath)               # 删除文件夹及其下所有文件
    os.mkdir(moveApkOutResGuardPath)

  #混淆完成之后，拷贝有有用的文件
  shutil.copyfile(apkOutAndResGuardName,moveApkOutResGuardName)

  #删除无用文件
  shutil.rmtree(outAndResGuardPath)               # 删除文件夹及其下所有文件
  print ("**** 执行代码完毕 ****")


