import streamlit as st
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter

st.set_page_config(layout="wide")

# Function to perform analysis and create graphs for given level data
def analyze_and_plot_level_data(level_data):
    try:
        # Preparing data for analysis
        ai_types = [entry['AI Type'] for entry in level_data if 'AI Type' in entry]
        ai_graph_ids = [entry['Graph ID'] for entry in level_data if 'Graph ID' in entry]
        ai_graphs_names = [entry['Graph Name'] for entry in level_data if 'Graph Name' in entry]
        ai_model_ids = [entry['Model ID'] for entry in level_data if 'Model ID' in entry]
        ai_model_names = [entry['Model Name'].replace('AITYPE_', '') for entry in level_data if 'Model Name' in entry]
        soldier_positions = [(entry['Position X'], entry['Position Y'], entry['Position Z']) for entry in level_data if all(k in entry for k in ('Position X', 'Position Y', 'Position Z'))]
        graph_positions = [(entry['Graph Position']['X'], entry['Graph Position']['Y'], entry['Graph Position']['Z']) for entry in level_data if 'Graph Position' in entry]
        angles = [entry['Angle'] for entry in level_data if 'Angle' in entry]
        
        # Additional data
        positions = [(entry['Position X'], entry['Position Y'], entry['Position Z']) for entry in level_data if all(k in entry for k in ('Position X', 'Position Y', 'Position Z'))]
        model_ids = [entry['Model ID'] for entry in level_data if 'Model ID' in entry]
        model_names = [entry['Model Name'] for entry in level_data if 'Model Name' in entry]
        graph_names = [entry['Graph Name'] for entry in level_data if 'Graph Name' in entry]

        model_names = [name.replace('AITYPE_', '') for name in model_names]
        # Total number of AI in level
        total_ai = len(ai_types)

        # Total number of unique AI types
        unique_ai_types = len(set(ai_types))

        # Total number of graphs
        total_graphs = len(set(ai_graph_ids))

        # Number of AI on each graph
        ai_graph_counts = Counter(ai_graph_ids)
        ai_on_each_graph = {f"Graph ID {graph_id}": count for graph_id, count in ai_graph_counts.items()}

        # Names of AI on each graph
        ai_graph_names = {graph_id: [] for graph_id in set(ai_graph_ids)}
        for entry in level_data:
            if 'Graph ID' in entry and 'AI Type' in entry:
                ai_graph_names[entry['Graph ID']].append(entry['AI Type'])
        names_of_ai_on_each_graph = {f"Graph ID {graph_id}": ', '.join(names) for graph_id, names in ai_graph_names.items()}

        # Writing the data as JSON and outputting it in Streamlit
        data = {
            "Total number of AI in level": total_ai,
            "Total number of unique AI types": unique_ai_types,
            "Total number of graphs": total_graphs,
            "Number of AI on each graph": ai_on_each_graph,
            "Names of AI on each graph": names_of_ai_on_each_graph
        }
        st.json(data)
        

        # Plotting the distribution of soldiers across the different graphs
    
        # Creating a two column layout for the plots
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Distribution of Soldiers')
            fig, ax = plt.subplots()
            sns.countplot(ai_model_names, ax=ax)
            st.pyplot(fig)
            
        # Creating a 3D scatter plot of the positions
            st.subheader("3D Scatter Plot of Positions")
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            for pos, name in zip(positions, model_names):
                x, y, z = pos
                ax.scatter(x, y, z)
                ax.text(x, y, z, name, size=10, zorder=1, color='k') 
            ax.set_xlabel('Position X')
            ax.set_ylabel('Position Y')
            ax.set_zlabel('Position Z')
            st.pyplot(fig)

        with col2:
            # Analyzing the distribution of different AI types among the soldiers
            st.subheader('Distribution of Graph Types')
            fig, ax = plt.subplots()
            sns.countplot(ai_graphs_names, ax=ax)
            #sns.histplot(ai_graphs_names, bins=30, kde=False, ax=ax)
            st.pyplot(fig)

            # Histogram of the angles to see if there's a common orientation for the soldiers
            st.subheader("Histogram of Soldiers' Angles")
            fig, ax = plt.subplots()
            sns.histplot(angles, bins=30, kde=False, ax=ax)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Main method to handle file upload and call analysis functions
def main():
    # Title of the app
    st.title("Project IGI A.I information.")

    # UI for user to enter level number
    level_number = st.number_input("Enter level number (1-14)", min_value=1, max_value=14, step=1)
    
    # When the user enters a level number, read the corresponding file and perform analysis
    if level_number is not None:
        try:
            # Construct the file path
            file_path = f"ai_level_info/level{level_number}.json"
            # Read the JSON file
            with open(file_path, 'r') as f:
                level_data = json.load(f)
            # Perform analysis and plot graphs
            analyze_and_plot_level_data(level_data)
        except FileNotFoundError:
            st.error("The specified level file does not exist.")
        except json.JSONDecodeError:
            st.error("The level file is not a valid JSON file.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Run the main method
if __name__ == "__main__":
    main()
