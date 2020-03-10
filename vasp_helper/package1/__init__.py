'''
Copyright (c) 2020 马成 All rights reserved.
E-mail:15810063661@163.com
Last_modified:2020/3/10
'''
import tkinter as tk#pytho官方GUI包tkinter
import os, re, shutil, sys#系统，正则，文件处理, 系统
from tkinter import ttk#tkinter的进阶内容
from tkinter import filedialog#tkinter自带的文件对话框
from tkinter.simpledialog import *#tkinter自带的简单提问框
from tkinter.messagebox import *#tkinter自带的消息显示框
#初始化可能被摧毁的元素Lable列表
Old_Target_Elements = []
#默认预激活Tags
COMPLEX_RELAX_READY_ACTIVE_TAGS = []
#初始化认为POSCAR尚未读取
POSCAR_is_ready = False

class Tag:
    def __init__(self, Name, possibilities = None, Value = None):
        self.name = Name
        self.options =  possibilities.split(' | ')
        self.value = Value
        self.default = Value
        if Value in self.options:
            self.option = self.options.index(Value)
        else:
            self.option = len(self.options) - 1
        self.select = None#自定义时ttk.Combobox需要一个变量容器，实际不会访问tk.StringVar()
        self.frame = None#自定义值时放置控件(无法给出父容器)tk.Frame()
        self.name_button = None
        self.value_label = None
        self.label_content = None#显示自定义值的Label所用(无法在定义类时操作)tk.StringVar()
        self.ready_active = False
        self.active = False
    def SET(self, VALUE):
        self.ready_active = True#自定义时需要
        self.active = True#非自定义时需要
        if type(VALUE) == 'int':#可以给int型数字代表选项序号
            self.option = VALUE
            self.value = self.options[VALUE]
        else:#也可以直接给string型值
            self.value = VALUE
            if VALUE in self.options:
                self.option = self.options.index(VALUE)
            else:
                self.option = len(self.options) - 1
    def RESET(self):#初始化Tag
        self.value = self.default
        self.active = False
        self.ready_active = False

class Element:
    def __init__(self, Name, Family, Cycle, Sequence, Electrons = None):
        self.name = Name
        self.family = Family
        self.cycle = Cycle
        self.sequence = Sequence
        self.enmax = None
        self.electrons = Electrons
        self.frame = None
        self.name_label = None
        self.electrons_label = None
        self.df_electrons = (('d' in self.electrons) or ('f' in self.electrons))

class scrolled_frame:
    def __init__(self, Father):
        Father.resizable(0, 1)
        Father.update()
        self.main_frame = tk.Frame(Father)
        self.main_frame.pack(fill = 'both', expand = 1)
        self.canvas = tk.Canvas(self.main_frame, width = Father.winfo_width()-24, height = 0)
        self.canvas.pack(side = 'left', fill = 'both')
        self.vbar = tk.Scrollbar(self.main_frame, orient = 'vertical', bd = 0, width = 20)
        self.vbar.pack(side = 'right', fill = 'y')
        self.vbar.config(command = self.canvas.yview)
        self.canvas.config(yscrollcommand = self.vbar.set)
        self.frame = tk.Frame(self.canvas)
        self.frame.pack()
        self.canvas.create_window(int((Father.winfo_width()-24)/2), 0, window = self.frame)
        self.frame.bind("<Configure>", self.myfunction)
    def myfunction(self, event):
        self.canvas.config(scrollregion = self.canvas.bbox("all"))#弃用(功能不完善，不适合)

