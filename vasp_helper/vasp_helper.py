'''
Copyright (c) 2020 马成 All rights reserved.
E-mail:15810063661@163.com
Last_modified:2020/3/10
'''
from package1 import *

def main():
    INI()
    WINDOW()
    main_frame_window = tk.Frame(window)
    main_frame_window.pack(side = 'top')
    frame1_window = tk.Frame(main_frame_window)
    frame1_window.pack(pady = 10)
    frame2_window = tk.Frame(main_frame_window)
    frame2_window.pack()
    frame3_window = tk.Frame(main_frame_window)
    frame3_window.pack(pady = 10)
    frame4_window = tk.Frame(main_frame_window)
    frame4_window.pack()
    POSCAR_button = tk.Button(frame1_window, text = 'POSCAR', font = ('Arial', 10), fg = 'white', bg = 'red', command = lambda: Read_POSCAR(POSCAR_button, main_frame_window))
    POSCAR_button.pack()
    Pre_read_POSCAR(POSCAR_button, main_frame_window)
    relax_button = tk.Button(frame2_window, text = 'relax', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Relax)
    relax_button.pack(side = 'left', padx = 10)
    converge_test_button = tk.Button(frame2_window, text = 'converge_test', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Converge_test)
    converge_test_button.pack(side = 'left')
    SCF_button = tk.Button(frame3_window, text = 'self_consistent_filed', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Self_consistent_filed)
    SCF_button.pack()
    DoS_button = tk.Button(frame4_window, text = 'density_of_states', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Density_of_states)
    DoS_button.pack(side = 'left', padx = 10)
    u_test_button = tk.Button(frame4_window, text = 'u_test', font = ('Arial', 10), fg = 'white', bg = 'blue', command = U_test)
    u_test_button.pack(side = 'left')
    window.mainloop()
    return True

def Read_POSCAR(POSCAR_button, main_frame_window):
    def Check_POSCAR():
        global POSCAR_is_ready#需要修改状态
        POSCAR_is_ready = False#先默认错误
        if len(POSCAR) < 6:#防止未选择有效地址
            showinfo('提示', '请选择正确格式的POSCAR')
            return False
        else:
            result = True
            target_elements = POSCAR[5].strip().split()
            for target_element in target_elements:
                target_flag = False
                for element in Elements:
                    if element.name == target_element:
                        target_flag = True
                        Target_Elements.append(element)
                result = result * target_flag
                if target_flag == False:
                    result = False
                    showinfo('提示', 'can not find element {}!'.format(target_element))
            POSCAR_is_ready = result
    def Tag():#新增元素信息Label控件
        global Old_Target_Elements
        Untag()#新增前先删除之前的
        for target_element in Target_Elements:
            Old_Target_Elements.extend([target_element])
            target_element.frame = tk.Frame(main_frame_window)
            target_element.frame.pack(side = 'left', padx = 20)
            target_element.name_label = tk.Label(target_element.frame, text = '{}'.format(target_element.name), fg = 'white', bg = 'green', font = ('Arial',10), width = 3)
            target_element.name_label.pack(pady = 10)
            target_element.electrons_label = tk.Label(target_element.frame, text = '{}'.format(target_element.electrons), fg = 'white', bg = 'green', font = ('Arial',10))
            target_element.electrons_label.pack()
            if 'd' in target_element.electrons and 'd10' not in target_element.electrons:
                target_element.name_label.config(bg = 'purple')
                target_element.electrons_label.config(bg = 'purple')
            if 'f' in target_element.electrons and 'f14' not in target_element.electrons:
                target_element.name_label.config(bg = 'red')
                target_element.electrons_label.config(bg = 'red')
    def Untag():#删除元素信息Label控件
        global Old_Target_Elements
        if Old_Target_Elements:
            for old_target_element in Old_Target_Elements:
                old_target_element.electrons_label.pack_forget()
                old_target_element.name_label.pack_forget()
                old_target_element.frame.pack_forget()
            Old_Target_Elements = []
    def Count_atoms():
        global TOTAL_ATOMS
        TOTAL_ATOMS = 0
        ATOMS = POSCAR[6].strip().split()
        for atom in ATOMS:
            TOTAL_ATOMS = TOTAL_ATOMS + int(atom)
    def Get_ENMAX():
        global MAX_ENMAX
        ENMAX = []#存放所有元素的ENMAX
        for element in Target_Elements:
            path = '{}\{}\POTCAR'.format(PAW_PATH, element.name)
            with open(path, 'r') as file:
                for line in file.readlines():
                    if 'ENMAX' in line:
                        #正则表达式找到=和；之间的值并加入列表
                        enmax = r'=(.*?);'
                        element.enmax = int(float(re.findall(enmax, line.replace(' ',''))[0]))
                        ENMAX.extend([element.enmax])
        MAX_ENMAX = max(ENMAX)
        ENCUT.value = MAX_ENMAX
    def Get_unitcell_constant():
        global A_constant
        global B_constant
        global C_constant
        A_constant = ((float(POSCAR[2].strip().split()[0])**2 + float(POSCAR[2].strip().split()[1])**2 + float(POSCAR[2].strip().split()[2])**2)**0.5)*float(POSCAR[1])
        B_constant = ((float(POSCAR[3].strip().split()[0])**2 + float(POSCAR[3].strip().split()[1])**2 + float(POSCAR[3].strip().split()[2])**2)**0.5)*float(POSCAR[1])
        C_constant = ((float(POSCAR[4].strip().split()[0])**2 + float(POSCAR[4].strip().split()[1])**2 + float(POSCAR[4].strip().split()[2])**2)**0.5)*float(POSCAR[1])
        #print(A_constant)
        #print(B_constant)
        #print(C_constant)
    global POSCAR#POSCAR可能被多个函数读
    global POSCAR_path#生成POSCAR时需要原文件路径
    Target_Elements.clear()#每次进入都要清空重读
    POSCAR_path = filedialog.askopenfilename(title = u'选择POSCAR', initialdir = INI_POSCAR_PATH)#选择POSCAR
    if len(POSCAR_path) == 0:#防止未选择地址
        return False
    else:#打开POSCAR查看并检查
        with open(POSCAR_path, 'r', encoding = 'utf-8') as file:
            POSCAR = [line.strip() for line in file]
        Check_POSCAR()
        if POSCAR_is_ready:#检查无误后找到目标元素的POTCAR并提取出ENMAX值
            Count_atoms()
            Get_ENMAX()
            Get_unitcell_constant()
            POSCAR_button.config(bg = 'green')
            Tag()
            return True
        else:#检查有误，则将之前的Label都删除
            POSCAR_button.config(bg = 'red')
            Untag()
            return False

