import pandas as pd
import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px 
import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
from plotly.subplots import make_subplots

df = pd.read_csv("/Users/rathikakn/Desktop/Guvi/project3airbnb/airbnbproject.csv")

# --------------------------------------------------Logo & details on top

st.set_page_config(page_title= "Airbnb Analysis",
                   layout= "wide",
                   initial_sidebar_state= "expanded")

        #------------------------------------------------------------------HEADER common to all menu


st.write(" ")
st.write(" ")
st.write(" ")
st.markdown("""
                <style>
                .centered-text {
                    text-align: center;
                    font-style:'Arial', sans-serif;
                    font-weight: bold;
                    font-size: 100px; 
                    pointer-events: none;
                }
                </style>
                <div class="centered-text">
                    Airbnb Analysis
                </div>
                """, unsafe_allow_html=True)    
    

    
opt = st.radio(
    label="",
    options=["Home", "Analysis", "Insights"],
    index=0,
    format_func=lambda x: x.title(),
    horizontal=True,
    key="menu",
)
#------------------------------------HOME
if opt=="Home":

    st.write(" ") 
    st.write(" ")     
    st.markdown("#### :red[*OVERVIEW* ]")
    st.markdown("##### This project aims to analyze Airbnb data & perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends in the Airbnb marketplace.")

    st.markdown("#### :red[*DOMAIN* ] ")
    st.markdown(" ##### Travel Industry, Property Management and Tourism ")
    st.markdown("""
                #### :red[*TECHNOLOGIES USED*]    
        
                ##### Python scripting, Data Preprocessing, Visualization,EDA, Streamlit

                """)
    
#---------------------------------------- DATA EXPLORATION
elif opt=="Analysis":
    st.write(" ")

#------------------------------------------------------------------------------------------------------------ Price Analysis 
    on = st.checkbox("##### Price Analysis")

    if on:
        
        st.write(" ")

        # What factors (e.g., amenities, review scores) influence listing prices the most?
    
        review_scores_prices = df.groupby('Review_scores')['Price'].mean().reset_index()

        # Create a bar chart
        fig = px.bar(
            review_scores_prices,
            x='Review_scores',
            y='Price',
            title='Review Scores and Average Price',
            labels={'Review_scores': 'Review Scores', 'Price': 'Average Price'},
            width=1300,
            height=700,
        )

        # Show the bar chart
        st.plotly_chart(fig)


# How does the average price vary by property type?

        avg_price_by_type = df.groupby("Property_type")["Price"].mean()
        fig = px.line(
            avg_price_by_type.reset_index(),
            x="Property_type",
            y="Price",
            title="Average Price for each Property",width=1300,height=700,
            labels={"Property_type": "Property Type", "Price": "Average Price"},
        )
        fig.update_traces(mode='markers+lines') 
        fig.update_layout(xaxis_title='Property Type', yaxis_title='Average Price')
        st.plotly_chart(fig)



# How does the price vary across different neighborhoods or cities?
         
        avg_price_by_location = df.groupby("Host_neighbourhood")["Price"].mean().reset_index()

        fig = px.strip(avg_price_by_location, x="Host_neighbourhood", y="Price", color="Host_neighbourhood",
                    title="Average Price by City",
                    labels={"Host_neighbourhood": "Host Neighbourhood", "Price": "Average Price"},
                    width=1410, height=700)

        st.plotly_chart(fig)


            
#------------------------------------------------------------------------- Avalaibility Analysis

    on = st.checkbox("##### Avalaibility Analysis")

    if on:
        
        st.write(" " )
 

# What is the overall availability trend of Airbnb listings over time? 

        df = df.drop(columns=['Listing_Id'])
        numeric_df = df.select_dtypes(include=[np.number])
        overall_availability = numeric_df.mean()
        fig = px.pie(names=overall_availability.index, values=overall_availability.values,
                    title='Availability Trend of Airbnb Listings',hole=0.5, width=1300,height=700,)
        st.plotly_chart(fig)

#---------------------------------------------------------------------------------

# How does the availability of listings change based on the cancellation policy?
           
        avg_data_by_cancellation_policy = df.groupby('Cancellation_policy').agg({'Availability_365': 'mean', 'Price': 'mean'}).reset_index()
        fig = px.scatter_3d(avg_data_by_cancellation_policy, x='Cancellation_policy', z='Availability_365', y='Price',
                            title='Average Availability and Price by Cancellation Policy',width=1000,height=700,color="Availability_365",color_continuous_scale="Plotly3",
                            labels={'Cancellation_policy': 'Cancel Pol', 'Availability_365': 'Avg Avail', 'Price': 'Price'})

        st.plotly_chart(fig)

