# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objs as go
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure Gemini AI
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def create_visualization(df, chart_type, x_axis, y_axis):
#     """
#     Create a visualization with maximum flexibility for any column combination
#     """
#     try:
#         # Determine column types
#         x_is_numeric = pd.api.types.is_numeric_dtype(df[x_axis])
#         y_is_numeric = pd.api.types.is_numeric_dtype(df[y_axis])
        
#         # Color palette
#         color_palettes = {
#             'Bar Chart': ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'],
#             'Pie Chart': px.colors.qualitative.Pastel,
#             'Scatter Plot': ['#00CC96', '#636EFA', '#EF553B'],
#             'Box Plot': ['#AB63FA', '#636EFA', '#00CC96'],
#             'Line Chart': ['#FFA15A', '#636EFA', '#EF553B']
#         }
        
#         # Flexible Visualization Logic
#         if chart_type == "Bar Chart":
#             # Handle both categorical and numeric scenarios
#             if not y_is_numeric:
#                 # Count for categorical Y
#                 fig = px.bar(df[y_axis].value_counts().reset_index(), 
#                              x='index', y=y_axis, 
#                              title=f"Count of {y_axis}",
#                              labels={'index': y_axis, y_axis: 'Count'},
#                              color_discrete_sequence=color_palettes['Bar Chart'])
#             else:
#                 # Aggregation for numeric Y
#                 fig = px.bar(df, x=x_axis, y=y_axis, 
#                              title=f"{y_axis} by {x_axis}",
#                              color_discrete_sequence=color_palettes['Bar Chart'])
        
#         elif chart_type == "Pie Chart":
#             # Use value counts or proportions
#             value_counts = df[y_axis].value_counts()
#             fig = px.pie(value_counts, 
#                          names=value_counts.index, 
#                          values=value_counts.values, 
#                          title=f"Distribution of {y_axis}",
#                          color_discrete_sequence=color_palettes['Pie Chart'])
        
#         elif chart_type == "Scatter Plot":
#             # Scatter plot with fallback for non-numeric
#             if x_is_numeric and y_is_numeric:
#                 fig = px.scatter(df, x=x_axis, y=y_axis, 
#                                  title=f"{y_axis} vs {x_axis}",
#                                  color_discrete_sequence=color_palettes['Scatter Plot'])
#             else:
#                 # Categorical scatter plot with jitter
#                 fig = px.strip(df, x=x_axis, y=y_axis, 
#                                title=f"{y_axis} by {x_axis}",
#                                color_discrete_sequence=color_palettes['Scatter Plot'])
        
#         elif chart_type == "Box Plot":
#             # Box plot works with categorical X and numeric Y
#             fig = px.box(df, x=x_axis, y=y_axis, 
#                          title=f"{y_axis} Distribution by {x_axis}",
#                          color_discrete_sequence=color_palettes['Box Plot'])
        
#         elif chart_type == "Line Chart":
#             # Line chart with more flexibility
#             if y_is_numeric:
#                 fig = px.line(df, x=x_axis, y=y_axis, 
#                               title=f"{y_axis} Trend by {x_axis}",
#                               color_discrete_sequence=color_palettes['Line Chart'])
#             else:
#                 # For non-numeric, use count line plot
#                 grouped = df.groupby(x_axis)[y_axis].count().reset_index()
#                 fig = px.line(grouped, x=x_axis, y=y_axis, 
#                               title=f"Count of {y_axis} by {x_axis}",
#                               color_discrete_sequence=color_palettes['Line Chart'])
        
#         # Universal chart styling
#         fig.update_layout(
#             plot_bgcolor='rgba(0,0,0,0)',
#             paper_bgcolor='rgba(0,0,0,0)',
#             font=dict(family="Arial, sans-serif", size=12),
#             title_font_size=16,
#             title_x=0.5,
#             hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
#         )
        
#         return fig
    
#     except Exception as e:
#         st.error(f"Visualization Error: {str(e)}")
#         return None