def Creat_INCAR(job):
    with open('{}\INCAR'.format(work_path), 'w', newline = '\n', encoding = 'utf-8') as INCAR:
        INCAR.write('SYSTEM = {}_{}\n'.format(system_name, job))#INCAR的第一行为系统名
        for tag in Tags:
            if tag.active:#判断是否激活
                INCAR.write('{} = {}\n'.format(tag.name, tag.value))
                tag.active = False

def Creat_POTCAR():
    with open('{}\POTCAR'.format(work_path), 'w', newline = '\n', encoding = 'utf-8') as POTCAR:#将目标元素POTCAR一一取出修改并写入新的POTCAR整合
        for element in Target_Elements:
            path = '{}\{}\POTCAR'.format(PAW_PATH, element.name)
            with open(path, 'r') as file:
                for line in file.readlines():
                    if 'LEXCH' in line:
                        line = line.replace('PE', GGA.value)#替换交换关联能的近似方式
                    POTCAR.write(line)

def Creat_KPOINTS(job):
    with open('{}\KPOINTS'.format(work_path), 'w', newline = '\n', encoding = 'utf-8') as KPOINTS:
        KPOINTS.write('automatic\n0\nGamma\n')#此处用的都是以Gamma点为中心自动生成K点的方式
        if job == 'easy_relax' or job == 'main_converge_test' or job == 'encut_converge_test' or job == 'sigma_converge_test' or job == 'kpoints_converge_test' or job == 'density_of_states' or job == 'u_test':
            K_mesh = '{} {} {}\n0.0 0.0 0.0\n'.format(int(25.0/A_constant), int(25.0/B_constant), int(25.0/C_constant))
        if job == 'hard_relax' or job == 'complex_relax' or job == 'self_consistent_filed':
            K_mesh = '{} {} {}\n0.0 0.0 0.0\n'.format(int(40.0/A_constant), int(40.0/B_constant), int(40.0/C_constant))
        KPOINTS.write(K_mesh)

def Creat_script(job):
    with open('{}\\run.sh'.format(work_path), 'w', newline = '\n', encoding = 'utf-8') as Script:
        #设置环境变量和一些SBATCH关键参数
        Script.write("#!/bin/sh\n")#告诉shell此脚本使用/bin/sh来解释执行
        Script.write("#SBATCH -N {}\n#SBATCH -n {}\n#SBATCH -p paratera\n#SBATCH -J MC_{}\n".format(NODES, CORES, job))#告诉slurm系统一些必须参数
        Script.write("start_time=$(date +%s)\n")#1970以来的时间(秒)
        Script.write("date=$(date +'%Y-%m-%d %H:%M:%S')\n")#显示当前的时间(年-月-日 时:分:秒)
        Script.write("echo ran at $date > output\n")
        Script.write("source vasp_environment\n")#设置一系列临时环境变量并加载vasp的编译器，已写入脚本放入$PATH中一个目录下;source表示在当前shell下执行脚本
        if job == 'easy_relax' or job == 'hard_relax' or job == 'complex_relax':
            Script.write("relax\n")#已写入脚本放入$PATH中一个目录下
        if job == 'main_converge_test':
            Script.write("encut_converge\n")#已写入脚本放入$PATH中一个目录下
            Script.write("kpoints_converge\n")#已写入脚本放入$PATH中一个目录下
            if SIGMA_TEST:
                Script.write("sed -i 's/ISMEAR = -5/ISMEAR = 0/' INCAR\n")
                Script.write("echo SIGMA = 0 >> INCAR\n")#已写入脚本放入$PATH中一个目录下
                Script.write("sigma_converge\n")#已写入脚本放入$PATH中一个目录下
        if job == 'encut_converge_test':
            Script.write("encut_converge\n")
        if job == 'sigma_converge_test':
            Script.write("sigma_converge\n")
        if job == 'kpoints_converge_test':
            Script.write("kpoints_converge\n")
        if job == 'self_consistent_filed':
            Script.write("yhrun vasp_std\n")
        if job == 'density_of_states':
            Script.write("yhrun vasp_std\n")
            Script.write("density_of_states\n")
        if job == 'u_test':
            Script.write("u_test {}\n".format(GAP))
        Script.write("end_time=$(date +%s)\n")#1970以来的时间(秒)
        Script.write("task_time=$(echo $end_time $start_time | awk '{print ($1 - $2)}')\n")#跑这个任务所花时间(秒)
        Script.write("printf 'task costs %d:%02d:%02d\{}' $(($task_time / 3600)) $(((($task_time % 3600)) / 60)) $(($task_time%60)) >> output\n".format('n'))
        
