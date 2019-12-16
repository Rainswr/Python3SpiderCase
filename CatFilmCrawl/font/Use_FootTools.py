# -*- encoding: utf-8 -*-
"""
@author/github: Shirmay1
@software: PyCharm
@file: Use_FootTools.py
@time: 2019/12/10 22:55
@function:FootTools的使用
@url: https://vfile.meituan.net/colorstone/20e8627b1aa9e979c6a8e975a83575bf2272.woff
"""

from fontTools.ttLib import TTFont

# 加载字体文件：
font = TTFont('local_fonts.woff')
# 保存为xml文件：
font.saveXML('local_fonts.xml')
# 获取各节点名称，返回为列表
print(font.keys())
# 获取getGlyphOrder节点的name值, 返回列表
print(font.getGlyphOrder())
print(font.getGlyphNames())
# 获取cmap节点code与name值映射, 返回为字典
print(font.getBestCmap())
# 获取glyf节点TTGlyph字体xy坐标信息
print(font['glyf']['uniE1A0'].coordinates)
# 获取glyf节点TTGlyph字体xMin,yMin,xMax,yMax坐标信息
print(font['glyf']['uniE1A0'].xMin, font['glyf']['uniE1A0'].yMin,
      font['glyf']['uniE1A0'].xMax, font['glyf']['uniE1A0'].yMax)
# 获取glyf节点TTGlyph字体on信息
print(font['glyf']['uniE1A0'].flags)
# 获取GlyphOrder节点GlyphID的id信息, 返回int型
print(font.getGlyphID('uniE1A0'))


