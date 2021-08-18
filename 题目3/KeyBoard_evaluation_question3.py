from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams

import pypinyin

import numpy as np

'''
 第一步：获取PDF文档内容，并存入字符串

'''
fp = open("共产党宣言.pdf", 'rb')    
# 创建解释器
pdf_parser = PDFParser(fp)
# PDF文档对象
pdf_doc = PDFDocument()
# 连接解释器和文档对象
pdf_parser.set_document(pdf_doc)
pdf_doc.set_parser(pdf_parser)
# 初始化文档
pdf_doc.initialize()
# 创建PDF资源管理器
pdf_resource = PDFResourceManager()
# 创建一个PDF参数分析器
pdf_laparam = LAParams()
# 创建聚合器
pdf_device = PDFPageAggregator(pdf_resource, laparams=pdf_laparam)
# 创建PDF页面解析器
pdf_interpreter = PDFPageInterpreter(pdf_resource, pdf_device)
 
# 循环遍历列表，每次处理并获取一页的内容
pdf_content = ''
for page in pdf_doc.get_pages():
    #使用页面解释器来读取
    pdf_interpreter.process_page(page)
    #使用聚合器获得内容
    layout = pdf_device.get_result()
    for out in layout:       
        if hasattr(out, 'get_text'):
            pdf_content += out.get_text()


# 获取字符串的拼音
pinyin_list = pypinyin.lazy_pinyin(pdf_content, style=pypinyin.NORMAL, errors='ignore')

lshengmu1 = ['b','p','m','f','d','t','n','l','g','k','h','j','q','x','r','z','c','s','y','w']
lshengmu2 = ['zh','ch','sh']

lyunmu1 = ['a','e','i','o','u','v']
lyunmu2 = ['ai','ei','ui','ao','ou','iu','ie','ve','er','an','en','in','un','vn','ang','eng','ing','ong']

shengmu1 = {'b':0,'p':0,'m':0,'f':0,'d':0,'t':0,'n':0,'l':0,'g':0,'k':0,'h':0,'j':0,'q':0,'x':0,'r':0,'z':0,'c':0,'s':0,'y':0,'w':0}
shengmu2 = {'zh':0,'ch':0,'sh':0}

yunmu1 = {'a':0,'e':0,'i':0,'o':0,'u':0,'v':0}
yunmu2 = {'ai':0,'ei':0,'ui':0,'ao':0,'ou':0,'iu':0,'ie':0,'ve':0,'er':0,'an':0,'en':0,'in':0,'un':0,'vn':0,'ang':0,'eng':0,'ing':0,'ong':0}

for i in range(len(pinyin_list)):
    p_str = pinyin_list[i]
    p2 = ''
    if p_str[:2] in shengmu2:
        shengmu2[p_str[:2]] += 1
        p2 = p_str[2:]
    elif p_str[:1] in shengmu1:
        shengmu1[p_str[:1]] += 1
        p2 = p_str[1:]
    else:
        p2 = p_str
    
    if p2 in yunmu1:
        yunmu1[p2] += 1
    elif p2 in yunmu2:
        yunmu2[p2] += 1
    else:
        p3 = p2[1:]
        if p2[:1] in yunmu1:
            yunmu1[p2[:1]] += 1
        if p3 in yunmu1:
            yunmu1[p3] += 1
        elif p3 in yunmu2:
            yunmu2[p3] += 1
        
lns1 = []
lns2 = []
lny1 = []
lny2 = []
for i in range(len(lshengmu1)):
    lns1.append(shengmu1[lshengmu1[i]])
for i in range(len(lshengmu2)):
    lns2.append(shengmu2[lshengmu2[i]])
for i in range(len(lyunmu1)):
    lny1.append(yunmu1[lyunmu1[i]])
for i in range(len(lyunmu2)):
    lny2.append(yunmu2[lyunmu2[i]])


# 替换规则
sy1 = {'an':'p','ong':'k','en':'s','ai':'c','ie':'n','eng':'r','ao':'f','ang':'q','ou':'w',
       'ui':'m','ing':'t','ei':'b','in':'h','un':'h','iu':'x','er':'x','ve':'x','vn':'x'}
sy2 = {'zh':'v','sh':'o','ch':'a'}

# 进行输入法替换
pdf_pinyin = ''
for i in range(len(pinyin_list)):
    p_str = pinyin_list[i]
    p2 = ''
    if p_str[:2] in shengmu2:
        pinyin_list[i] = sy2[p_str[:2]] + p_str[2:]
        p2 = p_str[2:]
    elif p_str[:1] in shengmu1:
        p2 = p_str[1:]
    else:
        p2 = p_str
    
    if p2 in yunmu2:
        pinyin_list[i] = pinyin_list[i][:1] + sy1[p2]
    elif p2 not in yunmu1:
        p3 = p2[1:]
        if p3 in yunmu2:
            pinyin_list[i] = pinyin_list[i][:2] + sy1[p3]
    pdf_pinyin += pinyin_list[i]
            
result_count={}
for n in pdf_pinyin:
    result_count[n]=pdf_pinyin.count(n)

rc = sorted(result_count.items(), key = lambda x:x[1], reverse = True)

x = []
for i in range(26):
    x.append(rc[i][1])
    
# 1、26字母按键次数的标准差std
std = np.std(x, ddof = 1)

# 2、逐字输入的平均按键次数
p = len(pdf_pinyin) / len(pinyin_list)

# 3、逐字输入的平均手指移动次数
# 键盘上26字母键的手指移动次数
y = {'q':1,'w':1,'f':1,'r':1,'t':1,'y':1,'k':1,'a':1,'l':1,'s':1,
     'j':0,'p':0,'d':0,'e':0,'g':1,'h':1,'i':0,'u':0,'o':0,
     'z':1,'x':1,'c':1,'v':1,'b':1,'n':1,'m':1}

m_sum = 0
for i in range(26):
    py_ch = chr(i+97)
    m_sum += result_count[py_ch] * y[py_ch]
m = m_sum / len(pinyin_list)

print('1、26字母按键次数的标准差为：%f' %(std))
print('2、逐字输入的平均按键次数为：%f（次/字）' %(p))
print('3、逐字输入的平均手指移动次数为：%f（次/字）' %(m))