def Creat_files(job):
    def Creat_folder():#先生成文件夹
        global work_path#最终生成文件的存放路径
        global system_name#生成INCAR可以用
        system_name = ''#用于产生所算系统的名称
        for element in Target_Elements:
            system_name = system_name + element.name
        system_path = '{}\{}'.format(DESKTOP_PATH, system_name)#所算系统的文件夹路径
        if os.path.isdir(system_path) == False:
            os.mkdir(system_path)
        work_path = '{}\{}'.format(system_path, job)
        if os.path.isdir(work_path) == False:
            os.mkdir(work_path)
    def Creat_POSCAR():
        shutil.copyfile(POSCAR_path, '{}\POSCAR'.format(work_path))
    Creat_folder()
    Creat_POSCAR()
    Creat_POTCAR()
    Creat_INCAR(job)
    Creat_KPOINTS(job)
    Creat_script(job)
    print('{} finished'.format(job))

def Relax():
    def Easy_relax():#一般的结构优化，计算精度和收敛条件较低
        if(Set_value('easy_relax')):#其实这种情况只会返回True。。但是这样写比较工整
            Creat_files('easy_relax')
            return True
        else:
            return False
    def Hard_relax():#高级的结构优化，计算精度较和收敛条件较高
        if(Set_value('hard_relax')):
            Creat_files('hard_relax')
            return True
        else:
            return False
    def Complex_relax():#复杂的结构优化，可以自定义INCAR内容
        Customize('complex_relax', relax)
        return True
    if Check_POSCAR():
        Reset_tags()#一旦点击relax便重置Tags
        relax = tk.Toplevel(window)
        relax.title('Relax')
        size = '{}x{}+{}+{}'.format(int(WIDTH), int(HEIGHT), window.winfo_x() + window.winfo_width(), int((window.winfo_screenheight()-int(HEIGHT))/2))
        relax.geometry(size)
        main_frame_relax = tk.Frame(relax)
        main_frame_relax.pack()
        easy_relax_button = tk.Button(main_frame_relax, text = 'easy_relax', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Easy_relax)
        easy_relax_button.pack(pady = 10)
        hard_relax_button = tk.Button(main_frame_relax, text = 'hard_relax', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Hard_relax)
        hard_relax_button.pack()
        complex_relax_button = tk.Button(main_frame_relax, text = 'complex_relax', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Complex_relax)
        complex_relax_button.pack(pady = 10)
        return True

def Converge_test():
    def Main_test():#一次性将ENCUT、KPOINTS、SIGMA(有可能不测试)全测试
        global SIGMA_TEST
        SIGMA_TEST = tk.messagebox.askquestion('提示', '是否测试SIGMA')
        if (Set_value('main_converge_test')):
            Creat_files('main_converge_test')
            return True
        else:
            return False
    def Encut_test():
        Set_value('encut_converge_test')
        Creat_files('encut_converge_test')
    def Kpoints_test():
        Set_value('kpoints_converge_test')
        Creat_files('kpoints_converge_test')
    def Sigma_test():
        Set_value('sigma_converge_test')
        Creat_files('sigma_converge_test')
    if Check_POSCAR():
        converge_test = tk.Toplevel(window)
        converge_test.title('Converge_test')
        size = '{}x{}+{}+{}'.format(int(WIDTH), int(HEIGHT), window.winfo_x() + window.winfo_width(), int((window.winfo_screenheight()-int(HEIGHT))/2))
        converge_test.geometry(size)
        main_frame_converge_test = tk.Frame(converge_test)
        main_frame_converge_test.pack()
        frame1 = tk.Frame(main_frame_converge_test)
        frame1.pack()
        frame2 = tk.Frame(main_frame_converge_test)
        frame2.pack()
        main_test = tk.Button(frame1, text = 'main_test', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Main_test)
        main_test.pack(pady = 10)
        encut_test = tk.Button(frame2, text = 'encut_test', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Encut_test)
        encut_test.pack(side = 'left')
        kpoints_test = tk.Button(frame2, text = 'kpoints_test', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Kpoints_test)
        kpoints_test.pack(side = 'left', padx = 20)
        sigma_test = tk.Button(frame2, text = 'sigma_test', font = ('Arial', 10), fg = 'white', bg = 'blue', command = Sigma_test)
        sigma_test.pack(side = 'left')

