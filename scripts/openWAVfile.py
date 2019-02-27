
'''Note:
        This is using a module that is able to read 24-bit .wav files because for some reason scipy wavfile modules
        can't do that... https://gist.github.com/josephernest/3f22c5ed5dabf1815f16efa8fa53d476  wavfile.py '''

from wavfile import read
import numpy as np
import matplotlib.pyplot as plt


def open_wav(file_name, make_plot=False):

    # TODO add option for other file types -  maybe change the name from open_wav?
    # TODO trim the vector to make all the length uniform
    # TODO normalize the vector so all the values are between 0 and 1
    # TODO add option to play the sound
    # TODO Check to make the inputs are the right variable types


    # use read to return the sample rate and data from the .wav file
    samp_rate, data, bits = read(file_name,normalized=True)

    # create a time vector that corresponds to the real time of each data point
    endtime = ((1 / samp_rate) * data.shape[0])
    time = np.linspace(0, endtime, num=data.shape[0])

    if make_plot:
        # plot the file to just to prove we did it!
        plot = plt.plot(time, data, '.')
        plt.show(plot)

    return samp_rate, time, data


