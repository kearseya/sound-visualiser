import moderngl_window as mglw
import sounddevice as sd
import soundfile as sf
import numpy as np

filename = "skank.mp3" #input("File: ")

class App(mglw.WindowConfig):
	window_size = 600, 400
	resources_dir = "visualiser"
	data, fs = sf.read(filename)
	print(len(data))
	print(fs)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.quad = mglw.geometry.quad_fs()
		self.prog = self.load_program(vertex_shader="/mnt/c/Users/Alex/Downloaded Apps/music-visualiser/visualiser-app/mv/shaders/vertex_shader.glsl",
										fragment_shader="/mnt/c/Users/Alex/Downloaded Apps/music-visualiser/visualiser-app/mv/shaders/heart_spin.glsl")
		#self.set_uniform("time", 0)
		self.set_uniform("resolution", self.window_size)
		#self.set_uniform("music", 0)
		sd.play(self.data, self.fs)

	def set_uniform(self, u_name, u_value):
		try:
			self.prog[u_name] = u_value
		except KeyError:
			print(f"uniform: {u_name} - not used in shader")

	def render(self, time, frame_time):
		self.ctx.clear()
		self.set_uniform("time", time)
		print("time: ",time)
		# self.set_uniform("resolution", self.window_size)
		# iResolution;           // viewport resolution (in pixels)
		# iTime;                 // shader playback time (in seconds)
		# iTimeDelta;            // render time (in seconds)
		# iFrameRate;            // shader frame rate
		# iFrame;                // shader playback frame
		# iChannelTime[4];       // channel playback time (in seconds)
		# iChannelResolution[4]; // channel resolution (in pixels)
		# iMouse;                // mouse pixel coords. xy: current (if MLB down), zw: click
		# iChannel0..3;          // input channel. XX = 2D/Cube
		# iDate;                 // (year, month, day, time in seconds)
		# iSampleRate;           // sound sample rate (i.e., 44100)
		self.set_uniform("music", np.mean(self.data[int(time*self.fs)]))
		# print(np.mean(self.data[int(time*self.fs)]))
		self.quad.render(self.prog)

if __name__ == "__main__":
	filename = input("File: ")
	print(filename)
	if filename == "":
		filename = "skank.mp3"
	mglw.run_window_config(App)