def Self_consistent_filed():
    if Check_POSCAR():
        if (Set_value('self_consistent_filed')):
            Creat_files('self_consistent_filed')   
            return True
        else:
            return False

def Density_of_states():
    if Check_POSCAR():
        if (Set_value('density_of_states')):
            Creat_files('density_of_states')
            return True
        else:
            return False

def U_test():
    if Check_POSCAR():
        if (Set_value('u_test')):
            Creat_files('u_test')
            return True
        else:
            return False

def Customize(job, Father):
    def Confirm():
        for tag in Tags:#正式激活所有Tag
            tag.active = tag.ready_active
            tag.ready_active = False
        big_customize.destroy()
        Creat_files(job)
        return True
    def Select(tag, frame):
        def Assignment(Select_box, tag):
            if '[' not in Select_box.get():#如果选择的值不含'['即选择了预设可能值
                tag.ready_active = True#选择则自动预激活
                tag.name_button.config(bg = 'green')
                tag.value = Select_box.get()
                tag.label_content.set(tag.value)#修改选择值显示内容
                return True
            else:#如果选择的值包含'['即选择了要输入自定义值
                Value = askstring('请输入', prompt='{} = '.format(tag.name), initialvalue = tag.value)
                if Value:#如果给的值不为空
                    tag.ready_active = True#自动预激活
                    tag.name_button.config(bg = 'green')
                    tag.value = Value.strip()#改Tag的值
                    tag.label_content.set(tag.value)#修改自定义值显示内容
                    return True
                else:#如果给的值为空则返回False
                    return False
        def Active(tag):#每次点击改变预激活状态
            if tag.ready_active:
                tag.ready_active = False
                tag.name_button.config(bg = 'red')
                return True
            else:
                tag.ready_active = True
                tag.name_button.config(bg = 'green')
                return True
        tag.label_content = tk.StringVar()#显示自定义值的Label所用(无法在定义类时操作)
        tag.frame = tk.Frame(frame)
        tag.frame.pack(side = 'top', pady = 8)
        #显示Tag名的按键
        tag.name_button = tk.Button(tag.frame, text = '{}'.format(tag.name), font = ('Arial', 10), bg = 'red', fg = 'white', command = lambda: Active(tag), width = 13)
        tag.name_button.pack(side = 'left') 
        if tag.ready_active:#按键颜色代表预激活状态
            tag.name_button.config(bg = 'green')#红色未预激活，绿色预激活
        #包含Tag可能值的下拉框
        tag.select = tk.StringVar()#ttk.Combobox需要一个tk.StringVar()的变量容器，实际不会访问
        select_box = ttk.Combobox(tag.frame, state = 'readonly', values = tag.options, textvariable = tag.select, width = 12)
        select_box.current(tag.option)
        select_box.bind('<<ComboboxSelected>>', lambda _ : Assignment(select_box, tag))#绑定选择下拉框虚拟事件和Assignment函数并利用lambda传参
        select_box.pack(side = 'left', padx = 20)
        tag.value_label = tk.Label(tag.frame, textvariable = tag.label_content, fg = 'white', bg = 'blue', font = ('Arial',10), width = 7)
        tag.value_label.pack()
        tag.label_content.set(tag.value)
    Reset_tags()
    customize = tk.Toplevel(Father)
    size = '{}x{}+{}+{}'.format(window.winfo_screenwidth(), window.winfo_screenheight(), -8, 0)
    customize.geometry(size)
    customize.title('eighth_test')
    root_frame = tk.Frame(customize)
    root_frame.pack()
    main_frame = tk.Frame(root_frame)
    main_frame.pack()
    confirm_frame = tk.Frame(root_frame)
    confirm_frame.pack(pady = 100)
    frame_1 = tk.Frame(main_frame)
    frame_1.pack(side = 'left', padx = 30, anchor = 'n')
    frame_2 = tk.Frame(main_frame)
    frame_2.pack(side = 'left', padx = 30, anchor = 'n')
    frame_3 = tk.Frame(main_frame)
    frame_3.pack(side = 'left', padx = 30, anchor = 'n')
    frame_4 = tk.Frame(main_frame)
    frame_4.pack(side = 'left', padx = 30, anchor = 'n')
    #提前检测是否范德华材料
    if int(float(POSCAR[1])*float(POSCAR[4].split()[2])) > int(VDW_THRESHOLD):#是否范德华材料
        IVDW.SET('11')#直接设置预激活和值
        #最后检测半满df轨道元素
    Check_half_df_element()#是否含半满df轨道元素
    ###########################################
    if job == 'complex_relax':#分情况设置预激活
        for necessary in COMPLEX_RELAX_READY_ACTIVE_TAGS:
            for tag in Tags:
                if tag.name == necessary:
                    tag.ready_active = True
    ###########################################
    label_1 = tk.Label(frame_1, text = 'algorithm', font = ('Arial', 15), bg = 'blue', fg = 'white')
    label_1.pack(pady = 10)
    label_2 = tk.Label(frame_2, text = 'precision', font = ('Arial', 15), bg = 'blue', fg = 'white')
    label_2.pack(pady = 10)
    label_3 = tk.Label(frame_3, text = 'special', font = ('Arial', 15), bg = 'blue', fg = 'white')
    label_3.pack(pady = 10)
    label_4 = tk.Label(frame_4, text = 'output', font = ('Arial', 15), bg = 'blue', fg = 'white')
    label_4.pack(pady = 10)
    for tag in IBRION, ISTART, ISPIN, ISYM, LREAL, ICHARG, INIWAV, MAGMOM, GGA, ISIF, NCORE, NEDOS, NBANDS:
        Select(tag, frame_1)
    for tag in ENCUT, ISMEAR, SIGMA, POTIM, NELM, NELMIN, NELMDL, EDIFF, NSW, EDIFFG, PREC, ALGO, ADDGRID:
        Select(tag, frame_2)
    for tag in LDAU, LDAUTYPE, LDAUL, LDAUU, LDAUJ, LMAXMIX, GGA_COMPAT, LASPH, IVDW:
        Select(tag, frame_3)
    for tag in LORBIT, LWAVE, LCHARG:
        Select(tag, frame_4)
    confirm_buttton = tk.Button(confirm_frame, text = 'Done', font = ('Arial', 15), bg = 'blue', fg = 'white', command = Confirm)
    confirm_buttton.pack()

