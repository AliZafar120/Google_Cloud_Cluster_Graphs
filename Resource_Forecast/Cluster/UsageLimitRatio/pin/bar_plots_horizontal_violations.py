from matplotlib import pyplot as plt
import numpy as np
# Read CSV into pandas
barWidth = 0.25
width=barWidth
name = ["u_25","u_50","u_75","u_100","u_collective","u_all","u_cumul"]
violations_mse = [0.218,0.605,0.56,0.559,0.82,0.876,0.677]
#savings_mse=[1434.15,858.54,653.84,116.51,411.31,401.02,382.05]
#mse=[]
#savings_pin=[1223.09,630.99,333.37,10.85,180.03,192.21,45.53]
violations_pin = [0.090,0.34,0.161,0.066,0.058,0.11,0.000]

ind = np.arange(len(name))
# Figure Size
fig, ax = plt.subplots(figsize=(8, 8))

# Horizontal Bar Plot
ax.barh(ind, violations_mse, barWidth, color='red', label='MSE')
ax.barh(ind + barWidth, violations_pin, barWidth, color='green', label='PIN')

ax.set_title('Violations',
             loc='center', )
ax.set(yticks=ind + width, yticklabels=name, ylim=[2*width - 1, len(name)])
ax.legend()


plt.savefig('./output_images/cluster_usagelimitratio_violations.jpg')
plt.show()