# 程序

一个在命令行下，通过扇贝查询单词的程序。

查询过程中可以选择性得将其加入单词计划中。这个功能使用前，需要人工登录并记录下cookie。

# 使用

1. 程序在使用时会尝试读取~/.lshanbay/cookie文件作为发送http请求时所带的cookie。若没有这个文件，则会输出一行错误信息，但查询功能不受影响。

2. 直接使用命令行第一个参数指定要查询的单词
``` shell
python shanbay.py word
```

3. 使用参数-c指定查询时使用的cookie
``` shell
python shanbay.py -c "your cookie"
or
python shanbay.py --cookie "your cookie"
```

4. 在makefile中使用	pyinstaller将shanbay.py打包为一个可执行文件。make install会将其放在~/bin目录下，并建立~/.lshanbay/cookie文件。

# 例子
``` shell
$ python shanbay.py server
----------------------------------------
-> Server ['sɜːrvər]
 n. 服伺者,服勤者,伺候者
----------------------------------------
Definitions in English:
- 1: a person whose occupation is to serve at table (as in a restaurant)
- 2: (court games) the player who serves to start a point
- 3: (computer science) a computer that provides client stations with access to files and printers as shared resources to a computer network
----------------------------------------
```

``` shell
$ python shanbay.py -c "your cookie"
% python shanbay.py Valor
---------- UserId:   userId ----------
-> valor ['vælə] -0▄▅▆▇█-
 n. 勇气, 英勇，勇猛
----------------------------------------
Definitions in English:
- 1: the qualities of a hero or heroine; exceptional or heroic courage when facing danger (especially in battle)
----------------------------------------
A NEW word for you, learn it? [Y] for yes: yes
----------------------------------------
```

``` shell
% ./shanbay.py epitome
---------- UserId:   userId ----------
-> epitome [ɪ'pɪtəmi] -▃▄2▆▇█-
 n. 摘要, 缩影, 化身
----------------------------------------
Definitions in English:
- 1: a standard or typical example
- 2: a brief abstract (as of an article or book)
----------------------------------------
An OLD word for you, learn it? [Y] for yes: yes
----------------------------------------
```

``` shell
% ./shanbay.py shanbay    
---------- UserId:   userId ----------
Unknow word!
----------------------------------------
```
