from manimlib.imports import *
import numpy as np


class Bullet(Triangle):
	CONFIG = {
		"fill_opacity": 1,
		"stroke_width": 0,
		"length": DEFAULT_ARROW_TIP_LENGTH,
		"start_angle": PI,
		"aspect": 1.5,
		"angle": 0,
	}

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		digest_config(self, kwargs)
		self.set_height(self.length, stretch=True)
		self.data["points"][4] += np.array([self.length, 0, 0])
		self.scale(0.35)

	def get_angle(self):
		return self.angle

	def get_vector(self):
		return self.point_from_proportion(0.5) - self.get_start()

	def rotate(self, angle, axis=OUT, **kwargs):
		super().rptate(angle, axis, *kwargs)
		self.angle = angle
		return self


class special_circle(Dot):
	CONFIG = {
		"radius": 0.05,

	}

	def __init__(self):
		self.start_angle = 0
		self.dim = 0

	def get_angle(self):
		return np.arctan(self.get_center()[1] / (self.get_center()[0] + 0.00000001))


class TestDanmaku(Scene):
	def construct(self):
		trace1 = VGroup()
		trace2 = VGroup()
		trace3 = VGroup()
		color_map = [PINK, BLUE, TEAL, GREEN, YELLOW, GOLD, ORANGE, RED]
		PI = 3.1415926

		def updater_one_trace(start_angle):
			def update(obj, dt):
				obj.add(special_circle().rotate(self.time ** 2 * PI + start_angle))
				obj.set_color_by_gradient(*color_map)
				for k in obj:
					k.shift(np.array([
						np.cos(k.get_angle()),
						np.sin(k.get_angle()),
						0
					]) * 4 * dt)
					if abs(get_norm(k.get_center())) > 7:
						obj.remove(k)

			return update

		trace1.add_updater(updater_one_trace(0))
		trace2.add_updater(updater_one_trace(2 * PI / 3))
		trace3.add_updater(updater_one_trace(4 * PI / 3))
		self.add(trace1, trace2, trace3)
		self.wait(10)


class running_curve(Scene):
	CONFIG = {"x_axis_label": '$x$',
	          "y_axis_label": '$y$',
	          "z_axis_label": '$z$',
	          "camera_config": {"background_color": BLACK}, }

	def construct(self):
		scale_times = 2
		dot_a = Dot(np.array([-1, -1, 0]) * scale_times).scale(2)
		dot_b = Dot(np.array([-1, 1, 0]) * scale_times).scale(2)
		dot_c = Dot(np.array([1, 1, 0]) * scale_times).scale(2)
		dot_d = Dot(np.array([1, -1, 0]) * scale_times).scale(2)
		l_ab = Line()
		l_bc = Line()
		l_cd = Line()
		l_da = Line()

		def put_line_on(a, b):
			def update(line):
				line.put_start_and_end_on(a.get_center(), b.get_center())

			return update

		def updater_dot(target):
			def anim(obj, dt):
				obj.shift(
					(target.get_center() - obj.get_center()) * dt
				)

			return anim

		dot_a.add_updater(updater_dot(dot_b))
		dot_b.add_updater(updater_dot(dot_c))
		dot_c.add_updater(updater_dot(dot_d))
		dot_d.add_updater(updater_dot(dot_a))
		l_ab.add_updater(put_line_on(dot_a, dot_b))
		l_bc.add_updater(put_line_on(dot_b, dot_c))
		l_cd.add_updater(put_line_on(dot_c, dot_d))
		l_da.add_updater(put_line_on(dot_d, dot_a))
		trace = VGroup()
		trace.add_updater(lambda a, dt: a.add(
			l_ab.copy().clear_updaters().set_stroke(width=0.6),
			l_bc.copy().clear_updaters().set_stroke(width=0.6),
			l_cd.copy().clear_updaters().set_stroke(width=0.6),
			l_da.copy().clear_updaters().set_stroke(width=0.6),
		))
		self.add(dot_a, dot_b, dot_c, dot_d, l_ab, l_bc, l_cd, l_da, trace)
		self.wait(5)


class polygon_fetching(Scene):
	CONFIG = {"x_axis_label": '$x$',
	          "y_axis_label": '$y$',
	          "z_axis_label": '$z$',##坐标轴参数，这里没有用到坐标轴
	          "camera_config": {"background_color": BLACK},  ##相机背景颜色
	          "scale_times": 3,  #显示放大倍率
	          "shape_number": 12, #多边形的边数
	          "direction": "clockwise",#追赶方向，clockwises顺时针追赶，counterclockwise逆时针追赶
	          "fetch_step": 2,  #点追赶的步距，1代表相邻点追赶，2代表追赶下第二个点
	          "link_step" : 2,  #线连接的步距，1代表相邻点连接，2代表隔一点连接
	          "run_speed": 1,#追赶速度
	          "start_angle": 0,#多边形摆放起始角度
	          "dot_scale": 2, #点的大小
	          "run_time": 5, #运行时间
	          }

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def construct(self):
		PI = 3.1415926
		each_angle = 2 * PI / self.shape_number
		dot = []
		line = []
		dot_link_index = []
		for i in range(self.shape_number):
			dot.append(Dot(np.array(
				[self.scale_times * np.cos(each_angle * i + self.start_angle*PI/180), self.scale_times * np.sin(each_angle * i + self.start_angle*PI/180), 0])).scale(self.dot_scale))
			line.append(Line())

		def put_line_on(a, b):
			def update(line):
				line.put_start_and_end_on(a.get_center(), b.get_center())

			return update

		def updater_dot(target):
			def anim(obj, dt):
				if self.direction == "clockwise":
					obj.shift(
						(target.get_center() - obj.get_center()) * self.run_speed * dt)
				elif self.direction == "counterclockwise":
					obj.shift(
						(obj.get_center() - target.get_center()) * self.run_speed * dt)

			return anim

		def updater_trace(target):
			def anim(obj, dt):
				for i in range(len(target)):
					obj.add(target[i].copy().clear_updaters().set_stroke(width=0.6))

			return anim
		sort_list = []
		for j in range(3):
			for j in range(self.shape_number):
				sort_list.append(int(j))
		for i in range(self.shape_number):
			dot[sort_list[i]].add_updater(updater_dot(dot[(int(sort_list[i + self.fetch_step]))]))
			line[int(sort_list[i])].add_updater(put_line_on(dot[int(sort_list[i])], dot[int(sort_list[i + self.link_step])]))

		trace = VGroup()
		trace.add_updater(updater_trace(line))
		self.add(*dot, *line, trace)
		self.wait(self.run_time)
