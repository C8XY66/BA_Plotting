import pandas as pd
import matplotlib.pyplot as plt


# Load the Excel file with raw data
df = pd.read_excel('src/raw_data_box_plot.xlsx')

# Define the colors for each model
model_colors = {'GIN_wNF': 'green', 'GIN_woNF': 'blue', 'DGCNN_wNF': 'red', 'DGCNN_woNF': 'orange',
                'MLP_wNF': 'purple', 'MLP_woNF': 'deeppink'}

# Create a new figure and a set of subplots
fig, axs = plt.subplots(2, 3, figsize=(18, 12), gridspec_kw={'wspace':0.2, 'hspace':0.2})  # Create a grid of 2 rows and 3 columns
fig.delaxes(axs[1, 2])  # delete the sixth subplot

# Define the datasets
datasets = ['MUTAG', 'PROTEINS', 'NCI1', 'IMDB-BINARY', 'IMDB-MULTI']

# Set the titles for the subplots
for ax, title in zip(axs.flat, datasets + ['']):
    ax.set_title(title, fontsize=20)
    ax.tick_params(axis='y', labelsize=14)
    ax.set_ylim(0.25, 1.05)


models = list(model_colors.keys())

for dataset, ax in zip(datasets, axs.flat):
    boxplot_data = []
    model_colors_array = []  # This will be used to assign colors

    for model in models:
        model_dataset_data = df[(df['Model'] == model) & (df['Dataset'] == dataset)]['test_acc_fold']
        boxplot_data.append(model_dataset_data)
        model_colors_array.append(model_colors[model])  # Save the color corresponding to the model

    # Plot the boxplot
    box_plot = ax.boxplot(boxplot_data, vert=True, widths=0.5, patch_artist=True, notch=False)

    # Customizing colors
    for patch, color in zip(box_plot['boxes'], model_colors_array):
        patch.set_facecolor('white')  # Set box interior to white
        patch.set_edgecolor(color)  # Set box outline to the color of the model

    for box in box_plot['boxes']:
        box.set_linewidth(3)  # Change this to your preferred linewidth

    # Change the color of median, whiskers and caps to match the model color
    for median, color in zip(box_plot['medians'], model_colors_array):
        median.set_color('black')  # Make the median line black
        median.set_linewidth(2)  # Change this to your preferred linewidth

    for whisker, cap, color in zip(box_plot['whiskers'], box_plot['caps'], model_colors_array*2):
        whisker.set_color('black')  # Set whiskers to the color of the model
        cap.set_color('black')  # Set caps to the color of the model
        whisker.set_linewidth(2)  # Change this to your preferred linewidth
        cap.set_linewidth(2)  # Change this to your preferred linewidth

    ax.set_xticks([])
    ax.set_xlabel("")

# Create a legend with model colors
legend_elements = [plt.Line2D([0], [0], color=color, lw=4, label=model) for model, color in model_colors.items()]
plt.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.15),
           ncol=len(legend_elements), fontsize=16)

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
#plt.tight_layout()
plt.savefig('box_plot.png', bbox_inches='tight', dpi=300, pad_inches=0.5)

plt.show()