def Check_POSCAR():
    if POSCAR_is_ready:
        return True
    else:
        showinfo('提示', 'please give POSCAR first')
        return False

def Check_half_df_element():#判断是否有半满df轨道的元素
    half_df_element = False#先认为没有
    lmaxmix = '2'#如果有，帮助设置LMAXMIX
    ldauj = ''#如果有，帮助设置LDAUJ
    ldaul = ''#如果有，帮助设置LDAUL
    for element in Target_Elements:
        ldauj = ldauj + '0 '
        if 'f' in element.electrons and 'f14' not in element.electrons:#含半满f轨道
            ldaul = ldaul + '3 '
            lmaxmix = '6'
        elif 'd' in element.electrons and 'd10' not in element.electrons:#含半满d轨道
            ldaul = ldaul + '2 '
            if  lmaxmix != '6':#取最大，不能往小取
                lmaxmix = '4'
        else:
            ldaul = ldaul + '-1 '
        if element.df_electrons:
            half_df_element = True
    ldauj = ldauj.strip()#抹去最后一个空格
    ldaul = ldaul.strip()
    if half_df_element:
        ISPIN.SET('2')
        VALUE = askstring('检测到半满df轨道元素', prompt='U - J = ', initialvalue = None)
        if VALUE:
            LDAUU.SET(VALUE.strip())
            LDAU.SET('.TRUE.')
            LDAUTYPE.SET('2')
            LDAUL.SET(ldaul)
            LDAUJ.SET(ldauj)
            LASPH.SET('.TRUE.')
            LMAXMIX.SET(lmaxmix)
            return True
        else:
            return False
    else:
        ISPIN.SET('1')
        return True