IBRION = Tag('IBRION' ,'-1 | 0 | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 44', '0')
ISTART = Tag('ISTART', '0 | 1 | 2 | 3', '0')
ISPIN = Tag('ISPIN', '1 | 2', '2')
ISYM = Tag('ISYM', '-1 | 0 | 1 | 2 | 3', '2')
LREAL = Tag('LREAL', '.TRUE. | .FALSE. | On | Auto', '.FALSE.')
ICHARG = Tag('ICHARG', '0 | 1 | 2 | 4', '2')
INIWAV = Tag('INIWAV', '0 | 1', '1')
MAGMOM = Tag('MAGMOM', '[real array]')
GGA = Tag('GGA', '91 | PE | RP | PS | AM', 'PS')
ISIF = Tag('ISIF', '0 | 1 | 2 | 3 | 4 | 5 | 6 | 7', '3')
NCORE = Tag('NCORE', '[integer]', '4')
NEDOS = Tag('NEDOS', '[integer]', '3001')
NBANDS = Tag('NBANDS', '[integer]')
ENCUT = Tag('ENCUT', '[real]')
ISMEAR = Tag('ISMEAR', '-5 | -4 | -3 | -2 | -1 | 0 | [integer]>0', '-5')
SIGMA = Tag('SIGMA', '[real]')
POTIM = Tag('POTIM', '[real]')
NELM = Tag('NELM', '[integer]')
NELMIN = Tag('NELMIN', '[integer]')
NELMDL = Tag('NELMDL', '[integer]')
EDIFF = Tag('EDIFF', '[real]', '1.00E-05')
NSW = Tag('NSW', '[integer]', 80)
EDIFFG = Tag('EDIFFG', '[real]', '-0.001')
PREC = Tag('PREC', 'Low | Medium | High | Normal | Single | Accurate', 'Accurate')
ALGO = Tag('ALGO', 'Normal | VeryFast | Fast', 'FAST')
ADDGRID = Tag('ADDGRID', '.TRUE. | .FALSE.')
LDAU = Tag('LDAU', '.TRUE. | .FALSE.')
LDAUTYPE = Tag('LDAUTYPE', '1 | 2 | 4', '2')
LDAUL = Tag('LDAUL', '[integer array]')
LDAUU = Tag('LDAUU', '[real array]')
LDAUJ = Tag('LDAUJ', '[real array]')
LMAXMIX = Tag('LMAXMIX', '[integer]')
GGA_COMPAT = Tag('GGA_COMPAT', '.TRUE. | .FALSE.')
LASPH = Tag('LASPH', '.TRUE. | .FALSE.')
IVDW = Tag('IVDW', '0 | 1 | 10 | 11 | 12 | 2 | 20 | 21 | 202 | 4', '0')
LORBIT = Tag('LORBIT', '0 | 1 | 2 | 5 | 10 | 11 | 12')
LWAVE = Tag('LWAVE', '.TRUE. | .FALSE.', '.FALSE.')
LCHARG = Tag('LCHARG', '.TRUE. | .FALSE.', '.TRUE.')
Tags = []
Tags.extend([IBRION, ISTART, ISPIN, ISYM, LREAL, ICHARG, INIWAV, MAGMOM, GGA, ISIF, NCORE, NEDOS, NBANDS, ENCUT, ISMEAR, SIGMA, POTIM, NELM, NELMIN, NELMDL, EDIFF, NSW, EDIFFG, PREC, ALGO, ADDGRID, LDAU, LDAUTYPE, LDAUL, LDAUU, LDAUJ, LMAXMIX, GGA_COMPAT, LASPH, IVDW, LORBIT, LWAVE, LCHARG])
Target_Elements = []

