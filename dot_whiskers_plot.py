import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines



# Load the Excel file
df = pd.read_excel('src/data_dot_whiskers_plot.xlsx')

# Define the colors for each model
model_colors = {'GIN_wNF': 'green', 'GIN_woNF': 'blue', 'DGCNN_wNF': 'red', 'DGCNN_woNF': 'orange',
                'MLP_wNF': 'purple', 'MLP_woNF': 'deeppink'}

# Define the markers for each source
source_markers = {'Exp. Test': 'o', 'Exp. Val.': 's', 'Errica et al.': 'D', 'Original': '^'}

# Create a new figure and a set of subplots
fig, axs = plt.subplots(2, 3, figsize=(18, 12))  # Create a grid of 2 rows and 3 columns
for ax in axs.flat:
    ax.tick_params(axis='y', labelsize=14)


# Set the titles for the subplots
axs[0, 0].set_title('MUTAG', fontsize=20)
axs[0, 1].set_title('PROTEINS', fontsize=20)
axs[0, 2].set_title('NCI1', fontsize=20)
axs[1, 0].set_title('IMDB-BINARY', fontsize=20)
axs[1, 1].set_title('IMDB-MULTI', fontsize=20)

fig.delaxes(axs[1, 2])


for dataset, ax in zip(['MUTAG', 'PROTEINS', 'NCI1', 'IMDB-BINARY', 'IMDB-MULTI'],
                       [axs[0, 0], axs[0, 1], axs[0, 2], axs[1, 0], axs[1, 1]]):
    # Plot each data point for the dataset
    for i, row in df.iterrows():
        model = row['Model']
        source = row['Source']
        position = row[f'Position']
        test_acc = row[f'Test_acc_{dataset}']
        stddev = row[f'stddv_{dataset}']

        # Check if the current test_acc value is not zero and is not NaN
        if not pd.isna(test_acc) and test_acc != 0:
            # Get the color and marker for this point from the model and source
            color = model_colors[model]
            marker = source_markers[source]

            # Plot the point with error bars
            ax.errorbar(position, test_acc, yerr=stddev, fmt=marker, color=color, ecolor=color, capsize=5,
                        label=f"{model} {source}")

            # Add a scatter plot on top of the error bar plot with the same coordinates
            ax.scatter(position, test_acc, s=70, color=color, marker=marker)  # Increase or decrease 's' for size

    # Remove x-labels and x-ticks
    ax.set_xlabel("")
    ax.set_xticks([])

# Create first legend with model colors
legend1_elements = [mlines.Line2D([0], [0], color='green', lw=4, label='GIN_wNF'),
                    mlines.Line2D([0], [0], color='blue', lw=4, label='GIN_woNF'),
                    mlines.Line2D([0], [0], color='red', lw=4, label='DGCNN_wNF'),
                    mlines.Line2D([0], [0], color='orange', lw=4, label='DGCNN_woNF'),
                    mlines.Line2D([0], [0], color='purple', lw=4, label='MLP_wNF'),
                    mlines.Line2D([0], [0], color='deeppink', lw=4, label='MLP_woNF')]

legend1 = plt.legend(handles=legend1_elements, loc='lower center', bbox_to_anchor=(0.5, -0.15),
                     ncol=len(legend1_elements), fontsize=16)
plt.gca().add_artist(legend1)


# Create second legend with source markers
legend2_elements = [mlines.Line2D([0], [0], marker='o', color='w', label='Exp. Test', markerfacecolor='k', markersize=10),
                    mlines.Line2D([0], [0], marker='s', color='w', label='Exp. Val.', markerfacecolor='k', markersize=10),
                    mlines.Line2D([0], [0], marker='D', color='w', label='Errica et al.', markerfacecolor='k', markersize=10),
                    mlines.Line2D([0], [0], marker='^', color='w', label='Original', markerfacecolor='k', markersize=10)]

plt.legend(handles=legend2_elements, loc='lower center', bbox_to_anchor=(0.5, -0.25),
           ncol=len(legend2_elements), fontsize=16)


plt.savefig('dot_whiskers_plot.png', bbox_inches='tight', dpi=300, pad_inches=0.5)


plt.tight_layout()
plt.show()