def Set_value(job):#此函数只能根据job直接设置Tags
    def U_test_set():
        half_df_element = False#先认为没有
        lmaxmix = '2'#帮助设置LMAXMIX
        ldauj = ''#帮助设置LDAUJ
        ldauu = ''#帮助设置LDAUU
        ldaul = ''#帮助设置LDAUL
        for element in Target_Elements:
            ldauj = ldauj + '0 '
            if 'f' in element.electrons and 'f14' not in element.electrons:#含半满f轨道
                ldaul = ldaul + '3 '
                ldauu = ldauu + 'U_test '
                lmaxmix = '6'
            elif 'd' in element.electrons and 'd10' not in element.electrons:#含半满d轨道
                ldaul = ldaul + '2 '
                ldauu = ldauu + 'U_test '
                if  lmaxmix != '6':#取最大，不能往小取
                    lmaxmix = '4'
            else:
                ldaul = ldaul + '-1 '
                ldauu = ldauu + '0 '
            if element.df_electrons:
                half_df_element = True
        if half_df_element:
            ldauj = ldauj.strip()#抹去最后一个空格
            ldaul = ldaul.strip()
            ldauu = ldauu.strip()
            ISPIN.SET('2')
            LDAUU.SET(ldauu)
            LDAU.SET('.TRUE.')
            LDAUTYPE.SET('2')
            LDAUL.SET(ldaul)
            LDAUJ.SET(ldauj)
            LASPH.SET('.TRUE.')
            LMAXMIX.SET(lmaxmix)
            return True
        else:
            showinfo('提示','未检测到半满df轨道元素')
            return False
    Reset_tags()#先恢复默认值
    ###########################任何情况都要做的判断设置
    if int(float(POSCAR[1])*float(POSCAR[4].split()[2])) > int(VDW_THRESHOLD):
        IVDW.SET('11')
    if TOTAL_ATOMS >= int(CELL_SIZE_THRESHOLD):
        LREAL.SET('.TRUE.')
    else:
        LREAL.SET('.FALSE.')
    ###########################分情况设置INCAR参数
    if job == 'easy_relax':
        IBRION.SET('2')
        ISTART.SET('0')
        ISPIN.SET('1')
        ISYM.SET('2')
        ICHARG.SET('2')
        INIWAV.SET('1')
        GGA.SET('PS')
        ISIF.SET('3')
        NCORE.SET('4')
        ENCUT.SET('{}'.format(MAX_ENMAX*1.3))
        ISMEAR.SET('-5')
        POTIM.SET('0.5')
        NELMDL.SET('-5')
        EDIFF.SET('1.00E-5')
        NSW.SET('60')
        EDIFFG.SET('-0.01')
        PREC.SET('Accurate')
        ALGO.SET('FAST')
        LWAVE.SET('.FALSE.')
        LCHARG.SET('.TRUE.')
    if job == 'hard_relax':
        if(Check_half_df_element()):#如果输入的值有问题（为空），则返回False
            IBRION.SET('1')
            ISTART.SET('0')
            ISYM.SET('2')
            ICHARG.SET('2')
            INIWAV.SET('1')
            GGA.SET('PS')
            ISIF.SET('3')
            NCORE.SET('4')
            ENCUT.SET('{}'.format(MAX_ENMAX*1.3))
            ISMEAR.SET('-5')
            POTIM.SET('0.2')
            NELMDL.SET('-5')
            EDIFF.SET('1.00E-5')
            NSW.SET('100')
            EDIFFG.SET('-0.001')
            PREC.SET('Accurate')
            ALGO.SET('Normal')
            ADDGRID.SET('.TRUE.')
            LWAVE.SET('.FALSE.')
            LCHARG.SET('.FALSE.')
            return True
        else:
            return False
    if job == 'encut_converge_test':
        IBRION.SET('-1')
        ISTART.SET('0')
        ISPIN.SET('1')
        ISYM.SET('2')
        ICHARG.SET('2')
        INIWAV.SET('1')
        GGA.SET('PS')
        NCORE.SET('4')
        ENCUT.SET('{}'.format(MAX_ENMAX))
        ISMEAR.SET('-5')
        NELMDL.SET('-5')
        EDIFF.SET('1.00E-5')
        PREC.SET('Accurate')
        ALGO.SET('FAST')
        LWAVE.SET('.FALSE.')
        LCHARG.SET('.TRUE.')
    if job == 'kpoints_converge_test':
        IBRION.SET('-1')
        ISTART.SET('0')
        ISPIN.SET('1')
        ISYM.SET('2')
        ICHARG.SET('2')
        INIWAV.SET('1')
        GGA.SET('PS')
        NCORE.SET('4')
        ENCUT.SET('{}'.format(MAX_ENMAX*1.3))
        ISMEAR.SET('-5')
        NELMDL.SET('-5')
        EDIFF.SET('1.00E-5')
        PREC.SET('Accurate')
        ALGO.SET('FAST')
        LWAVE.SET('.FALSE.')
        LCHARG.SET('.TRUE.')
    if job == 'sigma_converge_test':
        IBRION.SET('-1')
        ISTART.SET('0')
        ISPIN.SET('1')
        ISYM.SET('2')
        ICHARG.SET('2')
        INIWAV.SET('1')
        GGA.SET('PS')
        NCORE.SET('4')
        ENCUT.SET('{}'.format(MAX_ENMAX*1.3))
        ISMEAR.SET('0')
        SIGMA.SET('0.01')
        NELMDL.SET('-5')
        EDIFF.SET('1.00E-5')
        PREC.SET('Accurate')
        ALGO.SET('FAST')
        LWAVE.SET('.FALSE.')
        LCHARG.SET('.TRUE.')
    if job == 'main_converge_test':
        IBRION.SET('-1')
        ISTART.SET('0')
        ISPIN.SET('1')
        ISYM.SET('2')
        ICHARG.SET('2')
        INIWAV.SET('1')
        GGA.SET('PS')
        NCORE.SET('4')
        ENCUT.SET('{}'.format(MAX_ENMAX))
        ISMEAR.SET('-5')
        NELMDL.SET('-5')
        EDIFF.SET('1.00E-5')
        PREC.SET('Accurate')
        ALGO.SET('FAST')
        LWAVE.SET('.FALSE.')
        LCHARG.SET('.TRUE.')
    if job == 'self_consistent_filed':
        if(Check_half_df_element()):#如果输入的值有问题（为空），则返回False
            IBRION.SET('-1')
            ISTART.SET('0')
            ISYM.SET('-1')
            ICHARG.SET('2')
            INIWAV.SET('1')
            GGA.SET('PS')
            NCORE.SET('4')
            ENCUT.SET('{}'.format(MAX_ENMAX * 1.3))
            ISMEAR.SET('-5')
            NELMDL.SET('-5')
            EDIFF.SET('1.00E-5')
            PREC.SET('Accurate')
            ALGO.SET('Normal')
            ADDGRID.SET('.TRUE.')
            LWAVE.SET('.TRUE.')
            LCHARG.SET('.TRUE.')
            return True
        else:
            return False
    if job == 'density_of_states':
        if(Check_half_df_element()):#如果输入的值有问题（为空），则返回False
            IBRION.SET('-1')
            ISTART.SET('0')
            ISYM.SET('2')
            if tk.messagebox.askquestion('提示','是否预备CHGCAR？'):
                ICHARG.SET('1')
            else:
                ICHARG.SET('2')
            INIWAV.SET('1')
            GGA.SET('PS')
            NCORE.SET('4')
            NEDOS.SET('3001')
            ENCUT.SET('{}'.format(MAX_ENMAX * 1.3))
            ISMEAR.SET('-5')
            NELMDL.SET('-5')
            EDIFF.SET('1.00E-5')
            PREC.SET('Accurate')
            ALGO.SET('Normal')
            ADDGRID.SET('.TRUE.')
            LORBIT.SET('10')
            LWAVE.SET('.FALSE.')
            LCHARG.SET('.TRUE.')
            return True
        else:
            return False
    if job == 'u_test':
        global GAP
        GAP = askfloat('目标gap(eV)', prompt='gap = ', initialvalue = None)
        if GAP:
            IBRION.SET('-1')
            ISTART.SET('0')
            ISYM.SET('-1')
            if tk.messagebox.askquestion('提示','是否预备CHGCAR？'):
                ICHARG.SET('1')
            else:
                ICHARG.SET('2')
            INIWAV.SET('1')
            GGA.SET('PS')
            NCORE.SET('4')
            NEDOS.SET('3001')
            ENCUT.SET('{}'.format(MAX_ENMAX * 1.3))
            ISMEAR.SET('-5')
            NELMDL.SET('-5')
            EDIFF.SET('1.00E-5')
            PREC.SET('Accurate')
            ALGO.SET('Fast')
            ADDGRID.SET('.TRUE.')
            LWAVE.SET('.TRUE.')
            LCHARG.SET('.TRUE.')
            if (U_test_set()):
                return True
            else:
                return False
        else:
            return False
    return True

