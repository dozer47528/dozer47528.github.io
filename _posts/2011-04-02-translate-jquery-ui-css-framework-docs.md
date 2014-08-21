---
title: jQuery UI CSS Framework 文档 翻译
author: Dozer
layout: post
permalink: /2011/04/translate-jquery-ui-css-framework-docs/
categories:
  - 编程技术
tags:
  - CSS
  - html
  - jQuery
  - jQuery UI
---

### <span id="jQuery_UI_CSS_Framework">jQuery UI CSS Framework</span>

jQuery UI 包含一个强大的 CSS 框架来帮助我们设计 jQuery 小部件，这个框架包含了许多普通用户经常会用到的 class，并且还可以利用 jQuery UI 主题编辑器来方便地修改主题。当你在使用 jQuery UI CSS 框架来构建你网站的 UI 时，你必须要遵守一些约定，这样才能更好地使用 jQuery UI  CSS 框架。

&nbsp;

### <span id="Framework_Classes">Framework Classes</span>

一下的几个 class 分别在 ui.core.css 和 ui.theme.css 文件中，你可以直接下载一个完整的 css 文件，也可以几个部分。

这些类保证了构建 UI 的一致性和快速性，而它们的外观主要取决于你的主题样式。

<!--more-->

### <span id="Layout_Helpers">Layout Helpers</span>

.ui-helper-hidden: 给元素设置 display: none 属性。

.ui-helper-hidden-accessible: 是元素不可访问 (利用绝对定位使其在页面外部)

.ui-helper-reset: 基础重置 class， 重置： padding, margins, text-decoration, list-style, 等属性

.ui-helper-clearfix: 给元素设置 clear: both 属性

.ui-helper-zfix: 当元素需要覆盖在最上面是设置此属性

&nbsp;

### <span id="Widget_Containers">Widget Containers</span>

.ui-widget: 这个 class 会被用在外部容器上，它会给内部的部件统一字体、字号。这个主要是为了解决浏览器继承问题的

.ui-widget-header: 这个 class 会被用在标题容器上，同样，它也主要是给容器内部的成员统一一些属性的

.ui-widget-content: 这个 class 会被用在内容容器上，作用同上

&nbsp;

### <span id="Interaction_States">Interaction States</span>

.ui-state-default: 这个 class 会被用在类似于 button 的小部件上，用来显示这个部件在默认状态下的样式

.ui-state-hover: 用法同上，用来设置鼠标悬停时的样式

.ui-state-focus: 用法同上，用来设置得到焦点时的样式

.ui-state-active: 用法同上，用来设置鼠标按下时的样式

&nbsp;

### <span id="Interaction_Cues">Interaction Cues</span>

.ui-state-highlight: 设置高亮样式

.ui-state-error: 设置错误样式

.ui-state-error-text: 设置文本错误样式

.ui-state-disabled: 设置禁用样式

.ui-priority-primary: 设置高优先级样式

.ui-priority-secondary: 设置低优先级样式

&nbsp;

### <span id="Icons">Icons</span>

**States and images**

.ui-icon: 图标元素的基础 class，它会设置一个 16px 大小的正方形，隐藏内部文字，把背景设置成当前状态的背景（上一个部分分别有四种状态，这四种状态下的图标背景是不同的）

&nbsp;

**Icon types**

当你给 a 设置了 &#8220;.ui-icon&#8221; class 后，你可以再设置一个描述性的 class，格式如下： .ui-icon-{icon type}-{icon sub description}-{direction}.

例如一个单一的三角形图标： .ui-icon-triangle-1-e

&nbsp;

你可以在 <a href="http://jqueryui.com/themeroller/" target="_blank"><strong>jQuery UI 主题编辑器</strong></a> 页面看到这些图标，查看一下它们的 class 就知道怎么用了

&nbsp;

### <span id="Misc_Visuals">Misc Visuals</span>

**Corner Radius helpers**

.ui-corner-tl: 给元素的左上角设置圆角

.ui-corner-tr: 给元素的右上角设置圆角

.ui-corner-bl: 给元素的左下角设置圆角

.ui-corner-br: 给元素的右下角设置圆角

.ui-corner-top: 给元素的上部设置圆角

.ui-corner-bottom: 给元素的下部设置圆角

.ui-corner-right: 给元素的右边设置圆角

.ui-corner-left: 给元素的左边设置圆角

.ui-corner-all: 设置所有圆角

&nbsp;

**Overlay & Shadow**

.ui-widget-overlay: 设置一个小部件全屏的遮罩层

.ui-widget-shadow: 设置一个小部件的阴影
