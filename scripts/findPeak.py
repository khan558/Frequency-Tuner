import numpy as np
import matplotlib.pyplot as plt


def find_peak(vec):
    biggest = 0
    biggest_index = 0
    for x in range(0,vec.size):
        if (vec[x]>biggest):
            biggest=vec[x]
            biggest_index=x
    print(biggest)
    print(biggest_index)


# Create a Cosine (f=2) as a vector of length 1000 (1 second total)
x = np.linspace(0,1,num=1000)
y = np.cos(2*np.pi*2*x)

# run the cos through an fft and get the corresponding freqs to plot
h = np.fft.fft(y)
mag_h = np.abs(h)
freq = np.fft.fftfreq(y.size,d=0.001)

find_peak(mag_h)