def Reset_tags():
    for tag in Tags:#重置除ENCUT之外的所有TAG
        if tag != ENCUT:
            tag.RESET()
        else:
            tag.value = MAX_ENMAX
            tag.active = False
            tag.ready_active = False

def WINDOW():
    def Set_Nodes():
        global NODES
        Nodes = askinteger('请输入', '节点数：', initialvalue = NODES)
        if Nodes:
            NODES = Nodes
    def Set_Cores():
        global CORES
        Cores = askinteger('请输入', '核数：', initialvalue = CORES)
        if Cores:
            CORES = Cores
    global window
    window = tk.Tk()
    size = '{}x{}+{}+{}'.format(int(WIDTH), int(HEIGHT) - 25, 0, int((window.winfo_screenheight()-int(HEIGHT))/2))
    window.geometry(size)
    window.title('vasp_helper')
    menubar = tk.Menu(window)
    power_menu = tk.Menu(menubar, tearoff = False)
    menubar.add_cascade(label='算力', menu = power_menu)
    power_menu.add_command(label = '节点数', command = Set_Nodes)
    power_menu.add_command(label = '核数', command = Set_Cores)
    #power_menu.add_separator()为菜单设置隔板
    window.config(menu=menubar)
    return True

def INI():
    def Nodes(parameter):
        global NODES
        NODES = parameter[1]
    def Cores(parameter):
        global CORES
        CORES = parameter[1]
    def VDW_Threshold(parameter):
        global VDW_THRESHOLD
        VDW_THRESHOLD = parameter[1]
    def Cell_size_Threshold(parameter):
        global CELL_SIZE_THRESHOLD
        CELL_SIZE_THRESHOLD = parameter[1]
    def Height(parameter):
        global HEIGHT
        HEIGHT = parameter[1]
    def Width(parameter):
        global WIDTH
        WIDTH = parameter[1]
    def Customize_Height(parameter):
        global CUSTOMIZE_HEIGHT
        CUSTOMIZE_HEIGHT = parameter[1]
    def Customize_Width(parameter):
        global CUSTOMIZE_WIDTH
        CUSTOMIZE_WIDTH = parameter[1]
    def Desktop_path(parameter):
        global DESKTOP_PATH
        DESKTOP_PATH = parameter[1]
    def Ini_POSCAR_path(parameter):
        global INI_POSCAR_PATH
        INI_POSCAR_PATH = parameter[1]
    def PAW_path(parameter):
        global PAW_PATH
        PAW_PATH = parameter[1]
    def Complex_relax_ready_active_tags(parameter):
        global COMPLEX_RELAX_READY_ACTIVE_TAGS
        for tag in parameter:
            COMPLEX_RELAX_READY_ACTIVE_TAGS.extend([tag])
        del COMPLEX_RELAX_READY_ACTIVE_TAGS[0]
    def default(parameter):
        return False
    parameter = {
                'NODES':Nodes,
                'CORES':Cores,
                'VDW_THRESHOLD':VDW_Threshold,
                'CELL_SIZE_THRESHOLD':Cell_size_Threshold,
                'HEIGHT':Height,
                'WIDTH':Width,
                'CUSTOMIZE_HEIGHT':Customize_Height,
                'CUSTOMIZE_WIDTH':Customize_Width,
                'DESKTOP_PATH':Desktop_path,
                'INI_POSCAR_PATH':Ini_POSCAR_path,
                'PAW_PATH':PAW_path,
                'COMPLEX_RELAX_READY_ACTIVE_TAGS':Complex_relax_ready_active_tags}
    with open('config', 'r') as file:
        config = [line.strip() for line in file]
        for item in config:
            item = item.split()
            if item:
                parameter.get(item[0], default)(item)