H = Element('H', 1, 1, 1, '1s1')
He = Element('He', 2, 8, 2, '1s2')
Li = Element('Li', 1, 2, 3, '[He]2s1')
Be = Element('Be', 2, 2, 4, '[He]2s2')
B = Element('B', 3, 2, 5, '[He]2s2 2p1')
C = Element('C', 4, 2, 6, '[He]2s2 2p2')
N = Element('N', 5, 2, 7, '[He]2s2 2p3')
O = Element('O', 6, 2, 8, '[He]2s2 2p4')
F = Element('F', 7, 2, 9, '[He]2s2 2p5')
Ne = Element('Ne', 8, 2, 10, '[He]2s2 2p6')
Na = Element('Na', 1, 3, 11, '[Ne]3s1')
Mg = Element('Mg', 2, 3, 12, '[Ne]3s2')
Al = Element('Al', 3, 3, 13, '[Ne]3s2 3p1')
Si = Element('Si', 4, 3, 14, '[Ne]3s2 3p2')
P = Element('P', 5, 3, 15, '[Ne]3s2 3p3')
S = Element('S', 6, 3, 16, '[Ne]3s2 3p4')
Cl = Element('Cl', 7, 3, 17, '[Ne]3s2 3p5')
Ar = Element('Ar', 8, 3, 18, '[Ne]3s2 3p6')
K = Element('K', 1, 4, 19, '[Ar]4s1')
Ca = Element('Ca', 2, 4, 20, '[Ar]4s2')
Sc = Element('Sc', -3, 4, 21, '[Ar]3d1 4s2')
Ti = Element('Ti', -4, 4, 22, '[Ar]3d2 4s2')
V = Element('V', -5, 4, 23, '[Ar]3d3 4s2')
Cr = Element('Cr', -6, 4, 24, '[Ar]3d4 4s2')
Mn = Element('Mn', -7, 4, 25, '[Ar]3d5 4s2')
Fe = Element('Fe', -8, 4, 26, '[Ar]3d6 4s2')
Co = Element('Co', -8, 4, 27, '[Ar]3d7 4s2')
Ni = Element('Ni', -8, 4, 28, '[Ar]3d8 4s2')
Cu = Element('Cu', -1, 4, 29, '[Ar]3d9 4s2')
Zn = Element('Zn', -2, 4, 30, '[Ar]3d10 4s2')
Ga = Element('Ga', 3, 4, 31, '[Ar]3d2 4s2 4p1')
Ge = Element('Ge', 4, 4, 32, '[Ar]3d2 4s2 4p2')
As = Element('As', 5, 4, 33, '[Ar]3d2 4s2 4p3')
Se = Element('Se', 6, 4, 34, '[Ar]3d2 4s2 4p4')
Br = Element('Br', 7, 4, 35, '[Ar]3d2 4s2 4p5')
Kr = Element('Kr', 8, 4, 36, '[Ar]3d2 4s2 4p6')
Rb = Element('Rb', 1, 5, 37, '[Kr]5s1')
Sr = Element('Sr', 2, 5, 38, '[Kr]5s2')
Y = Element('Y', -3, 5, 39, '[Kr]4d1 5s2')
Zr = Element('Zr', -4, 5, 40, '[Kr]4d2 5s2')
Nb = Element('Nb', -5, 5, 41, '[Kr]4d4 5s1')
Mo = Element('Mo', -6, 5, 42, '[Kr]4d5 5s1')
Tc = Element('Tc', -7, 5, 43, '[Kr]4d5 5s2')
Ru = Element('Ru', -8, 5, 44, '[Kr]4d7 5s1')
Rh = Element('Rh', -8, 5, 45, '[Kr]4d8 5s1')
Pd = Element('Pd', -8, 5, 46, '[Kr]4d10')
Ag = Element('Ag', -1, 5, 47, '[Kr]4d10 5s1')
Cd = Element('Cd', -2, 5, 48, '[Kr]4d10 5s2')
In = Element('In', 3, 5, 49, '[Kr]4d10 5s2 5p1')
Sn = Element('Sn', 4, 5, 50, '[Kr]4d10 5s2 5p2')
Sb = Element('Sb', 5, 5, 51, '[Kr]4d10 5s2 5p3')
Te = Element('Te', 6, 5, 52, '[Kr]4d10 5s2 5p4')
I = Element('I', 7, 5, 53, '[Kr]4d10 5s2 5p5')
Xe = Element('Xe', 8, 5, 54, '[Kr]4d10 5s2 5p6')
Cs = Element('Cs', 1, 6, 55, '[Xe]6s1')
Ba = Element('Ba', 2, 6, 56, '[Xe]6s2')
La = Element('La', -3, 6, 57, '[Xe]5d1 6s2')
Ce = Element('Ce', -3, 6, 58, '[Xe]4f1 5d1 6s2')
Pr = Element('Pr', -3, 6, 59, '[Xe]4f3 6s2')
Nd = Element('Nd', -3, 6, 60, '[Xe]4f4 6s2')
Pm = Element('Pm', -3, 6, 61, '[Xe]4f5 6s2')
Sm = Element('Sm', -3, 6, 62, '[Xe]4f6 6s2')
Eu = Element('Eu', -3, 6, 63, '[Xe]4f7 6s2')
Gd = Element('Gd', -3, 6, 64, '[Xe]4f7 5d1 6s2')
Tb = Element('Tb', -3, 6, 65, '[Xe]4f9 6s2')
Dy = Element('Dy', -3, 6, 66, '[Xe]4f10 6s2')
Ho = Element('Ho', -3, 6, 67, '[Xe]4f11 6s2')
Er = Element('Er', -3, 6, 68, '[Xe]4f12 6s2')
Tm = Element('Tm', -3, 6, 69, '[Xe]4f13 6s2')
Yb = Element('Yb', -3, 6, 70, '[Xe]4f14 6s2')
Lu = Element('Lu', -3, 6, 71, '[Xe]4f14 5d1 6s2')
Hf = Element('Hf', -4, 6, 72, '[Xe]4f14 5d2 6s2')
Ta = Element('Ta', -5, 6, 73, '[Xe]4f14 5d3 6s2')
W = Element('W', -6, 6, 74, '[Xe]4f14 5d4 6s2')
Re = Element('Re', -7, 6, 75, '[Xe]4f14 5d5 6s2')
Os = Element('Os', -8, 6, 76, '[Xe]4f14 5d6 6s2')
Ir = Element('Ir', -8, 6, 77, '[Xe]4f14 5d7 6s2')
Pt = Element('Pt', -8, 6, 78, '[Xe]4f14 5d9 6s1')
Au = Element('Au', -1, 6, 79, '[Xe]4f14 5d10 6s1')
Hg = Element('Hg', -2, 6, 80, '[Xe]4f14 5d10 6s2')
Tl = Element('Tl', 3, 6, 81, '[Xe]4f14 5d10 6s2 6p1')
Pb = Element('Pb', 4, 6, 82, '[Xe]4f14 5d10 6s2 6p2')
Bi = Element('Bi', 5, 6, 83, '[Xe]4f14 5d10 6s2 6p3')
Po = Element('Po', 6, 6, 84, '[Xe]4f14 5d10 6s2 6p4')
At = Element('At', 7, 6, 85, '[Xe]4f14 5d10 6s2 6p5')
Rn = Element('Rn', 8, 6, 86, '[Xe]4f14 5d10 6s2 6p6')
Fr = Element('Fr', 1, 7, 87, '[Rn]7s1')
Ra = Element('Ra', 2, 7, 88, '[Rn]7s2')
Ac = Element('Ac', -3, 7, 89, '[Rn]6d1 7s2')
Th = Element('Th', -3, 7, 90, '[Rn]6d2 7s2')
Pa = Element('Pa', -3, 7, 91, '[Rn]5f2 6d1 7s2')
U = Element('U', -3, 7, 92, '[Rn]5f3 6d1 7s2')
Np = Element('Np', -3, 7, 93, '')
Pu = Element('Pu', -3, 7, 94, '')
Am = Element('Am', -3, 7, 95, '')
Cm = Element('Cm', -3, 7, 96, '')
Bk = Element('Bk', -3, 7, 97, '')
Cf = Element('Cf', -3, 7, 98, '')
Es = Element('Es', -3, 7, 99, '')
Fm = Element('Fm', -3, 7, 100, '')
Md = Element('Md', -3, 7, 101, '')
No = Element('No', -3, 7, 102, '')
Lr = Element('Lr', -3, 7, 103, '')
Rf = Element('Rf', -4, 7, 104, '')
Db = Element('Db', -5, 7, 105, '')
Sg = Element('Sg', -6, 7, 106, '')
Bh = Element('Bh', -7, 7, 107, '')
Hs = Element('Hs', -8, 7, 108, '')
Mt = Element('Mt', -8, 7, 109, '')
Ds = Element('Ds', -8, 7, 110, '')
Rg = Element('Rg', -1, 7, 111, '')
Cn = Element('Cn', -2, 7, 112, '')
Nh = Element('Nh', 3, 7, 113, '')
Fl = Element('Fl', 4, 7, 114, '')
Mc = Element('Mc', 5, 7, 115, '')
Lv = Element('Lv', 6, 7, 116, '')
Ts = Element('Ts', 7, 7, 117, '')
Og = Element('Og', 8, 7, 118, '')
Elements = []
Elements.extend([H, He, Li, Be, B, C, N, O, F, Ne, Na, Mg, Al, Si, P, S, Cl, Ar, K, Ca, Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Cu, Zn, Ga, Ge, As, Se, Br, Kr, Rb, Sr, Y, Zr, Nb, Mo, Tc, Ru, Rh, Pd, Ag, Cd, In, Sn, Sb, Te, I, Xe, Cs, Ba, La, Ce, Pr, Nd, Pm, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu, Hf, Ta, W, Re, Os, Ir, Pt, Au, Hg, Tl, Pb, Bi, Po, At, Rn, Fr, Ra, Ac, Th, Pa, U, Np, Pu, Am, Cm, Bk, Cf, Es, Fm, Md, No, Lr, Rf, Db, Sg, Bh, Hs, Mt, Ds, Rg, Cn, Nh, Fl, Mc, Lv, Ts, Og])
