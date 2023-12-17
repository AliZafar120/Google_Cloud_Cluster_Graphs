from matplotlib import pyplot as plt

# Read CSV into pandas



name = ["Borg","N_Sigma","RC","Max"]
price = [0,.98,0.22,0]



# Figure Size
fig, ax = plt.subplots(figsize=(8, 8))

# Horizontal Bar Plot

color = ['red',"green", "blue", "yellow", "purple", "orange", "pink", "brown", "black", "lightgray"]
ax.barh(name, price, color=color)

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
             str(round((i.get_width()), 2)),
             fontsize=10, fontweight='bold',
             color='grey')

# Add Plot Title
ax.set_title('Savings',
             loc='center', )

# Add Text watermark
# fig.text(0.9, 0.15, 'Jeeteshgavande30', fontsize=12,
#          color='grey', ha='right', va='bottom',
#          alpha=0.7)

# Show Plot

plt.savefig('./output_images/cluster_long_savings.jpg')
plt.show()