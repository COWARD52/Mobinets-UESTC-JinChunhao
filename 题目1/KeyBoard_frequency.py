from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams

import pypinyin

from pyheatmap.heatmap import HeatMap

import matplotlib.pyplot as plt

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
 第二步：将汉语字符串转换成拼音字符串

'''
# 获取字符串的拼音
pdf_pinyin = ''
for i in pypinyin.pinyin(pdf_content, style=pypinyin.NORMAL):
    pdf_pinyin += ''.join(i)


'''
 第三步：统计26个字母键的使用频率

'''
result_count={}
for n in pdf_pinyin:
    result_count[n]=pdf_pinyin.count(n)

py_count = {}
for i in range(26):
    py_ch = chr(i+97)
    if py_ch in result_count:
        py_count[py_ch] = result_count[py_ch]
    else:
        py_count[py_ch] = 0

'''
 第四步：绘制读入的这篇文章的26字母键使用热力图

'''
heat_data = [] 
# 键盘上26字母的分布
line_1 = ['q','w','e','r','t','y','u','i','o','p']
line_2 = ['a','s','d','f','g','h','j','k','l']
line_3 = ['z','x','c','v','b','n','m']
dx = 55
# 生成热力图数据
for i in range(len(line_1)):
    py_ch = line_1[i]
    if py_ch in py_count:
        heat_data.append([123+i*dx, 138, py_count[py_ch]])
    else:
        heat_data.append([123+i*dx, 138, 0])
    
for i in range(len(line_2)):
    py_ch = line_2[i]
    if py_ch in py_count:
        heat_data.append([136+i*dx, 191, py_count[py_ch]])
    else:
        heat_data.append([136+i*dx, 191, 0])
        
for i in range(len(line_3)):
    py_ch = line_3[i]
    if py_ch in py_count:
        heat_data.append([163+i*dx, 244, py_count[py_ch]])
    else:
        heat_data.append([163+i*dx, 244, 0])

# 实例化热力图对象，传入坐标点和键盘1背景图
hm = HeatMap(heat_data,base='keyboard.png') 
# 绘制26字母键使用热力图，并且保存
hm.heatmap(save_as="keyboard_heatmap.png", r = 30)

'''
 补充：绘制26字母键使用次数直方图

'''
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
py = []
py_num = []
for i in range(26):
    py_ch = chr(i+97)
    py.append(py_ch)
    py_num.append(py_count[py_ch])

plt.bar(py, py_num)
plt.title('给定文章全拼输入时26字母键使用次数直方图')

plt.show()
