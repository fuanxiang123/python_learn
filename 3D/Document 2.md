这段Python代码使用Pygame库和OpenGL来在窗口中绘制并旋转一个3D立方体。以下是代码各部分的详细解释：

导入模块：

pygame 是一个用于开发游戏和其他多媒体应用的Python库，它提供了创建窗口、处理事件（如按键和鼠标动作）以及渲染图形的功能。
from pygame.locals import * 导入了Pygame的一些常量，例如OPENGL和DOUBLEBUF，这些都是用来配置显示模式的。
from OpenGL.GL import * 和 from OpenGL.GLU import * 导入了OpenGL的函数，用于执行3D渲染操作，其中GLU提供了辅助函数，比如视锥体设置（gluPerspective）。
定义draw_cube函数：

定义了一个立方体的顶点列表vertices，包含八个顶点，每个顶点由(x, y, z)坐标组成，这些坐标定义了立方体各个面的位置。
定义了边列表edges，它列出了每对相连顶点的索引，用于构造立方体的线框模型。
函数内部使用OpenGL的glBegin和glEnd函数包裹绘制过程，指定这次绘图将以GL_LINES模式进行，即画线模式。
遍历所有边，在for edge in edges:循环中，再次遍历当前边的两个顶点，并通过glVertex3fv函数将它们的坐标传递给OpenGL，从而逐条绘制出构成立方体框架的线段。
定义main函数：

初始化Pygame。
设置窗口大小为800x600像素，并启用OpenGL双缓冲（防止画面撕裂）。
调用gluPerspective设置透视投影，包括视角角度、宽高比、近裁剪面和远裁剪面的距离。
使用glTranslatef将观察位置后移-5个单位，这样可以更好地从正面看到立方体。
进入主循环：
检查是否接收到退出事件（如用户点击关闭窗口），若是，则退出程序。
每次循环时，都通过glRotatef函数沿(3, 1, 1)轴向旋转立方体1度，实现立方体的动态旋转效果。
清除颜色和深度缓存，准备新的帧渲染。
调用draw_cube函数绘制立方体线框。
使用pygame.display.flip()更新屏幕显示新绘制的内容。
延迟等待10毫秒，以控制帧率。
入口点：

如果当前脚本被直接执行（即作为主程序运行），则执行main函数开始整个程序流程。
总之，这个程序会在一个Pygame窗口内利用OpenGL绘制一个不断旋转的3D线框立方体。