def Pre_read_POSCAR(POSCAR_button, main_frame_window):
    def Check_POSCAR():
        global POSCAR_is_ready#需要修改状态
        POSCAR_is_ready = False#先默认错误
        if len(POSCAR) < 6:#防止未选择有效地址
            showinfo('提示', '预置POSCAR格式有误')
            return False
        else:
            result = True
            target_elements = POSCAR[5].strip().split()
            for target_element in target_elements:
                target_flag = False
                for element in Elements:
                    if element.name == target_element:
                        target_flag = True
                        Target_Elements.append(element)
                result = result * target_flag
                if target_flag == False:
                    showinfo('提示', 'can not find element {}!'.format(target_element))
            POSCAR_is_ready = result
    def Tag():#新增元素信息Label控件
        global Old_Target_Elements
        for target_element in Target_Elements:
            Old_Target_Elements.extend([target_element])
            target_element.frame = tk.Frame(main_frame_window)
            target_element.frame.pack(side = 'left', padx = 20)
            target_element.name_label = tk.Label(target_element.frame, text = '{}'.format(target_element.name), fg = 'white', bg = 'green', font = ('Arial',10), width = 3)
            target_element.name_label.pack(pady = 10)
            target_element.electrons_label = tk.Label(target_element.frame, text = '{}'.format(target_element.electrons), fg = 'white', bg = 'green', font = ('Arial',10))
            target_element.electrons_label.pack()
            if 'd' in target_element.electrons and 'd10' not in target_element.electrons:
                target_element.name_label.config(bg = 'purple')
                target_element.electrons_label.config(bg = 'purple')
            if 'f' in target_element.electrons and 'f14' not in target_element.electrons:
                target_element.name_label.config(bg = 'red')
                target_element.electrons_label.config(bg = 'red')
    def Count_atoms():
        global TOTAL_ATOMS
        TOTAL_ATOMS = 0
        ATOMS = POSCAR[6].strip().split()
        for atom in ATOMS:
            TOTAL_ATOMS = TOTAL_ATOMS + int(atom)
    def Get_ENMAX():
        global MAX_ENMAX
        ENMAX = []#存放所有元素的ENMAX
        for element in Target_Elements:
            path = '{}\{}\POTCAR'.format(PAW_PATH, element.name)
            with open(path, 'r') as file:
                for line in file.readlines():
                    if 'ENMAX' in line:
                        #正则表达式找到=和；之间的值并加入列表
                        enmax = r'=(.*?);'
                        element.enmax = int(float(re.findall(enmax, line.replace(' ',''))[0]))
                        ENMAX.extend([element.enmax])
        MAX_ENMAX = max(ENMAX)
        ENCUT.value = MAX_ENMAX
    def Get_unitcell_constant():
        global A_constant
        global B_constant
        global C_constant
        A_constant = ((float(POSCAR[2].strip().split()[0])**2 + float(POSCAR[2].strip().split()[1])**2 + float(POSCAR[2].strip().split()[2])**2)**0.5)*float(POSCAR[1])
        B_constant = ((float(POSCAR[3].strip().split()[0])**2 + float(POSCAR[3].strip().split()[1])**2 + float(POSCAR[3].strip().split()[2])**2)**0.5)*float(POSCAR[1])
        C_constant = ((float(POSCAR[4].strip().split()[0])**2 + float(POSCAR[4].strip().split()[1])**2 + float(POSCAR[4].strip().split()[2])**2)**0.5)*float(POSCAR[1])
    if len(sys.argv) == 2:
        global POSCAR#POSCAR可能被多个函数读
        global POSCAR_path#生成POSCAR时需要原文件路径
        POSCAR_path = sys.argv[1]
        print(POSCAR_path)
        with open(POSCAR_path, 'r', encoding = 'utf-8') as file:
            POSCAR = [line.strip() for line in file]
        Check_POSCAR()
        if POSCAR_is_ready:#检查无误后找到目标元素的POTCAR并提取出ENMAX值
            Count_atoms()
            Get_ENMAX()
            Get_unitcell_constant()
            POSCAR_button.config(bg = 'green')
            Tag()
            return True
        else:#检查有误
            return False
        pass
    else:
        pass
    
if __name__ == "__main__":
    main()