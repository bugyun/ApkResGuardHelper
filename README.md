# ApkResGuardHelper
基于 微信混淆 的无侵入的python脚本

# 资源混淆工具
一步解决应用资源混淆问题，自动生成资源混淆包
##使用场景
通过android studio生成正式包之后，然后把正式包放到本项目中的根目录下，即可生成混淆资源apk
## 用法：
- 修改lib目录下的config.xml，需要修改一下信息
    - whitelist 节点，path value="你的项目名称.R.mipmap.ic_launcher"
- 将正式apk放到跟目录下
    - 保证目录下有且只有一个apk文件
    - apk文件名称可以为任何名字
- 输出为out这个文件
- 运行命令 `python ApkResGuard.py`,即可自动生成所有渠道包。

## 支持平台：（需要python环境）
- Windows (Test)
- Mac OS (Test)
- Linux

### 配置文件[参考链接](https://github.com/shwenzhang/AndResGuard/blob/master/doc/how_to_work.zh-cn.md)
主要有五大项，即property，whitelist, keepmapping, compress,sign。

#### Property项

Property主要设置一些通用属性：

--sevenzip, 是否使用7z重新压缩签名后的apk包(这步一定要放在签名后，不然签名时会破坏效果)，需要我们安装7z命令行，同时加入环境变量中，同时要求输入签名信息(不然不会使用)。

Window：7z command line version, 即7za(http://www.7-zip.org/download.html)

Linux: 可直接sudo apt-get install p7zip-full。

注意：效果很好，推荐使用，并且在Linux(Mac的高富帅也可)上。

--metaname, 由于重打包时需要删除签名信息，考虑到这个文件名可能会被改变，所以使用者可手动输入签名信息对应的文件名。默认为META_INF。

--keeproot, 是否将res/drawable混淆成r/s

#### Whitelist项

Whitelist主要是用来设置白名单，由于我们代码中某些资源会通过getIdentifier(需要全局搜索所有用法并添加到白名单)或动态加载等方式，我们并不希望混淆这部分的资源ID：

--isactive, 是否打开白名单功能；

--path, 是白名单的项，格式为package_name.R.type.specname,由于一个resources.arsc中可能会有多个包，所以这里要求写全包名。同时支持*，？通配符，例如: com.tencent.mm.R.drawable.emoji_*、com.tencent.mm.R.drawable.emoji_？；

注意:1.不能写成com.tencent.mm.R.drawable.emoji.png，即带文件后缀名；2. 通配符代表.+,即a,不能匹配到a；



#### Keepmapping项

Keepmapping主要用来指定旧的mapping文件，为了保持一致性，我们支持输入旧的mapping文件，可保证同一资源文件在不同版本混淆后的名称保持一致。另一方面由于我们需要支持增量下载方式，如果每次改动都导致所有文件名都会更改，这会导致增量文件增大，但测试证明影响并不大(后面有测试数据)。

--isactive, 是否打开keepmapping模式；

--path, 是旧mapping文件的位置，linux用/, window用 ;



#### Compress项

Compress主要用来指定文件重打包时是否压缩指定文件，默认我们重打包时是保持输入apk每个文件的压缩方式(即Stored或者Deflate)。一般来说，1、在2.3版本以下源文件大于1M不能压缩；2、流媒体不能压缩。对于.png、.jpg是可以压缩的，只是AssetManger读取时候的方式不同。

--isactive, 是否打开compress模式；

--path, 是需要被压缩文件的相对路径(相对于apk最顶层的位置)，这里明确一定要使用‘/’作为分隔符，同时支持通配符*，？，例如*.png(压缩所有.png文件)，res/drawable/emjio_?.png，resouces.arsc(压缩 resources.arsc)

注意若想得到最大混淆：

输入四项个path:*.png, *.jpg, *.jpeg, *.gif

若你的resources.arsc原文件小于1M，可加入resourcs.arsc这一项！若不需要支持低版本，直接加入也可。



#### Sign项

Sign主要是对处理后的文件重签名，需要我们输入签名文件位置，密码等信息。若想使用7z功能就一定要填入相关信息。

--isactive, 是否打开签名功能；

--path, 是签名文件的位置，linux用/, window用 ;

--storepass, 是storepass的数值;

--keypass, 是keypass的数值;

--alias, 是alias的数值；



## Android资源混淆工具需要注意的问题
compress参数对混淆效果的影响 若指定compess 参数.png、.gif以及*.jpg，resources.arsc会大大减少安装包体积。若要支持Android2.2以及以下版本的设备，resources.arsc需保证压缩前小于1M。

操作系统对7z的影响 实验证明，linux与mac的7z效果更好

keepmapping方式对增量包大小的影响 影响并不大，但使用keepmapping方式有利于保持所有版本混淆的一致性

渠道包的问题(建议通过修改zip摘要的方式生产渠道包) 在出渠道包的时候，解压重压缩会破坏7zip的效果，通过repackage命令可用7zip重压缩。

若想通过getIdentifier方式获得资源，需要放置白名单中。 部分手机桌面快捷图标的实现有问题，务必将程序桌面icon加入白名单。

对于一些第三方sdk,例如友盟，可能需要将部分资源添加到白名单中。

    <issue id="whitelist" isactive="true">
        <path value ="yourpackagename.R.string.umeng*" />   
        <path value ="yourpackagename.R.layout.umeng*" />
        <path value ="yourpackagename.R.drawable.umeng*" />
        <path value ="yourpackagename.R.anim.umeng*" />
        <path value ="yourpackagename.R.color.umeng*" />
        <path value ="yourpackagename.R.style.*UM*" />
        <path value ="yourpackagename.R.style.umeng*" />
        <path value ="yourpackagename.R.id.umeng*" />
        <path value ="yourpackagename.R.string.com.crashlytics.*" />
    </issue>


