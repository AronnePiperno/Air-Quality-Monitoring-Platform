import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from geopy.geocoders import Nominatim
from test_db import *
import data_retrieval

st.set_page_config(layout="wide")

def kpis(latitude, longitude, product):
    values, dates = data_retrieval.by_coordinate(latitude, longitude, product)
    location_average = np.mean(values)
    location_average_f = "{:.6f}".format(location_average)
    return location_average_f, values, dates

def graph_setup (dates, values, city, pollutant):
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 4)
    ax.plot(dates, values, label=city)
    ax.set_xlabel("Date")
    ax.set_ylabel(pollutant)
    date_format = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)
    return fig

def city_selection():
    # Add custom CSS for the background image
    st.title("City Selection")
    city = st.text_input("Enter a city name:")
    
    if st.button("Submit"):
        # Validate city input
        if city.strip():
            geolocator = Nominatim(user_agent="your_app_name")
            location = geolocator.geocode(city)            
            if location is None:
                st.error("I'm sorry, I could not find this city!")
            else:
                st.session_state.selected_city = city
                st.experimental_rerun()

# Data display page
def display_data():
    # Fetch and display data for the selected city
    # You can customize this part to fetch and display the relevant data

    # TITLE
    st.markdown("<h1 style='font-size: 40px; font-family: Roboto, sans-serif;'>Air Quality Monitoring Platform</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 15px; font-family: Arial, sans-serif; font-style: italic; margin-top: -30px'>Alessandro de Ferrari, Tommaso Ferretti</h1>", unsafe_allow_html=True)


    # FIRST ROW
    a1, a2, a3 = st.columns([1,3,1])
    a1.image(Image.open('esa-logo-color.png'), use_column_width=True)
    a2.write("")
    a2.markdown(
        """
        <div style="text-align: justify; font-family: Roboto; font-size: 16px;">
            Stay informed about the air you breathe with our Sentinel-5P Air Quality Dashboard. 
            Discover real-time data on various pollutants and their impact on the environment. 
            Gain insights into the quality of the air around you and make informed decisions for a healthier lifestyle.
            Each pollutant comes with a concise description to help you understand its potential effects.
            Stay up to date with the latest data and track changes in air quality over time.
            Take control of your surroundings and contribute to a cleaner and safer environment.
            With our intuitive dashboard, monitoring air quality has never been easier.
            Breathe easy, stay informed, and make a positive impact on your well-being and the planet.
        </div>
        """,
        unsafe_allow_html=True
    )
    a3.image(Image.open('esa-logo-color.png'), use_column_width=True)

    # City Info
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(st.session_state.selected_city)
    longitude = location.longitude
    latitude = location.latitude

    city = st.session_state.selected_city

    st.write("<p style='align: center;'><strong>City:</strong></p>", unsafe_allow_html=True)
    st.write("<p style='align: center; margin-top: -15px;'>" + str(location) + "</p>", unsafe_allow_html=True)
    st.write("<p style='align: center;'><strong>Latitude:</strong></p>", unsafe_allow_html=True)
    st.write("<p style='align: center; margin-top: -15px;'>" + str(latitude) + "</p>", unsafe_allow_html=True)
    st.write("<p style='align: center;'><strong>Longitude:</strong></p>", unsafe_allow_html=True)
    st.write("<p style='align: center; margin-top: -15px;'>" + str(longitude) + "</p>", unsafe_allow_html=True)


    # Select the pollutant
    selected_values = st.multiselect("Select the pollutant you are looking for:", ["Overall", "CH4", "CO", "HCHO", "NO2", "O3", "SO2"])

    # Overall
    if "Overall" in selected_values:
        st.title("Pollutant Overview")

        a1,a2,a3,a4,a5,a6=st.columns(6)
        a1.markdown("<h2 style='text-align: center;'>CH4</h2>", unsafe_allow_html=True)
        a1.markdown("""
        <div style="text-align: justify;">
            Methane (CH4) is a potent greenhouse gas that contributes to climate change. It is primarily emitted from natural sources such as wetlands and agricultural activities, as well as from human activities such as the production and transport of coal, oil, and gas. Methane plays a significant role in global warming and efforts are underway to reduce its emissions.
        </div>
        """, unsafe_allow_html=True)
        a2.markdown("<h2 style='text-align: center;'>CO</h2>", unsafe_allow_html=True)
        a2.markdown("""
        <div style="text-align: justify;">
            Carbon monoxide (CO) is a colorless and odorless gas produced by the incomplete combustion of fossil fuels, biomass, and other organic materials. It is primarily emitted from vehicles, industrial processes, and residential heating. Carbon monoxide is a toxic gas that can impair oxygen delivery in the body, leading to adverse health effects. Effective control measures have been implemented to reduce CO emissions and improve air quality.
        </div>
        """, unsafe_allow_html=True)
        a3.markdown("<h2 style='text-align: center;'>HCHO</h2>", unsafe_allow_html=True)
        a3.markdown("""
        <div style="text-align: justify;">
            Formaldehyde (HCHO) is a colorless gas with a strong odor. It is released into the air from various sources, including combustion processes, industrial activities, and the use of certain products. Formaldehyde is a known respiratory irritant and exposure to high levels can cause health issues, including eye, nose, and throat irritation. Regulations and guidelines are in place to limit formaldehyde emissions and protect human health.
        </div>
        """, unsafe_allow_html=True)
        a4.markdown("<h2 style='text-align: center;'>NO2</h2>", unsafe_allow_html=True)
        a4.markdown("""
        <div style="text-align: justify;">
            Nitrogen dioxide (NO2) is a reddish-brown gas that forms from the burning of fossil fuels, particularly in vehicles and power plants. It is a major component of urban air pollution and can contribute to the formation of smog. Nitrogen dioxide can have harmful effects on respiratory health, exacerbating asthma and other respiratory conditions. Efforts are being made to reduce NO2 emissions through stricter vehicle emissions standards and cleaner energy sources.
        </div>
        """, unsafe_allow_html=True)
        a5.markdown("<h2 style='text-align: center;'>O3</h2>", unsafe_allow_html=True)
        a5.markdown("""
        <div style="text-align: justify;">
            Ground-level ozone (O3) is a secondary pollutant formed when nitrogen oxides (NOx) and volatile organic compounds (VOCs) react in the presence of sunlight. It is a major component of smog and is known to be a respiratory irritant. Ground-level ozone poses risks to human health, particularly for individuals with respiratory conditions. Measures are in place to control NOx and VOC emissions and maintain ground-level ozone concentrations within acceptable limits.
        </div>
        """, unsafe_allow_html=True)
        a6.markdown("<h2 style='text-align: center;'>SO2</h2>", unsafe_allow_html=True)
        a6.markdown("""
        <div style="text-align: justify;">
            Sulfur dioxide (SO2) is a colorless gas with a pungent odor that is primarily emitted from the burning of fossil fuels, particularly in power plants and industrial processes. It is a respiratory irritant and contributes to the formation of acid rain. Efforts are underway to reduce SO2 emissions through the use of cleaner fuels and emission control technologies.
        </div>
        """, unsafe_allow_html=True)

        # Scorecards

        b1,b2,b3,b4,b5,b6=st.columns(6)

        # CH4
        mean = kpis(latitude,longitude,"L2__CH4___")
        b1.write("")
        b1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 18px;'>CH4 value for {}</h2>
                <p style='text-align: center; font-size: 40px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)
        
        # CO

        mean = kpis(latitude,longitude,"L2__CO___")
        b1.write("")
        b1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 18px;'>CO value for {}</h2>
                <p style='text-align: center; font-size: 40px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # HCHO

        mean = kpis(latitude,longitude,"L2__HCHO____")
        b1.write("")
        b1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 18px;'>HCHO value for {}</h2>
                <p style='text-align: center; font-size: 40px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # NO2

        mean = kpis(latitude,longitude,"L2__NO2__")
        b1.write("")
        b1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 18px;'>NO2 value for {}</h2>
                <p style='text-align: center; font-size: 40px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # O3

        mean = kpis(latitude,longitude,"L2__O3____")
        b1.write("")
        b1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 18px;'>O3 value for {}</h2>
                <p style='text-align: center; font-size: 40px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # SO2
        
        mean = kpis(latitude,longitude,"L2__SO2___")
        b1.write("")
        b1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 18px;'>SO2 value for {}</h2>
                <p style='text-align: center; font-size: 40px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

 
        
    # CH4
    if "CH4" in selected_values:

        # Description

        st.write("")
        st.markdown("<h1 style='font-size: 30px; font-family: Roboto, sans-serif;'>Methane (CH4)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Roboto; font-size: 13px; margin-top: -10px">
                Methane (CH4) is a greenhouse gas and a significant component of air pollution. It is primarily emitted from natural sources such as wetlands, as well as human activities including agriculture, fossil fuel extraction, and waste management. Methane is a potent greenhouse gas, meaning it has a high global warming potential and contributes to climate change.
                Exposure to elevated levels of methane can have environmental and health consequences. Methane itself is not directly harmful to human health. However, its presence in the atmosphere contributes to the greenhouse effect, leading to global warming and climate change. These changes in temperature and weather patterns can have wide-ranging impacts on ecosystems, agriculture, and human societies.
                Efforts to reduce methane emissions are crucial in mitigating climate change. Methane emissions can be reduced by implementing various strategies, such as improving waste management practices, reducing emissions from fossil fuel production and distribution, and implementing agricultural techniques that minimize methane release from livestock and rice cultivation.
                Regulatory agencies and international agreements play a vital role in setting targets and standards for methane emissions reduction. For example, the Paris Agreement aims to limit global warming well below 2 degrees Celsius compared to pre-industrial levels, and countries have made commitments to reduce their greenhouse gas emissions, including methane.
                In conclusion, methane (L2CH4) is a potent greenhouse gas that contributes to climate change. While it is not directly harmful to human health, its presence in the atmosphere has far-reaching environmental impacts. Controlling methane emissions through various strategies is essential for mitigating climate change and protecting the planet's ecosystems and societies.
            </div>
            """,
            unsafe_allow_html=True)


        a1, a2 = st.columns([3,12])

        # Scorecard

        mean, values, dates = kpis(latitude,longitude,"L2__CH4___")
        
        a1.write("")
        a1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 25px;'>CH4 value for {}</h2>
                <p style='text-align: center; font-size: 60px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # Graph

        a2.write("")
        a2.pyplot(graph_setup(dates, values, city, "Methane"))

    # CO
    if "CO" in selected_values:

        # Description

        st.write("")
        st.markdown("<h1 style='font-size: 30px; font-family: Roboto, sans-serif;'>Carbon Monoxide (CO)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Roboto; font-size: 13px; margin-top: -10px">
                Carbon Monoxide (CO) is a colorless and odorless gas that is produced primarily from the incomplete combustion of fossil fuels and biomass. It is a common air pollutant, especially in urban areas with high traffic and industrial activities.
                Exposure to elevated levels of carbon monoxide can have adverse health effects. When inhaled, carbon monoxide binds to hemoglobin in the bloodstream, reducing its ability to carry oxygen to body tissues. This can lead to a decrease in oxygen supply to vital organs, including the heart and brain. Symptoms of carbon monoxide poisoning include headache, dizziness, nausea, confusion, and in severe cases, it can even lead to loss of consciousness and death.
                To mitigate the risks associated with carbon monoxide, it is essential to prevent its formation and limit exposure. This involves implementing measures to improve combustion efficiency and reduce emissions from various sources such as vehicles, industrial processes, and residential heating systems. Regular maintenance of appliances that use fossil fuels, such as furnaces and water heaters, is crucial to ensure proper functioning and prevent the release of carbon monoxide indoors.
                Monitoring and regulation of carbon monoxide levels are important for maintaining air quality and protecting public health. Many countries have established ambient air quality standards for carbon monoxide to ensure that concentrations remain within acceptable limits.
                Public awareness about the dangers of carbon monoxide and the importance of proper ventilation and detection systems in homes and workplaces is also crucial. Carbon monoxide alarms are effective tools for early detection and warning of high levels of this gas.
                In conclusion, carbon monoxide (CO) is a harmful air pollutant that can have severe health effects. Implementing measures to reduce emissions, improve combustion efficiency, and raise awareness about carbon monoxide risks are essential for maintaining air quality and safeguarding public health.
            </div>
            """,
            unsafe_allow_html=True)
        
        a1, a2 = st.columns([3,12])

        # Scorecard

        mean, values, dates = kpis(latitude,longitude,"L2__CO____")
        
        a1.write("")
        a1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 25px;'>CO value for {}</h2>
                <p style='text-align: center; font-size: 60px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # Graph

        a2.write("")
        a2.pyplot(graph_setup(dates, values, city, "Carbon Monoxide"))

    # HCHO
    if "HCHO" in selected_values:

        # Description

        st.write("")
        st.markdown("<h1 style='font-size: 30px; font-family: Roboto, sans-serif;'>Formaldehyde (HCHO)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Roboto; font-size: 13px; margin-top: -10px">
                Formaldehyde (HCHO) is a colorless gas with a strong, pungent odor. It is a volatile organic compound (VOC) that is released into the air from various sources, including industrial processes, combustion of fossil fuels, and certain household products and materials.
                Exposure to elevated levels of formaldehyde can have adverse health effects. It is known to be a respiratory irritant, causing symptoms such as eye, nose, and throat irritation, coughing, and wheezing. Prolonged exposure to formaldehyde has been associated with an increased risk of respiratory conditions such as asthma and allergic reactions. Formaldehyde is also classified as a human carcinogen, with evidence linking it to the development of certain types of cancers, particularly in the respiratory system.
                Efforts to reduce formaldehyde emissions and exposure are crucial for protecting public health. This includes implementing regulations and standards for formaldehyde emissions in industrial processes and consumer products. For example, formaldehyde emissions from building materials and furniture can be regulated to ensure they meet low-emission standards. Additionally, promoting the use of formaldehyde-free or low-formaldehyde products can help reduce exposure.
                Indoor air quality is a significant concern when it comes to formaldehyde exposure. Proper ventilation and air exchange in buildings can help reduce indoor formaldehyde levels. It is also important to avoid smoking indoors, as cigarette smoke is a significant source of formaldehyde.
                Public awareness about formaldehyde exposure and its associated health risks is essential. This includes educating individuals about potential sources of formaldehyde in their environment and providing guidance on how to minimize exposure. Employers should also take steps to protect workers who may be exposed to formaldehyde in occupational settings by implementing appropriate safety measures and personal protective equipment.
                In conclusion, formaldehyde (HCHO) is a volatile organic compound that can have detrimental effects on human health. Taking measures to reduce formaldehyde emissions, regulate exposure in industrial and consumer settings, and promote awareness about formaldehyde sources and risks are essential for safeguarding public health and ensuring a healthier indoor and outdoor environment.
            </div>
            """,
            unsafe_allow_html=True)
        
        a1, a2 = st.columns([3,12])

        # Scorecard

        mean, values, dates = kpis(latitude,longitude,"L2__HCHO__")
        
        a1.write("")
        a1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 25px;'>HCHO value for {}</h2>
                <p style='text-align: center; font-size: 60px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # Graph
        
        a2.write("")
        a2.pyplot(graph_setup(dates, values, city, "Formaldehyde"))


    # NO2
    if "NO2" in selected_values:

        # Description

        st.write("")
        st.markdown("<h1 style='font-size: 30px; font-family: Roboto, sans-serif;'>Nitrogen dioxide (NO2)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Roboto; font-size: 13px; margin-top: -10px">
                Nitrogen Dioxide (NO2) is a reddish-brown gas that is part of the nitrogen oxide (NOx) family of air pollutants. It is primarily emitted from the burning of fossil fuels, particularly in vehicles, power plants, and industrial processes. NO2 is also formed through the atmospheric oxidation of nitric oxide (NO).
                Exposure to elevated levels of nitrogen dioxide can have adverse health effects. It is a respiratory irritant and can worsen respiratory conditions such as asthma and chronic obstructive pulmonary disease (COPD). Prolonged exposure to NO2 can lead to the inflammation of the airways and increased susceptibility to respiratory infections. In areas with high levels of NO2, individuals may experience symptoms such as coughing, wheezing, shortness of breath, and chest tightness.
                Nitrogen dioxide also contributes to the formation of ground-level ozone and particulate matter, which further exacerbate air quality issues and respiratory health risks. Additionally, NO2 plays a role in the formation of acid rain and contributes to the overall air pollution problem.
                To reduce NO2 emissions and mitigate its impact on air quality, various measures can be implemented. These include the use of cleaner fuels and technologies in transportation, such as electric vehicles and improved emission control systems in vehicles and industrial facilities. Urban planning strategies that promote sustainable transportation and reduce traffic congestion can also help reduce NO2 levels in urban areas.
                Regulatory agencies set standards and guidelines for NO2 concentrations to protect public health. Monitoring air quality and implementing effective pollution control measures are essential for maintaining air quality standards and minimizing the health risks associated with nitrogen dioxide.
                In conclusion, nitrogen dioxide (NO2) is a harmful air pollutant emitted primarily from the burning of fossil fuels. Exposure to NO2 can have detrimental effects on respiratory health and contribute to air pollution issues. Implementing measures to reduce NO2 emissions and improve air quality is crucial for protecting public health and creating a more sustainable environment.
            </div>
            """,
            unsafe_allow_html=True)
        
        a1, a2 = st.columns([3,12])

        # Scorecard

        mean, values, dates = kpis(latitude,longitude,"L2__NO2___")
        
        a1.write("")
        a1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 25px;'>NO2 value for {}</h2>
                <p style='text-align: center; font-size: 60px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # Graph

        a2.write("")
        a2.pyplot(graph_setup(dates, values, city, "Nitrogen Dioxide"))
        

        
    # O3
    if "O3" in selected_values:
        st.write("")
        st.markdown("<h1 style='font-size: 30px; font-family: Roboto, sans-serif;'>Ground-level Ozone (O3)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Roboto; font-size: 13px; margin-top: -10px">
                Ground-level Ozone (O3) is a secondary pollutant formed when nitrogen oxides (NOx) and volatile organic compounds (VOCs) react in the presence of sunlight. It is a major component of smog and is primarily found closer to the Earth's surface. While ozone in the upper atmosphere acts as a protective layer, ground-level ozone poses risks to human health.
                Exposure to elevated levels of ground-level ozone can have adverse health consequences. It is known to be a respiratory irritant, leading to symptoms such as coughing, throat irritation, chest discomfort, and shortness of breath. Individuals with respiratory conditions like asthma and chronic obstructive pulmonary disease (COPD) are particularly vulnerable and may experience worsened symptoms. Prolonged exposure to ozone can cause reduced lung function, increased susceptibility to respiratory infections, and the development of chronic respiratory issues.
                To ensure clean air and protect public health, it is crucial to maintain ground-level ozone concentrations within acceptable limits. Regulatory agencies like the Environmental Protection Agency (EPA) establish air quality standards for ozone. In the United States, the current standard for ozone is 0.070 parts per million (ppm) averaged over an 8-hour period. However, even lower levels are desired to achieve optimal air quality and minimize health risks.
                Efforts to reduce ground-level ozone focus on controlling the emissions of NOx and VOCs. This involves implementing stringent regulations for industrial processes, vehicle emissions, and consumer products. Additionally, public awareness campaigns and adherence to air quality advisories are important to mitigate exposure during periods of elevated ozone levels.
                In conclusion, ground-level ozone is a significant component of smog and poses risks to human health, particularly respiratory health. It is crucial to maintain ozone concentrations within acceptable limits through emission controls and public awareness to ensure clean air and protect the well-being of individuals and communities.
            </div>
            """,
            unsafe_allow_html=True)
        
        a1, a2 = st.columns([3,12])

        # Scorecard

        mean, values, dates = kpis(latitude,longitude,"L2__O3____")
        
        a1.write("")
        a1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 25px;'>O3 value for {}</h2>
                <p style='text-align: center; font-size: 60px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # Graph

        a2.write("")
        a2.pyplot(graph_setup(dates, values, city, "Ground-level Ozone"))

    # SO2
    if "SO2" in selected_values:
        st.write("")
        st.markdown("<h1 style='font-size: 30px; font-family: Roboto, sans-serif;'>Sulfur dioxide (SO2)</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: justify; font-family: Roboto; font-size: 13px; margin-top: -10px">
                Sulfur Dioxide (SO2) is a colorless gas with a pungent odor that is primarily emitted from the burning of fossil fuels, particularly in power plants and industrial processes that involve the combustion of sulfur-containing fuels such as coal and oil. SO2 can also be released from natural sources such as volcanic eruptions.
                Exposure to elevated levels of sulfur dioxide can have adverse health effects. It is a respiratory irritant and can cause symptoms such as coughing, wheezing, shortness of breath, and chest tightness. Individuals with pre-existing respiratory conditions, such as asthma, are particularly susceptible to the effects of SO2. Prolonged or repeated exposure to high concentrations of SO2 can lead to respiratory issues and may worsen existing respiratory conditions.
                Sulfur dioxide also contributes to the formation of acid rain, which has detrimental effects on ecosystems, including damage to forests, lakes, and aquatic life. When SO2 is released into the atmosphere, it can react with water, oxygen, and other chemicals to form sulfuric acid, which falls back to the Earth's surface as acid rain.
                To mitigate the impact of sulfur dioxide on air quality and human health, various measures can be implemented. These include the use of cleaner fuels with lower sulfur content, such as low-sulfur coal and alternative energy sources. Installing and upgrading emission control technologies in industrial facilities and power plants can also help reduce SO2 emissions. Additionally, regulatory standards and monitoring systems are important for ensuring compliance and maintaining air quality standards.
                Public awareness about the health risks associated with sulfur dioxide exposure is crucial. This includes providing information on air quality conditions, issuing air quality advisories, and promoting actions to reduce individual exposure, such as avoiding outdoor activities during periods of high SO2 levels.
                In conclusion, sulfur dioxide (SO2) is a harmful air pollutant emitted primarily from the burning of fossil fuels. Exposure to SO2 can have adverse respiratory effects and contribute to the formation of acid rain. Implementing measures to reduce SO2 emissions, using cleaner fuels, and raising public awareness about the associated health risks are essential for protecting human health and the environment.
            </div>
            """,
            unsafe_allow_html=True)
        
        a1, a2 = st.columns([3,12])

        # Scorecard

        mean, values, dates = kpis(latitude,longitude,"L2__SO2___")
        
        a1.write("")
        a1.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; border-radius: 10px; border: 1px solid black; margin-top: 40px;'>
                <h2 style='text-align: center; font-size: 25px;'>SO2 value for {}</h2>
                <p style='text-align: center; font-size: 60px;'>{}</p>
            </div>
            """.format(city, mean),
            unsafe_allow_html=True)

        # Graph

        a2.write("")
        a2.pyplot(graph_setup(dates, values, city, "Sulfur Dioxide"))

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

if __name__ == "__main__":
    main()