# How does the availability of listings vary by property type?
           
        avg_prop_avail = df.groupby("Property_type")["Availability_365"].mean().reset_index()
        fig = px.line(avg_prop_avail, x="Property_type", y="Availability_365", markers=True,
                    title="Average Availability by Property Type",
                    labels={"Property_type": "Property Type", "Availability_365": "Average Availability (Days)"},
                    width=1300, height=700)

        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig)

# What is the average availability for different room types?

        avg_availability_by_room_type = df.groupby('Room_type')['Availability_365'].mean().reset_index()

        fig = px.pie(avg_availability_by_room_type, values='Availability_365', names='Room_type',
                            title='Average Availability by Room Type', width=1300,height=700,)
        st.plotly_chart(fig)

    
# __________________________________Location Analysis
    on = st.checkbox("##### Location Analysis")

    if on:
            
 # ---------------------------------------------------------------------  diff countries based on avg review score 
    #-----------------------------------------------------diff countries based on their avg book price

            
        avg_review_score_by_country = df.groupby('Country')['Review_scores'].mean().reset_index()
        avg_review_score_by_country = avg_review_score_by_country.sort_values(by='Review_scores')
        avg_price_by_country = df.groupby('Country')['Price'].mean().reset_index()
        avg_price_by_country = avg_price_by_country.sort_values(by='Price', ascending=False)
        # Define colors for the bars
        fig = go.Figure()
        fig.add_trace(go.Bar(x=avg_review_score_by_country['Country'], y=avg_review_score_by_country['Review_scores'],
                            name='Average Review Score', marker_color='lightblue'))
        fig.add_trace(go.Bar(x=avg_price_by_country['Country'], y=avg_price_by_country['Price'],
                            name='Average Booking Price', marker_color='salmon'))
        fig.update_layout(barmode='group', title='Average Review Score and Booking Price by Country',width=1300,height=700,
                        xaxis_tickangle=-45, xaxis_title='Country', yaxis_title='Value')
        st.plotly_chart(fig)

#-------------------------------------------What are the top amenities offered in listings across different neighborhoods?


        amenities = df['Amenities'].str.replace('[{}]', '').str.replace('"', '').str.split(',')
        amenity_counts = {}
        for amns in amenities:
            for amenity in amns:
                if amenity.strip() in amenity_counts:
                    amenity_counts[amenity.strip()] += 1
                else:
                    amenity_counts[amenity.strip()] = 1
        sorted_amenities = sorted(amenity_counts.items(), key=lambda x: x[1], reverse=True)
        top_n = 10
        top_amenities = dict(sorted_amenities[:top_n])

        # Create a horizontal bar chart
        fig = go.Figure(go.Bar(
            x=list(top_amenities.values()),
            y=list(top_amenities.keys()),
            orientation='h',  # Horizontal orientation
            marker=dict(color='royalblue'),  # Custom color
        ))

        # Update layout
        fig.update_layout(
            title='Top Amenities Offered in Listings Across Different Neighborhoods',
            xaxis_title='Count',
            yaxis_title='Amenity',
            width=1000,
            height=700,
        )

        # Show the plot
        st.plotly_chart(fig)


        #----------------------------------------Are there any neighborhoods with a significantly higher average review score than others?

        avg_review_score_by_neighborhood = df.groupby('suburb')['Review_scores'].mean().reset_index()
        top_10_neighborhoods = avg_review_score_by_neighborhood.sort_values(by='Review_scores', ascending=False).head(10)
        top_10_neighborhoods['Rank'] = 'Top 10'
        least_10_neighborhoods = avg_review_score_by_neighborhood.sort_values(by='Review_scores', ascending=True).head(10)
        least_10_neighborhoods['Rank'] = 'Least 10'
        merged_neighborhoods = pd.concat([top_10_neighborhoods, least_10_neighborhoods])
        fig = px.bar(merged_neighborhoods, x='suburb', y='Review_scores', color='Rank',
                    labels={'Review_scores': 'Average Review Score'},
                    title='Top and Least 10 Neighborhoods by Average Review Score',width=1200,height=700,
                    color_discrete_sequence=px.colors.qualitative.Pastel)

        fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Average Review Score')
        st.plotly_chart(fig)

