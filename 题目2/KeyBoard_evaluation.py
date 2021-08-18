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

'''
 第二步：将汉语字符串转换成拼音列表和拼音字符串

'''
# 获取字符串的拼音
pinyin_list = pypinyin.lazy_pinyin(pdf_content, style=pypinyin.NORMAL, errors='ignore')
pdf_pinyin = ''
for i in pinyin_list:
    pdf_pinyin += ''.join(i)


'''
 第三步：统计26个字母建的使用频率

'''
result_count={}
for n in pdf_pinyin:
    result_count[n]=pdf_pinyin.count(n)

py_count = {}
x = []
for i in range(26):
    py_ch = chr(i+97)
    if py_ch in result_count:
        py_count[py_ch] = result_count[py_ch]
        x.append(result_count[py_ch])
    else:
        py_count[py_ch] = 0
        x.append(0)

'''
 第四步：计算评价指标

'''
# 1、26字母按键次数的标准差std
std = np.std(x, ddof = 1)

# 2、逐字输入的平均按键次数
p = len(pdf_pinyin) / len(pinyin_list)

# 3、逐字输入的平均手指移动次数
# 键盘上26字母键的手指移动次数
y = {'q':1,'w':1,'e':1,'r':1,'t':1,'y':1,'u':1,'i':1,'o':1,'p':1,
     'a':0,'s':0,'d':0,'f':0,'g':1,'h':1,'j':0,'k':0,'l':0,
     'z':1,'x':1,'c':1,'v':1,'b':1,'n':1,'m':1}
m_sum = 0
for i in range(26):
    py_ch = chr(i+97)
    m_sum += py_count[py_ch] * y[py_ch]
m = m_sum / len(pinyin_list)

print('1、26字母按键次数的标准差为：%f' %(std))
print('2、逐字输入的平均按键次数为：%f（次/字）' %(p))
print('3、逐字输入的平均手指移动次数为：%f（次/字）' %(m))
