windows mecab 설치하기 위해서

https://github.com/Pusnow/mecab-python-msvc
에서 하는 대로 설치

[c:\mecab] mecab-ko-msvc를 설치하지 않았으면 설치해야 합니다.
[c:\mecab에 설치하며 약 70mega짜리임] mecab-ko-dic-msvc를 설치하지 않았으면 설치해야 합니다.
[mecab_python-0.996_ko_0.9.2_msvc-cp36-cp36m-win_amd64.whl pip install 로 설치함]실행 환경에 맞는 최신버전을 다운로드합니다. 32bit, 64bit 버전의 Python 2.7, 3.3, 3.4, 3.5, 3.6 을 지원합니다.
pip install <다운로드한 whl 파일> 로 설치할 수 있습니다. venv를 사용하지 않을 경우 관리자 권한이 필요합니다

설치하면 C:\ProgramData\Anaconda3\Lib\site-packages\mecab_python-0.996_ko_0.9.2_msvc.dist-info 로 들어감

C:\ProgramData\Anaconda3\Lib\site-packages\konlpy\tag  _mecab.py 
# def __init__(self, dicpath='/usr/local/lib/mecab/dic/mecab-ko-dic'):
    def __init__(self, dicpath='C:\\mecab\\mecab-ko-dic'): 


하기의 코드로 test해보고 제대로 설치되었는지 확인

#!/usr/bin/python
# -*- coding: utf-8 -*-

import MeCab
import sys
import string

sentence = "무궁화꽃이피었습니다."

try:
    print(MeCab.VERSION)

    t = MeCab.Tagger ()
    print(t.parse(sentence))

    m = t.parseToNode(sentence)
    while m:
        print(m.surface, "\t", m.feature)
        m = m.next
    print("EOS")

    lattice = MeCab.Lattice()
    t.parse(lattice)
    lattice.set_sentence(sentence)
    len = lattice.size()
    for i in range(len + 1):
        b = lattice.begin_nodes(i)
        e = lattice.end_nodes(i)
        while b:
            print("B[%d] %s\t%s" % (i, b.surface, b.feature))
            b = b.bnext 
        while e:
            print("E[%d] %s\t%s" % (i, e.surface, e.feature))
            e = e.bnext 
    print("EOS")

    d = t.dictionary_info()
    while d:
        print("filename: %s" % d.filename)
        print("charset: %s" %  d.charset)
        print("size: %d" %  d.size)
        print("type: %d" %  d.type)
        print("lsize: %d" %  d.lsize)
        print("rsize: %d" %  d.rsize)
        print("version: %d" %  d.version)
        d = d.next

except RuntimeError as e:
    print("RuntimeError:", e)
.
