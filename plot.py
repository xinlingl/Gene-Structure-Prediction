import matplotlib.pyplot as plt
import numpy as np

true_label = {
    'N': 96981,
    'E': 6370,
    'I': 16603,
    'p': 7,
    'P': 7,
    'Z': 7,
    'z': 7,
    's': 9,
    'S': 9
}
output = {
    '0': 435,
    '1': 39,
    '2': 1037,
    '3': 114885,
    '4': 1401,
    '5': 707,
    '6': 669,
    '7': 417,
    '8': 410,
}

men_means = (0.169, 0.191, 0.3, 0.284, 0.717)
women_means = (0.186, 0.386, 0.783, 0.753, 0.790)

ind = np.arange(len(men_means))  # the x locations for the groups
width = 0.40  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, men_means, width,
                color='SkyBlue', label='Random')
rects2 = ax.bar(ind + width/2, women_means, width,
                color='IndianRed', label='Count-based')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Accuracy')
# ax.set_title('Number of Iterations')
ax.set_xticks(ind)
ax.set_xticklabels(('100', '200', '300', '400', '500'))
plt.ylim(0, 1)
ax.legend(loc=2)

def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'center', 'left': 'center'}
    offset = {'center': 0.5, 'right': 0.5, 'left': 0.5}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')


autolabel(rects1, "left")
autolabel(rects2, "right")

plt.show()