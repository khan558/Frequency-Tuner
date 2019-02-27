import numpy as np
import matplotlib.pyplot as plt

# Create a Cosine (f=2) as a vector of length 1000 (1 second total)
x = np.linspace(0,1,num=1000)
y = np.cos(2*np.pi*2*x)

# run the cos through an fft and get the corresponding freqs to plot
h = np.fft.fft(y)
mag_h = np.abs(h)
freq = np.fft.fftfreq(y.size,d=0.001)

# time_domain = plt.plot(x,y, '.')
freq_domain = plt.plot(freq,mag_h,'.')

# plt.show(time_domain)
plt.show(freq_domain)