# def main():
#     # Set page configuration
#     st.set_page_config(page_title="Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
    
#     # Custom CSS for enhanced styling
#     st.markdown("""
#     <style>
#     /* Custom Background and Typography */
#     body {
#         background-color: #F0F4F8;
#         color: #2C3E50;
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }
    
#     /* Main Title Styling */
#     .main-title {
#         font-size: 48px;
#         font-weight: bold;
#         color: #1A5F7A;
#         text-align: center;
#         margin-bottom: 30px;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
#     }
    
#     /* Sidebar Enhancements */
#     .sidebar .sidebar-content {
#         background-color: #FFFFFF;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         padding: 20px;
#     }
    
#     /* Card-like Sections */
#     .stCard {
#         background-color: #FFFFFF;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         padding: 20px;
#         margin-bottom: 20px;
#     }
    
#     /* Button Styling */
#     .stButton>button {
#         background-color: #1A5F7A;
#         color: white;
#         border: none;
#         border-radius: 6px;
#         transition: all 0.3s ease;
#     }
    
#     .stButton>button:hover {
#         background-color: #137099;
#         transform: scale(1.05);
#     }
#     </style>
#     """, unsafe_allow_html=True)
    
#     # Introduction and Overview
#     st.markdown('<div class="main-title">InsightEase: HR Analytics Dashboard</div>', unsafe_allow_html=True)
    
#     # Informative Introduction
#     st.markdown("""
#     ### 🚀 InsightEase: Your HR Data Insights Companion
    
#     RecruitEase is a powerful, user-friendly HR analytics platform designed to transform raw HR data into meaningful insights. Our dashboard empowers HR professionals and data analysts to:

#     - 📊 **Visualize Complex Data**: Create intuitive charts and graphs
#     - 🔍 **Gain Deep Insights**: Analyze workforce trends and patterns
#     - 🤖 **Smart Analytics**: Get intelligent insights with our integrated AI
    
#     ### How to Use:
#     1. 📤 Upload your CSV file
#     2. 🧐 Explore data overview and metrics
#     3. 📈 Generate various visualizations
#     4. 🤔 Ask Smart Analytics questions about your data
#     """)
    
#     # Sidebar for visualization controls
#     st.sidebar.header("📊 Visualization Settings")
    
#     # File uploader
#     uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    
#     if uploaded_file:
#         # Read the CSV file
#         df = pd.read_csv(uploaded_file)
        
#         # Data Overview
#         st.header("📋 Data Overview")
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Total Records", len(df))
#         col2.metric("Total Columns", len(df.columns))
#         col3.metric("Data Completeness", f"{df.notna().mean().mean()*100:.2f}%")
        
#         # Visualization Section
#         st.header("📈 Data Visualization")
        