#-----------------------------------------------------Are there any differences in the distribution of property types across neighborhoods?

    
        property_type_distribution = df.groupby(['suburb', 'Property_type']).size().reset_index(name='count')

        fig = px.scatter(property_type_distribution, x='suburb', y='count', color='Property_type',
                        title='Distribution of Property Types Across Neighborhoods',width=1110,height=700,
                        labels={'count': 'Number of Listings', 'suburb': 'Neighborhood'})
        fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Number of Listings')
        st.plotly_chart(fig)

            #________________________________________________here merge merge highest lowest host in one pie and highest lowest property 
        
    

        hosts_by_country = df.groupby('Country')['Host_id'].nunique().reset_index(name='host_count')
        property_types_by_country = df.groupby(['Country', 'Property_type']).size().reset_index(name='property_count')
        country_with_highest_hosts = hosts_by_country.loc[hosts_by_country['host_count'].idxmax()]
        country_with_lowest_hosts = hosts_by_country.loc[hosts_by_country['host_count'].idxmin()]
        country_with_highest_property_types = property_types_by_country.groupby('Country')['Property_type'].nunique().reset_index()
        country_with_highest_property_types = country_with_highest_property_types.loc[country_with_highest_property_types['Property_type'].idxmax()]
        country_with_lowest_property_types = property_types_by_country.groupby('Country')['Property_type'].nunique().reset_index()
        country_with_lowest_property_types = country_with_lowest_property_types.loc[country_with_lowest_property_types['Property_type'].idxmin()]
        fig1 = go.Figure()
        fig1.add_trace(go.Pie(labels=[f"Highest Hosts ({country_with_highest_hosts['Country']})", f"Lowest Hosts ({country_with_lowest_hosts['Country']})"],
                            values=[country_with_highest_hosts['host_count'], country_with_lowest_hosts['host_count']],
                            name="Number of Hosts",
                            hoverinfo='label+percent+name',
                            marker=dict(colors=["#636efa", "#EF553B"])))

        fig1.update_layout(title_text="Highest and Lowest Number of Hosts by Country",width=700,height=400)
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Pie(labels=[f"Highest Property Types ({country_with_highest_property_types['Country']})", f"Lowest Property Types ({country_with_lowest_property_types['Country']})"],
                            values=[country_with_highest_property_types['Property_type'], country_with_lowest_property_types['Property_type']],
                            name="Number of Property Types",
                            hoverinfo='label+percent+name',
                            marker=dict(colors=["#00cc96", "#ab63fa"])))

        fig2.update_layout(title_text="Highest and Lowest Number of Property Types by Country",width=700,height=400)
        #st.subheader("Distribution of Hosts and Property Types by Country")
        st.plotly_chart(fig2, use_container_width=True)
    
    on = st.checkbox("##### Geo visualisation")
    if on:
               
         #------------------------------------------------------------------How does the availability of listings change based on location?

        df_filtered = df[df['Availability_365'] < 365]
        fig = px.scatter_mapbox(df_filtered, lat="Latitude", lon="Longitude", color="Availability_365",
                                hover_name="suburb", hover_data={"suburb": True, "market": True, "Country": True, "Availability_365": True},
                                color_continuous_scale=px.colors.sequential.Viridis,
                                zoom=1,width=1300,height=700)
        fig.update_layout(mapbox_style="open-street-map", title="Listing Availability by Location")
        st.plotly_chart(fig)

    #---------------------------------------- INSIGHTS
