import scipy.signal as signal
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
from openWAVfile import open_wav
import hashlib


'''This is basically a carbon copy of Dejavu by worldveil on GitHub - 
    https://github.com/worldveil/dejavu/blob/master/dejavu/fingerprint.py
    There are a few minor changes but only to simplify'''

# number of points used for the FFTs of the spectrogram - keep it a power of 2 to get fastest runtime
DEFAULT_WINDOW_SIZE = 4096

# overlap for the FFTs that make up the spectrogram
DEFAULT_OVERLAP = 0.5

# larger filter usually means it will detect less peaks
PEAK_NEIGHBORHOOD_SIZE = 5

# how many index values to look ahead of a given frequency
DEFAULT_FAN_VALUE = 5

# default values for how far apart (in seconds) the peaks can be when generating the fingerprints
MIN_HASH_TIME_DELTA = 1
MAX_HASH_TIME_DELTA = 3

# Number of bits to throw away from the front of the SHA1 hash in the
# fingerprint calculation. The more you throw away, the less storage, but
# potentially higher collisions and misclassifications when identifying songs.
FINGERPRINT_REDUCTION = 20

def fingerprint(time, data, fs, window_size=DEFAULT_WINDOW_SIZE, overlap=DEFAULT_OVERLAP, show_plots=False,
                fan_val = DEFAULT_FAN_VALUE):


    # start by creating a spectrogram of the input data
    spec_freqs, spec_time, spec_data = signal.spectrogram(data, fs, nperseg=window_size, window='hanning', noverlap=int(window_size*overlap), mode='magnitude')

    # convert spec_data to dB scale
    spec_data = 10*np.log10(spec_data)

    # TODO make the get_peaks into a seperate function
    # create a filter to run over the image then make it bigger by iterating (print it out to see what it looks like)
    neighborhood = ndimage.generate_binary_structure(2,1).astype(int)
    neighborhood = ndimage.iterate_structure(neighborhood,PEAK_NEIGHBORHOOD_SIZE)

    # for visualization purposes - don't actually need to calculate
    max_filter_data = ndimage.maximum_filter(spec_data,footprint=neighborhood)

    # create binary array of the local maximums
    local_max = spec_data == ndimage.maximum_filter(spec_data,footprint=neighborhood)#  == ndimage.maximum_filter(spec_data, size=(3,3))

    # have this here in case we want to change how we find the peaks - I know its redundant!
    detected_peaks = local_max.astype(int)

    # create a list of the indices of time and frequency of the peaks
    freq_ind, time_ind = np.where(detected_peaks == 1)
    peak_locs = np.zeros((2, freq_ind.size))
    peak_locs[0, :] = spec_freqs[freq_ind]
    peak_locs[1, :] = spec_time[time_ind]



    # TODO create a hash value for each time chunk. Will be based on the frequency and time indexes

    # initialize the array of hashes
    hashes = np.zeros((1,2))

    # loop over all the frequency locations
    for i in range(0, np.size(peak_locs,axis=1)):
        # loop over all the local values
        for j in range(1, fan_val):

            # make sure we don't exceed matrix dimensions
            if (i+j) < np.size(peak_locs,axis=1) and (i-j) > 0:

                # look the frequencies of two peaks
                freq1 = peak_locs[0,i]
                freq2 = peak_locs[0,i+j]

                # look at the times of the same two peaks
                time1 = peak_locs[1,i]
                time2 = peak_locs[1,i+j]
                delta_t = time2 - time1

                # make sure that the peaks aren't too far apart in time
                if delta_t > MIN_HASH_TIME_DELTA and delta_t < MAX_HASH_TIME_DELTA:
                    # TODO generate the hash from the frequencies and time delta
                    # create string of the frequencies and the time offset
                    string = str(freq1)+str(freq2)+str(delta_t)

                    # create a hash object and give it the string form of the frequencies and time offset
                    h = hashlib.sha1(string.encode('utf-8'))#"%s|%s|%s" % (str(freq1), str(freq2), str(delta_t)))

                    # generate the hash
                    hashes = np.append(hashes, (h.hexdigest()[0:FINGERPRINT_REDUCTION], time1))

    print(str(np.max(spec_data)))
    # print(detected_peaks)

    # show a plot if we wanna show off
    if show_plots:

        # plot the original spectrogram
        plt.figure(1)
        plt.pcolormesh(spec_time, spec_freqs, spec_data)
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')

        # plot the output from the maximum filter
        plt.figure(2)
        plt.pcolormesh(spec_time, spec_freqs, max_filter_data)
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')

        # Plot the matrix of detected peaks
        plt.figure(3)
        plt.pcolormesh(spec_time, spec_freqs, detected_peaks)
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')

        # a scatter plot of the peak locations to compare to the detected peaks - points should be same
        plt.figure(4)
        plt.scatter(peak_locs[1, :], peak_locs[0,:],marker='.')
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')

        plt.show()

    return hashes



# test our functions
samp_rate, time, data = open_wav('Microwave.wav')

hashbrown = fingerprint(time, data[:,0], samp_rate, show_plots=True)

print('done')
