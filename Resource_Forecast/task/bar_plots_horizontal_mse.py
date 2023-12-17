from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
# Read CSV into pandas


name = ["Borg","RC","Itrans_pin","Itran_mse","Lstm_pin","Lstm_mse","ARNN_mse","Bi-At_pin","Bi-At_mse"]
price = [8.225083843597357e-05, 0,  5.7955826521124155e-05, 4.216134249313686e-05, 7.603495358752868e-05, 4.651052787581278e-05, 0.00015079436640748724, 7.411611066926277e-05, 5.868184450497127e-05]


fig, ax = plt.subplots(figsize=(8, 8))

# Horizontal Bar Plot

color = ['red',"green", "blue", "yellow", "purple", "orange", "pink", "brown", "black", "lightgray"]

ax.barh(name, price, color=color,)


#ax.get_xaxis().set_major_formatter(mtick.FormatStrFormatter('%.000000e'))
#ax.get_xaxis().set_major_formatter( mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
#ax.ticklabel_format(style='sci',scilimits=(-6,-4),axis='both')
# Remove axes splines [outer boundary]
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)

# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')


# Add padding between axes and labels
ax.xaxis.set_tick_params(pad=5)
ax.yaxis.set_tick_params(pad=10)



# Add x, y gridlines
ax.grid( axis='both', color='grey',
        linestyle='-.', linewidth=0.5,
        alpha=0.2)

# Show top values
ax.invert_yaxis()

# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width() , i.get_y() + 0.5,
             str(i.get_width()),
             fontsize=10, fontweight='bold',
             color='grey')

# Add Plot Title
ax.set_title('MSE',
             loc='center', )

# Add Text watermark
# fig.text(0.9, 0.15, 'Jeeteshgavande30', fontsize=12,
#          color='grey', ha='right', va='bottom',
#          alpha=0.7)

# Show Plot

plt.savefig('./output_images/task_mse.jpg')
plt.show()