elif opt=="Insights":
        st.markdown(
    """
    <style>
        .css-15qegpx {
            display: flex;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
                
        title=st.selectbox("Select one of these",
                                    ["Choose a Title...",
                                     '1.Neighborhoods with the Highest Number of Listings',
                                     '2.Number of Available Listings in the Next 30 Days by City',
                                     '3.Top 10 Countries with the Most Listings',
                                     '4.Top 10 Most Common Amenities Provided in Listings',
                                     '5.Distribution of Average Review Scores for Top Hosts',
                                     '6.Top 10 Most Popular Host Verification Methods'],
                                      index=0)
                
        if title=='1.Neighborhoods with the Highest Number of Listings':

            # Which neighborhoods have the highest number of listings?

                    neighborhood_counts = df['Host_neighbourhood'].value_counts().reset_index()
                    neighborhood_counts.columns = ['Neighborhood', 'Number of Listings']
                    neighborhood_counts = neighborhood_counts.sort_values(by='Number of Listings', ascending=False)

                   
                    fig = px.bar(neighborhood_counts.head(10), x='Neighborhood', y='Number of Listings',
                                labels={'Neighborhood': 'Neighborhood', 'Number of Listings': 'Number of Listings'},
                                title='Neighborhoods with the Highest Number of Listings', width=1300,height=700,color='Number of Listings',color_continuous_scale= "plasma")
                    
                    st.plotly_chart(fig)


        elif title=='2.Number of Available Listings in the Next 30 Days by City':
            availability_30_by_city = df.groupby('market')['Availability_30'].sum().reset_index()
            availability_30_by_city_sorted = availability_30_by_city.sort_values(by='Availability_30', ascending=False)

            fig = px.bar(availability_30_by_city_sorted, x='market', y='Availability_30',color="Availability_30",color_continuous_scale='oryel',
                        title='Number of Available Listings in the Next 30 Days by City', width=1300,height=700,
                        labels={'market': 'City', 'Availability_30': 'Available'})

            fig.update_layout(xaxis_title='City', yaxis_title='Available')
            st.plotly_chart(fig)

            # ------------------------------Which hosts have the highest average review scores?


        elif title=='3.Top 10 Countries with the Most Listings':

            # What are the top 10 countries with the most listings? 

            listings_by_country = df['Country'].value_counts().reset_index()
            listings_by_country.columns = ['Country', 'Number of Listings']
            listings_by_country = listings_by_country.sort_values(by='Number of Listings', ascending=False)
            top_10_countries = listings_by_country.head(10)

            fig = px.bar(top_10_countries, x='Number of Listings', y='Country', orientation='h',
                        labels={'Number of Listings': 'Number of Listings', 'Country': 'Country'},
                        title='Top 10 Countries with the Most Listings', width=1300,height=700,color='Number of Listings',color_continuous_scale='Purpor')

            st.plotly_chart(fig)


        elif title=='4.Top 10 Most Common Amenities Provided in Listings':

        #----------------------------------------What are the top 10 most common amenities provided in listings?

            all_amenities = ', '.join(df['Amenities'])
            amenities_list = [amenity.strip() for amenity in all_amenities.split(',')]
            amenity_counts = pd.Series(amenities_list).value_counts().reset_index()
            amenity_counts.columns = ['Amenity', 'Count']

            top_10_common_amenities = amenity_counts.head(10)

            fig = px.pie(top_10_common_amenities, values='Count', names='Amenity',
                        title='Top 10 Most Common Amenities Provided in Listings', width=1300,height=700)
            st.plotly_chart(fig)

        # ------------------------------------ Which city has the highest number of available listings in the next 30 days?

        elif title=='5.Distribution of Average Review Scores for Top Hosts':

            
            avg_review_scores_by_host = df.groupby('Host_id')['Review_scores'].mean().reset_index()
            avg_review_scores_by_host = avg_review_scores_by_host.sort_values(by='Review_scores', ascending=False)
            top_hosts = avg_review_scores_by_host.head(10)

            fig = px.pie(top_hosts, values='Review_scores', names='Host_id',
                        title='Distribution of Average Review Scores for Top Hosts', width=1300,height=700,color='Host_id',
                        hole=0.4)  
            st.plotly_chart(fig)

        elif title=="6.Top 10 Most Popular Host Verification Methods":

        #-----------------------------------------Which host verification method is the most popular among hosts?

            all_verifications = ', '.join(df['Host_verifications'])
            verifications_list = [verification.strip() for verification in all_verifications.split(',')]
            verification_counts = pd.Series(verifications_list).value_counts().reset_index()
            verification_counts.columns = ['Verification Method', 'Count']

            
            top_10_verification_methods = verification_counts.sort_values(by='Count', ascending=True).head(10)
            fig = px.bar(top_10_verification_methods, x='Verification Method', y='Count',color="Count" ,color_continuous_scale='bluyl',
                        title='Top 10 Most Popular Host Verification Methods', width=1300,height=700,
                        labels={'Verification Method': 'Host Verification Method', 'Count': 'Number of Hosts'})

        
            fig.update_layout(xaxis_title='Verification Method', yaxis_title='Number of Hosts')
            st.plotly_chart(fig)