#         # Visualization Controls
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             chart_type = st.selectbox("Chart Type", 
#                 ["Bar Chart", "Pie Chart", "Scatter Plot", "Box Plot", "Line Chart"])
        
#         with col2:
#             x_axis = st.selectbox("X-Axis / Category", df.columns)
        
#         with col3:
#             # All columns can now be selected as Y-axis
#             y_axis = st.selectbox("Y-Axis / Value", df.columns)
        
#         # Generate Visualization
#         if st.button("Generate Chart"):
#             fig = create_visualization(df, chart_type, x_axis, y_axis)
#             if fig:
#                 st.plotly_chart(fig, use_container_width=True)
        
#         # Data Preview
#         st.header("🔍 Data Preview")
#         st.dataframe(df.head())
        
#         # Bonus: Column Information
#         st.header("📊 Column Information")
#         column_info = pd.DataFrame({
#             'Column Name': df.columns,
#             'Data Type': df.dtypes,
#             'Non-Null Count': df.notna().sum(),
#             'Unique Values': [df[col].nunique() for col in df.columns]
#         })
#         st.dataframe(column_info)
        
#         # AI Query Section
#         st.header("🤖 Smart Analytics")
#         query = st.text_area("Ask a question about the data:")
        
#         if st.button("Get Insights"):
#             try:
#                 # Prepare prompt
#                 prompt = f"Given the following HR dataset:\n{df.to_string(index=False)}\n\nAnswer the following question:\n{query}"
                
#                 # Call Google Gemini AI
#                 model = genai.GenerativeModel("gemini-1.5-flash")
#                 response = model.generate_content(prompt)
                
#                 # Display response
#                 st.write("### AI Response:")
#                 st.write(response.text)
            
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")

# # Run the Streamlit app
# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def display_column_info(df):
    """
    Create and display column information with robust error handling
    """
    try:
        # Create column information DataFrame with explicit type conversions
        column_info = pd.DataFrame({
            'Column Name': df.columns.tolist(),
            'Data Type': [str(dtype) for dtype in df.dtypes],
            'Non-Null Count': df.notna().sum().astype(int).tolist(),
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        
        # Additional type conversion to ensure compatibility
        column_info = column_info.astype(str)
        
        # Display the information
        st.dataframe(column_info, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error displaying column information: {e}")
        
        # Fallback display method
        st.write("Column Information:")
        for col in df.columns:
            st.write(f"**{col}**:")
            st.write(f"- Data Type: {df[col].dtype}")
            st.write(f"- Non-Null Count: {df[col].notna().sum()}")
            st.write(f"- Unique Values: {df[col].nunique()}")

def create_visualization(df, chart_type, x_axis, y_axis):
    """
    Create a visualization with maximum flexibility for any column combination
    """
    try:
        # Determine column types
        x_is_numeric = pd.api.types.is_numeric_dtype(df[x_axis])
        y_is_numeric = pd.api.types.is_numeric_dtype(df[y_axis])
        
        # Color palette
        color_palettes = {
            'Bar Chart': ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'],
            'Pie Chart': px.colors.qualitative.Pastel,
            'Scatter Plot': ['#00CC96', '#636EFA', '#EF553B'],
            'Box Plot': ['#AB63FA', '#636EFA', '#00CC96'],
            'Line Chart': ['#FFA15A', '#636EFA', '#EF553B']
        }
        
        # Flexible Visualization Logic
        if chart_type == "Bar Chart":
            # Handle both categorical and numeric scenarios
            if not y_is_numeric:
                # Count for categorical Y
                fig = px.bar(df[y_axis].value_counts().reset_index(), 
                             x='index', y=y_axis, 
                             title=f"Count of {y_axis}",
                             labels={'index': y_axis, y_axis: 'Count'},
                             color_discrete_sequence=color_palettes['Bar Chart'])
            else:
                # Aggregation for numeric Y
                fig = px.bar(df, x=x_axis, y=y_axis, 
                             title=f"{y_axis} by {x_axis}",
                             color_discrete_sequence=color_palettes['Bar Chart'])
        
        elif chart_type == "Pie Chart":
            # Use value counts or proportions
            value_counts = df[y_axis].value_counts()
            fig = px.pie(value_counts, 
                         names=value_counts.index, 
                         values=value_counts.values, 
                         title=f"Distribution of {y_axis}",
                         color_discrete_sequence=color_palettes['Pie Chart'])
        
        elif chart_type == "Scatter Plot":
            # Scatter plot with fallback for non-numeric
            if x_is_numeric and y_is_numeric:
                fig = px.scatter(df, x=x_axis, y=y_axis, 
                                 title=f"{y_axis} vs {x_axis}",
                                 color_discrete_sequence=color_palettes['Scatter Plot'])
            else:
                # Categorical scatter plot with jitter
                fig = px.strip(df, x=x_axis, y=y_axis, 
                               title=f"{y_axis} by {x_axis}",
                               color_discrete_sequence=color_palettes['Scatter Plot'])
        
        elif chart_type == "Box Plot":
            # Box plot works with categorical X and numeric Y
            fig = px.box(df, x=x_axis, y=y_axis, 
                         title=f"{y_axis} Distribution by {x_axis}",
                         color_discrete_sequence=color_palettes['Box Plot'])
        
        elif chart_type == "Line Chart":
            # Line chart with more flexibility
            if y_is_numeric:
                fig = px.line(df, x=x_axis, y=y_axis, 
                              title=f"{y_axis} Trend by {x_axis}",
                              color_discrete_sequence=color_palettes['Line Chart'])
            else:
                # For non-numeric, use count line plot
                grouped = df.groupby(x_axis)[y_axis].count().reset_index()
                fig = px.line(grouped, x=x_axis, y=y_axis, 
                              title=f"Count of {y_axis} by {x_axis}",
                              color_discrete_sequence=color_palettes['Line Chart'])
        
        # Universal chart styling
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12),
            title_font_size=16,
            title_x=0.5,
            hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
        )
        
        return fig
    
    except Exception as e:
        st.error(f"Visualization Error: {str(e)}")
        return None

def main():
    # Set page configuration
    st.set_page_config(page_title="Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    /* Custom Background and Typography */
    body {
        background-color: #F0F4F8;
        color: #2C3E50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main Title Styling */
    .main-title {
        font-size: 48px;
        font-weight: bold;
        color: #1A5F7A;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Enhancements */
    .sidebar .sidebar-content {
        background-color: #FFFFFF;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
    }
    
    /* Card-like Sections */
    .stCard {
        background-color: #FFFFFF;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #1A5F7A;
        color: white;
        border: none;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #137099;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Introduction and Overview
    st.markdown('<div class="main-title">InsightEase: HR Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Informative Introduction
    st.markdown("""
    ### 🚀 InsightEase: Your HR Data Insights Companion
    
    RecruitEase is a powerful, user-friendly HR analytics platform designed to transform raw HR data into meaningful insights. Our dashboard empowers HR professionals and data analysts to:

    - 📊 **Visualize Complex Data**: Create intuitive charts and graphs
    - 🔍 **Gain Deep Insights**: Analyze workforce trends and patterns
    - 🤖 **Smart Analytics**: Get intelligent insights with our integrated AI
    
    ### How to Use:
    1. 📤 Upload your CSV file
    2. 🧐 Explore data overview and metrics
    3. 📈 Generate various visualizations
    4. 🤔 Ask Smart Analytics questions about your data
    """)
    
    # Sidebar for visualization controls
    st.sidebar.header("📊 Visualization Settings")
    
    # File uploader
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Data Overview
        st.header("📋 Data Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Total Columns", len(df.columns))
        col3.metric("Data Completeness", f"{df.notna().mean().mean()*100:.2f}%")
        
        # Visualization Section
        st.header("📈 Data Visualization")
        
        # Visualization Controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            chart_type = st.selectbox("Chart Type", 
                ["Bar Chart", "Pie Chart", "Scatter Plot", "Box Plot", "Line Chart"])
        
        with col2:
            x_axis = st.selectbox("X-Axis / Category", df.columns)
        
        with col3:
            # All columns can now be selected as Y-axis
            y_axis = st.selectbox("Y-Axis / Value", df.columns)
        
        # Generate Visualization
        if st.button("Generate Chart"):
            fig = create_visualization(df, chart_type, x_axis, y_axis)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # Data Preview
        st.header("🔍 Data Preview")
        st.dataframe(df.head())
        
        # Column Information - Updated section
        st.header("📊 Column Information")
        display_column_info(df)
        
        # AI Query Section
        st.header("🤖 Smart Analytics")
        query = st.text_area("Ask a question about the data:")
        
        if st.button("Get Insights"):
            try:
                # Prepare prompt
                prompt = f"Given the following HR dataset:\n{df.to_string(index=False)}\n\nAnswer the following question:\n{query}"
                
                # Call Google Gemini AI
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                # Display response
                st.write("### AI Response:")
                st.write(response.text)
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
