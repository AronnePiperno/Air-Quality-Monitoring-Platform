import streamlit as st
import pandas as pd
import numpy as np
import plost
from dashboard_func import *
from PIL import Image
from geopy.geocoders import Nominatim


# Page setting
st.set_page_config(layout="wide",
                   page_title="Air Quality Monitoring",
                   page_icon= "./images/esa-logo-color.png",
                   )

# Page 1
def city_selection():

    # Hide Button
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Add background image
    add_bg_from_local("images/08wildfires-blog-aqi-500-vqhb-videoSixteenByNine3000.jpg")

    # Set up
    st.markdown("<h1 style='color:#00000; font-size: 40px; font-family: Workhorse, sans-serif;'>Location Selection</h1>", unsafe_allow_html=True)
    city = st.text_input("Enter a City, Region or a State:")

    if st.form(key='city_form'):
        # Validate city input
        if city.strip():
            geolocator = Nominatim(user_agent="your_app_name")
            location = geolocator.geocode(city)
            if location is None:
                st.error("I'm sorry, I could not find this location!")
            else:
                st.session_state.selected_city = city
                st.session_state.city_selected = True  # Set flag to indicate city selection
                st.experimental_rerun()
# Page 2

def display_data():
    # Fetch and display data for the selected city
    # You can customize this part to fetch and display the relevant data

    # Hide Button
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-color: #f5f3f4;
    background-size: 180%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # TITLE
    st.markdown("<h1 style='color:#00000; font-size: 40px; font-family: Workhorse Rough, sans-serif;'>Air Quality Monitoring Platform</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#00000; font-size: 15px; font-family: Workhorse Rough, sans-serif; font-style: italic; margin-top: -30px'>Alessandro de Ferrari, Tommaso Ferretti</h1>", unsafe_allow_html=True)

    if st.button("Restart"):

            city = None
            st.session_state.selected_city = None
            st.session_state.city_selected = False  # Remove the flag to reset city selection
            st.experimental_rerun()

    # FIRST ROW

    a1, a2, a3 = st.columns(3)  # Adjust the width values as per your requirement

    with open("./images/esa-logo-color.png", "rb") as f:
        image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode()
    markdown_text = f'<div style="text-align: center;"><img src="data:image/jpg;base64,{encoded_image}" alt="Image" style="width: 200px;"></div>'
    a1.markdown(markdown_text, unsafe_allow_html=True)

    with open('images/Sigillo_Università_di_Trento.svg.png', "rb") as f:
        image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode()
    markdown_text = f'<div style="text-align: center;"><img src="data:image/jpg;base64,{encoded_image}" alt="Image" style="width: 120px;"></div>'
    a2.markdown(markdown_text, unsafe_allow_html=True)

    with open('images/Copernicus_fb.png', "rb") as f:
        image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode()
    markdown_text = f'<div style="text-align: center;"><img src="data:image/jpg;base64,{encoded_image}" alt="Image" style="width: 200px;"></div>'
    a3.markdown(markdown_text, unsafe_allow_html=True)


    # Introduction

    container_style = '''
        border-radius: 10px;
        background-color: #ffffff;
        padding: 20px;
        margin-bottom: 20px;
        text-align: justify;
        color: #000000;
        font-family: Workhorse Regular, sans-serif;
    '''

    st.write("")
    st.write("")
    st.markdown(
        f'<div style="{container_style}">Stay informed about the air you breathe with our Sentinel-5P Air Quality Dashboard. Discover real-time data on various pollutants and their impact on the environment. Gain insights into the quality of the air around you and make informed decisions for a healthier lifestyle. Each pollutant comes with a concise description to help you understand its potential effects. Stay up to date with the latest data and track changes in air quality over time. Take control of your surroundings and contribute to a cleaner and safer environment. With our intuitive dashboard, monitoring air quality has never been easier. Breathe easy, stay informed, and make a positive impact on your well-being and the planet.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # City Info
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(st.session_state.selected_city, language="en")
    longitude = location.longitude
    latitude = location.latitude

    st.write("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    st.write("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.write("<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'><strong>Location:</strong> " + str(location) + "</p>", unsafe_allow_html=True)
    st.write("<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'><strong>Latitude:</strong> " + str(latitude) + "</p>", unsafe_allow_html=True)
    st.write("<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'><strong>Longitude:</strong> " + str(longitude) + "</p>", unsafe_allow_html=True)
    st.write("</div>", unsafe_allow_html=True)
    st.write("</div>", unsafe_allow_html=True)


    # Select the pollutant
    selected_values = st.selectbox("Select the pollutant you are looking for:", (["CO", "HCHO", "NO2", "O3", "SO2", "Overall"]))


    # Overall
    if "Overall" in selected_values:

        st.write("")

        a1,a2,a3,a4,a5 = st.columns(5, gap="medium")

        # Scorecards

        scorecard_style = '''
            border-radius: 10px;
            background-color: #ffffff;
            padding: 20px;
            margin-bottom: 20px;
            color: #000000;
            font-family: Workhorse Regular, sans-serif;
            text-align: center;
        '''

        name_style = "font-size: 18px;"
        level_style = "font-size: 50px;"

        # CO

        mean_CO, values_CO, dates_CO = kpis(latitude,longitude,"L2__CO____")
        df_CO = pd.DataFrame(values_CO, dates_CO)

        co_level_html = f'<div style="{name_style}">CO level</div>'
        level_co_html = f'<div style="{level_style}">{mean_CO}</div>'
        
        container_html = f'<div style="{scorecard_style}">{co_level_html}{level_co_html}</div>'
        a1.markdown(container_html, unsafe_allow_html=True)

        # HCHO

        mean_HCHO, values_HCHO, dates_HCHO = kpis(latitude,longitude,"L2__HCHO__")
        df_HCHO = pd.DataFrame(values_HCHO, dates_HCHO)

        hcho_level_html = f'<div style="{name_style}">HCHO level</div>'
        level_hcho_html = f'<div style="{level_style}">{mean_HCHO}</div>'

        container_html = f'<div style="{scorecard_style}">{hcho_level_html}{level_hcho_html}</div>'
        a2.markdown(container_html, unsafe_allow_html=True)

        # NO2

        mean_NO2, values_NO2, dates_NO2 = kpis(latitude,longitude,"L2__NO2___")
        df_NO2 = pd.DataFrame(values_NO2, dates_NO2)

        no2_level_html = f'<div style="{name_style}">NO2 level</div>'
        level_no2_html = f'<div style="{level_style}">{mean_NO2}</div>'

        container_html = f'<div style="{scorecard_style}">{no2_level_html}{level_no2_html}</div>'
        a3.markdown(container_html, unsafe_allow_html=True)

        # O3

        mean_O3, values_O3, dates_O3 = kpis(latitude,longitude,"L2__O3____")
        df_O3 = pd.DataFrame(values_O3, dates_O3)

        o3_level_html = f'<div style="{name_style}">O3 level</div>'
        level_o3_html = f'<div style="{level_style}">{mean_O3}</div>'

        container_html = f'<div style="{scorecard_style}">{o3_level_html}{level_o3_html}</div>'
        a4.markdown(container_html, unsafe_allow_html=True)

        # SO2

        mean_SO2, values_SO2, dates_SO2 = kpis(latitude,longitude,"L2__SO2___")
        df_SO2 = pd.DataFrame(values_SO2, dates_SO2)

        so2_level_html = f'<div style="{name_style}">SO2 level</div>'
        level_so2_html = f'<div style="{level_style}">{mean_SO2}</div>'

        container_html = f'<div style="{scorecard_style}">{so2_level_html}{level_so2_html}</div>'
        a5.markdown(container_html, unsafe_allow_html=True)

        # Description

        #a1.markdown("<h2 style='text-align: center; font-family: Workhorse Rough, sans-serif;'>CO</h2>", unsafe_allow_html=True)
        a1.markdown("""
        <div style="font-family: Workhorse Regular sans-serif;">
            Carbon monoxide (CO) is a colorless and odorless gas produced by the incomplete combustion of fossil fuels, biomass, and other organic materials. It is primarily emitted from vehicles, industrial processes, and residential heating. Carbon monoxide is a toxic gas that can impair oxygen delivery in the body, leading to adverse health effects. Effective control measures have been implemented to reduce CO emissions and improve air quality.
        </div>
        """, unsafe_allow_html=True)
        #a2.markdown("<h2 style='text-align: center; font-family: Workhorse Rough, sans-serif;'>HCHO</h2>", unsafe_allow_html=True)
        a2.markdown("""
        <div style="font-family: Workhorse Regular sans-serif;">
            Formaldehyde (HCHO) is a colorless gas with a strong odor. It is released into the air from various sources, including combustion processes, industrial activities, and the use of certain products. Formaldehyde is a known respiratory irritant and exposure to high levels can cause health issues, including eye, nose, and throat irritation. Regulations and guidelines are in place to limit formaldehyde emissions and protect human health.
        </div>
        """, unsafe_allow_html=True)
        #a3.markdown("<h2 style='text-align: center; font-family: Workhorse Rough, sans-serif;'>NO2</h2>", unsafe_allow_html=True)
        a3.markdown("""
        <div style="font-family: Workhorse Regular sans-serif;">
            Nitrogen dioxide (NO2) is a reddish-brown gas that forms from the burning of fossil fuels, particularly in vehicles and power plants. It is a major component of urban air pollution and can contribute to the formation of smog. Nitrogen dioxide can have harmful effects on respiratory health, exacerbating asthma and other respiratory conditions. Efforts are being made to reduce NO2 emissions through stricter vehicle emissions standards and cleaner energy sources.
        </div>
        """, unsafe_allow_html=True)
        #a4.markdown("<h2 style='text-align: center; font-family: Workhorse Rough, sans-serif;'>O3</h2>", unsafe_allow_html=True)
        a4.markdown("""
        <div style="font-family: Workhorse Regular sans-serif;">
            Ground-level ozone (O3) is a secondary pollutant formed when nitrogen oxides (NOx) and volatile organic compounds (VOCs) react in the presence of sunlight. It is a major component of smog and is known to be a respiratory irritant. Ground-level ozone poses risks to human health, particularly for individuals with respiratory conditions. Measures are in place to control NOx and VOC emissions and maintain ground-level ozone concentrations within acceptable limits.
        </div>
        """, unsafe_allow_html=True)
        #a5.markdown("<h2 style='text-align: center; font-family: Workhorse Rough, sans-serif;'>SO2</h2>", unsafe_allow_html=True)
        a5.markdown("""
        <div style="font-family: Workhorse Regular sans-serif;">
            Sulfur dioxide (SO2) is a colorless gas with a pungent odor that is primarily emitted from the burning of fossil fuels, particularly in power plants and industrial processes. It is a respiratory irritant and contributes to the formation of acid rain. Efforts are underway to reduce SO2 emissions through the use of cleaner fuels and emission control technologies.
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        aqi_value = data_retrieval.calc_aqi(latitude, longitude)
        st.write(
            f"<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'>AQI: <strong>{aqi_value}</strong>",
            unsafe_allow_html=True)
        st.write("")
        color = get_color(aqi_value)
        html_code = f"""
            <div style="width: 200px; height: 200px; background-color: {color}; 
                        display: flex; justify-content: center; align-items: center;">
                <p style="color: white; font-size: 24px;">{aqi_value}</p>
            </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)
        quality = get_quality(color)
        st.write("")
        st.write(f"<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'>The Air Quality is <strong>{quality}</strong>",
                 unsafe_allow_html=True)
        st.write("")
        st.markdown('''
            <div style="display: flex; justify-content: space-between; margin-top: 20px;">
                <div style="background-color: green; height: 20px; width: 20px; border-radius: 5px;"></div>
                <div style="background-color: yellow; height: 20px; width: 20px; border-radius: 5px;"></div>
                <div style="background-color: orange; height: 20px; width: 20px; border-radius: 5px;"></div>
                <div style="background-color: red; height: 20px; width: 20px; border-radius: 5px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Good</span>
                <span>Fair</span>
                <span>Poor</span>
                <span>Very Poor</span>
            </div>
        ''', unsafe_allow_html=True)

        
        
    # CO
    if "CO" in selected_values:

        st.write("")
        st.markdown("<h1 style='font-size: 30px;  font-family: Workhorse Rough, sans-serif;'>Carbon Monoxide (CO)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify;  font-family: Workhorse Regular, sans-serif;font-size: 13px; margin-top: -10px">
                Carbon Monoxide (CO) is a colorless and odorless gas that is produced primarily from the incomplete combustion of fossil fuels and biomass. It is a common air pollutant, especially in urban areas with high traffic and industrial activities.<br>
                Exposure to elevated levels of carbon monoxide can have adverse health effects. When inhaled, carbon monoxide binds to hemoglobin in the bloodstream, reducing its ability to carry oxygen to body tissues. This can lead to a decrease in oxygen supply to vital organs, including the heart and brain. Symptoms of carbon monoxide poisoning include headache, dizziness, nausea, confusion, and in severe cases, it can even lead to loss of consciousness and death.<br>
                To mitigate the risks associated with carbon monoxide, it is essential to prevent its formation and limit exposure. This involves implementing measures to improve combustion efficiency and reduce emissions from various sources such as vehicles, industrial processes, and residential heating systems. Regular maintenance of appliances that use fossil fuels, such as furnaces and water heaters, is crucial to ensure proper functioning and prevent the release of carbon monoxide indoors.<br>
                Monitoring and regulation of carbon monoxide levels are important for maintaining air quality and protecting public health. Many countries have established ambient air quality standards for carbon monoxide to ensure that concentrations remain within acceptable limits.<br>
                Public awareness about the dangers of carbon monoxide and the importance of proper ventilation and detection systems in homes and workplaces is also crucial. Carbon monoxide alarms are effective tools for early detection and warning of high levels of this gas.<br>
                In conclusion, carbon monoxide (CO) is a harmful air pollutant that can have severe health effects. Implementing measures to reduce emissions, improve combustion efficiency, and raise awareness about carbon monoxide risks are essential for maintaining air quality and safeguarding public health.
            </div>
            """,
            unsafe_allow_html=True)
        st.write("")
        st.write("")

        st.write("<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'>Critical threshold for CO: <strong>0.033 mol/m^2</strong>", unsafe_allow_html=True)
        st.write("")

        mean_CO, values_CO, dates_CO = kpis(latitude,longitude,"L2__CO____")
        df_CO = pd.DataFrame(values_CO, dates_CO)

        if len(values_CO)==0:
            st.write("")
            st.write("<div style='display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; font-family: Workhorse, sans-serif;'>", unsafe_allow_html=True)
            st.write("<h3>No data available for this pollutant</h3>")
            st.write("</div>", unsafe_allow_html=True)
       
        else:

            # Graph

            st.pyplot(graph_setup(df_CO, values_CO, dates_CO, "L2__CO____"))
            st.write("")
            city = location.raw['display_name'].split(", ")[0]
            city_2nd = st.text_input(f"Do you want to compare {city} with another location?")
            if city_2nd.strip():
                st.pyplot(graph_comparison_setup(df_CO, city, city_2nd, "L2__CO____"))


    # HCHO
    if "HCHO" in selected_values:

        st.write("")
        st.markdown("<h1 style='font-size: 30px;  font-family: Workhorse Rough, sans-serif;'>Formaldehyde (HCHO)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Workhorse Regular, sans-serif; font-size: 13px; margin-top: -10px">
                Formaldehyde (HCHO) is a colorless gas with a strong, pungent odor. It is a volatile organic compound (VOC) that is released into the air from various sources, including industrial processes, combustion of fossil fuels, and certain household products and materials.<br>
                Exposure to elevated levels of formaldehyde can have adverse health effects. It is known to be a respiratory irritant, causing symptoms such as eye, nose, and throat irritation, coughing, and wheezing. Prolonged exposure to formaldehyde has been associated with an increased risk of respiratory conditions such as asthma and allergic reactions. Formaldehyde is also classified as a human carcinogen, with evidence linking it to the development of certain types of cancers, particularly in the respiratory system.<br>
                Efforts to reduce formaldehyde emissions and exposure are crucial for protecting public health. This includes implementing regulations and standards for formaldehyde emissions in industrial processes and consumer products. For example, formaldehyde emissions from building materials and furniture can be regulated to ensure they meet low-emission standards. Additionally, promoting the use of formaldehyde-free or low-formaldehyde products can help reduce exposure.<br>
                Indoor air quality is a significant concern when it comes to formaldehyde exposure. Proper ventilation and air exchange in buildings can help reduce indoor formaldehyde levels. It is also important to avoid smoking indoors, as cigarette smoke is a significant source of formaldehyde.<br>
                Public awareness about formaldehyde exposure and its associated health risks is essential. This includes educating individuals about potential sources of formaldehyde in their environment and providing guidance on how to minimize exposure. Employers should also take steps to protect workers who may be exposed to formaldehyde in occupational settings by implementing appropriate safety measures and personal protective equipment.<br>
                In conclusion, formaldehyde (HCHO) is a volatile organic compound that can have detrimental effects on human health. Taking measures to reduce formaldehyde emissions, regulate exposure in industrial and consumer settings, and promote awareness about formaldehyde sources and risks are essential for safeguarding public health and ensuring a healthier indoor and outdoor environment.
            </div>
            """,
            unsafe_allow_html=True)
        
        st.write("")
        st.write("")

        st.write("<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'>Critical threshold for HCHO: <strong>0.0025 mol/m^2</strong>", unsafe_allow_html=True)
        st.write("")

        mean_HCHO, values_HCHO, dates_HCHO = kpis(latitude,longitude,"L2__HCHO__")
        df_HCHO = pd.DataFrame(values_HCHO, dates_HCHO)

        if len(values_HCHO)==0:
            st.write("")
            st.write("<div style='display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; font-family: Workhorse, sans-serif;'>", unsafe_allow_html=True)
            st.write("<h3>No data available for this pollutant</h3>")
            st.write("</div>", unsafe_allow_html=True)
        
        else:

            # Graph

            st.pyplot(graph_setup(df_HCHO, values_HCHO, dates_HCHO, "L2__HCHO__"))
            st.write("")
            city = location.raw['display_name'].split(", ")[0]
            city_2nd = st.text_input(f"Do you want to compare {city} with another location?")
            if city_2nd.strip():
                st.pyplot(graph_comparison_setup(df_HCHO, city, city_2nd, "L2__HCHO__"))


    # NO2
    if "NO2" in selected_values:

        st.write("")
        st.markdown("<h1 style='font-size: 30px;  font-family: Workhorse Rough, sans-serif;'>Nitrogen Dioxide (NO2)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Roboto; font-size: 13px; margin-top: -10px">
                Nitrogen Dioxide (NO2) is a reddish-brown gas that is part of the nitrogen oxide (NOx) family of air pollutants. It is primarily emitted from the burning of fossil fuels, particularly in vehicles, power plants, and industrial processes. NO2 is also formed through the atmospheric oxidation of nitric oxide (NO).<br>
                Exposure to elevated levels of nitrogen dioxide can have adverse health effects. It is a respiratory irritant and can worsen respiratory conditions such as asthma and chronic obstructive pulmonary disease (COPD). Prolonged exposure to NO2 can lead to the inflammation of the airways and increased susceptibility to respiratory infections. In areas with high levels of NO2, individuals may experience symptoms such as coughing, wheezing, shortness of breath, and chest tightness.<br>
                Nitrogen dioxide also contributes to the formation of ground-level ozone and particulate matter, which further exacerbate air quality issues and respiratory health risks. Additionally, NO2 plays a role in the formation of acid rain and contributes to the overall air pollution problem.<br>
                To reduce NO2 emissions and mitigate its impact on air quality, various measures can be implemented. These include the use of cleaner fuels and technologies in transportation, such as electric vehicles and improved emission control systems in vehicles and industrial facilities. Urban planning strategies that promote sustainable transportation and reduce traffic congestion can also help reduce NO2 levels in urban areas.<br>
                Regulatory agencies set standards and guidelines for NO2 concentrations to protect public health. Monitoring air quality and implementing effective pollution control measures are essential for maintaining air quality standards and minimizing the health risks associated with nitrogen dioxide.<br>
                In conclusion, nitrogen dioxide (NO2) is a harmful air pollutant emitted primarily from the burning of fossil fuels. Exposure to NO2 can have detrimental effects on respiratory health and contribute to air pollution issues. Implementing measures to reduce NO2 emissions and improve air quality is crucial for protecting public health and creating a more sustainable environment.
            </div>
            """,
            unsafe_allow_html=True)
        
        st.write("")
        st.write("")

        st.write("<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'>Critical threshold for NO2: <strong>0.00006 mol/m^2</strong>", unsafe_allow_html=True)
        st.write("")

        mean_NO2, values_NO2, dates_NO2 = kpis(latitude,longitude,"L2__NO2___")
        df_NO2 = pd.DataFrame(values_NO2, dates_NO2)

        if len(values_NO2)==0:
            st.write("")
            st.write("<div style='display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; font-family: Workhorse, sans-serif;'>", unsafe_allow_html=True)
            st.write("<h3>No data available for this pollutant</h3>")
            st.write("</div>", unsafe_allow_html=True)
        
        else:

            # Graph

            st.pyplot(graph_setup(df_NO2, values_NO2, dates_NO2, "L2__NO2___"))
            st.write("")
            city = location.raw['display_name'].split(", ")[0]
            city_2nd = st.text_input(f"Do you want to compare {city} with another location?")
            if city_2nd.strip():
                st.pyplot(graph_comparison_setup(df_NO2, city, city_2nd, "L2__NO2___"))


    # O3
    if "O3" in selected_values:

        st.write("")
        st.markdown("<h1 style='font-size: 30px;  font-family: Workhorse Rough, sans-serif;'>Ground-level Ozone (O3)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Roboto; font-size: 13px; margin-top: -10px">
                Ground-level Ozone (O3) is a secondary pollutant formed when nitrogen oxides (NOx) and volatile organic compounds (VOCs) react in the presence of sunlight. It is a major component of smog and is primarily found closer to the Earth's surface. While ozone in the upper atmosphere acts as a protective layer, ground-level ozone poses risks to human health.<br>
                Exposure to elevated levels of ground-level ozone can have adverse health consequences. It is known to be a respiratory irritant, leading to symptoms such as coughing, throat irritation, chest discomfort, and shortness of breath. Individuals with respiratory conditions like asthma and chronic obstructive pulmonary disease (COPD) are particularly vulnerable and may experience worsened symptoms. Prolonged exposure to ozone can cause reduced lung function, increased susceptibility to respiratory infections, and the development of chronic respiratory issues.<br>
                To ensure clean air and protect public health, it is crucial to maintain ground-level ozone concentrations within acceptable limits. Regulatory agencies like the Environmental Protection Agency (EPA) establish air quality standards for ozone. In the United States, the current standard for ozone is 0.070 parts per million (ppm) averaged over an 8-hour period. However, even lower levels are desired to achieve optimal air quality and minimize health risks.<br>
                Efforts to reduce ground-level ozone focus on controlling the emissions of NOx and VOCs. This involves implementing stringent regulations for industrial processes, vehicle emissions, and consumer products. Additionally, public awareness campaigns and adherence to air quality advisories are important to mitigate exposure during periods of elevated ozone levels.<br>
                In conclusion, ground-level ozone is a significant component of smog and poses risks to human health, particularly respiratory health. It is crucial to maintain ozone concentrations within acceptable limits through emission controls and public awareness to ensure clean air and protect the well-being of individuals and communities.
            </div>
            """,
            unsafe_allow_html=True)
        
        st.write("")
        st.write("")

        st.write("<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'>Critical threshold for O3: <strong>0.17 mol/m^2</strong>", unsafe_allow_html=True)
        st.write("")

        mean_O3, values_O3, dates_O3 = kpis(latitude,longitude,"L2__O3____")
        df_O3 = pd.DataFrame(values_O3, dates_O3)

        if len(values_O3)==0:
            st.write("")
            st.write("<div style='display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; font-family: Workhorse, sans-serif;'>", unsafe_allow_html=True)
            st.write("<h3>No data available for this pollutant</h3>")
            st.write("</div>", unsafe_allow_html=True)
        
        else:

            # Graph

            st.pyplot(graph_setup(df_O3, values_O3, dates_O3, "L2__O3____"))
            st.write("")
            city = location.raw['display_name'].split(", ")[0]
            city_2nd = st.text_input(f"Do you want to compare {city} with another location?")
            if city_2nd.strip():
                st.pyplot(graph_comparison_setup(df_O3, city, city_2nd, "L2__O3____"))       


    # SO2
    if "SO2" in selected_values:

        st.write("")
        st.markdown("<h1 style='font-size: 30px;  font-family: Workhorse Rough, sans-serif;'>Sulfur Dioxide (SO2)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Roboto; font-size: 13px; margin-top: -10px">
                Sulfur Dioxide (SO2) is a colorless gas with a pungent odor that is primarily emitted from the burning of fossil fuels, particularly in power plants and industrial processes that involve the combustion of sulfur-containing fuels such as coal and oil. SO2 can also be released from natural sources such as volcanic eruptions.<br>
                Exposure to elevated levels of sulfur dioxide can have adverse health effects. It is a respiratory irritant and can cause symptoms such as coughing, wheezing, shortness of breath, and chest tightness. Individuals with pre-existing respiratory conditions, such as asthma, are particularly susceptible to the effects of SO2. Prolonged or repeated exposure to high concentrations of SO2 can lead to respiratory issues and may worsen existing respiratory conditions.<br>
                Sulfur dioxide also contributes to the formation of acid rain, which has detrimental effects on ecosystems, including damage to forests, lakes, and aquatic life. When SO2 is released into the atmosphere, it can react with water, oxygen, and other chemicals to form sulfuric acid, which falls back to the Earth's surface as acid rain.<br>
                To mitigate the impact of sulfur dioxide on air quality and human health, various measures can be implemented. These include the use of cleaner fuels with lower sulfur content, such as low-sulfur coal and alternative energy sources. Installing and upgrading emission control technologies in industrial facilities and power plants can also help reduce SO2 emissions. Additionally, regulatory standards and monitoring systems are important for ensuring compliance and maintaining air quality standards.<br>
                Public awareness about the health risks associated with sulfur dioxide exposure is crucial. This includes providing information on air quality conditions, issuing air quality advisories, and promoting actions to reduce individual exposure, such as avoiding outdoor activities during periods of high SO2 levels.<br>
                In conclusion, sulfur dioxide (SO2) is a harmful air pollutant emitted primarily from the burning of fossil fuels. Exposure to SO2 can have adverse respiratory effects and contribute to the formation of acid rain. Implementing measures to reduce SO2 emissions, using cleaner fuels, and raising public awareness about the associated health risks are essential for protecting human health and the environment.
            </div>
            """,
            unsafe_allow_html=True)
        
        st.write("")
        st.write("")

        st.write("<p style='color:#00000; font-family: Workhorse Regular, sans-serif;'>Critical threshold for SO2: <strong>0.0003 mol/m^2</strong>", unsafe_allow_html=True)
        st.write("")

        mean_SO2, values_SO2, dates_SO2 = kpis(latitude,longitude,"L2__SO2___")
        df_SO2 = pd.DataFrame(values_SO2, dates_SO2)

        if len(values_SO2)==0:
            st.write("")
            st.write("<div style='display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; font-family: Workhorse, sans-serif;'>", unsafe_allow_html=True)
            st.write("<h3>No data available for this pollutant</h3>")
            st.write("</div>", unsafe_allow_html=True)
        
        else:

            # Graph

            st.pyplot(graph_setup(df_SO2, values_SO2, dates_SO2, "L2__SO2___"))
            st.write("")
            city = location.raw['display_name'].split(", ")[0]
            city_2nd = st.text_input(f"Do you want to compare {city} with another location?")
            if city_2nd.strip():
                st.pyplot(graph_comparison_setup(df_SO2, city, city_2nd, "L2__SO2___"))

# Main function
def main():

    # Check if the selected_city attribute exists in session state
    if "selected_city" not in st.session_state:
        # Initialize selected_city attribute
        st.session_state.selected_city = None

    # Display the appropriate page based on the selected city
    if st.session_state.selected_city is None:
        city_selection()
    else:
        display_data()

if __name__ == '__main__':
    main()