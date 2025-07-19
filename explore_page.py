import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i]>=cutoff:
            categorical_map[categories.index[i]]=categories.index[i]
        else:
            categorical_map[categories.index[i]]='others'
    return categorical_map


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Something else' in x or 'Associate degree' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache #wont run the dataset again and again
def load_data():
    import pandas as pd
    import matplotlib.pyplot as plt
    data=pd.read_csv(r"C:\Users\sriva\OneDrive\Desktop\Projects\survey_results_public.csv")
    data=data[['EdLevel','Country','Employment','YearsCodePro','ConvertedCompYearly']]
    data=data.rename({"ConvertedCompYearly":"Salary"},axis=1)
    data=data[data['Salary'].notnull()]
    data= data.dropna()
    data = data[data["Employment"]=="Employed, full-time"]
    data=data.drop('Employment',axis=1)
    
    country_map=shorten_categories(data.Country.value_counts(), 400)
    data['Country']=data['Country'].map(country_map)
    data=data[data['Salary']<=250000]
    data=data[data['Salary']<=10000]
    data=data[data['Country']!='others']
    
    data['YearsCodePro'] =pd.to_numeric(data['YearsCodePro'],errors='coerce')
    data ["EdLevel"] = data["EdLevel"].apply(clean_education)

    return data

data=load_data()

def show_explore_page():
    st.title("🚀Explore Software Developer Salaries")
    st.write("""
    ### Stack overflow developer survey 2024✨
    """)

    data1 = data["Country"].value_counts()
    percentages = data1 / data1.sum() * 100
    labels = [f"{country} - {percent:.1f}%" for country, percent in zip(data1.index, percentages)]

    fig1, ax1 = plt.subplots()
    wedges, _ = ax1.pie(
        data1, 
        labels=None,              # No labels on the chart
        shadow=True, 
        startangle=90
    )
    ax1.axis("equal")

    # Custom legend with percentages
    ax1.legend(wedges, labels, title="Countries", bbox_to_anchor=(1, 0.5), loc="center left")

    st.write("#### Number of Data from different countries")
    st.pyplot(fig1)


    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data1= data.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data1)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data1= data.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data1)