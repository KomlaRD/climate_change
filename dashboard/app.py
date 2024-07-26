# Import libraries
import matplotlib.pyplot as plt # Visualisation
import pandas as pd # Data manipulation and analysis
from faicons import icon_svg # Icons
import datetime # Manipulate date time

# Import data from shared.py
from shared import app_dir, df
# Shiny modules
from shiny import reactive
from shiny.express import input, render, ui

# Title page
ui.h1("Historical Emissions from Ghana, Rwanda, and Zimbabwe")

# # Navigation tabs
with ui.navset_tab(id="home"):
    # Home tab
    with ui.nav_panel("Home"):
        #  Value boxes for the sum of unit price, sales volume and sales value
        with ui.layout_columns(fill=False):
            with ui.value_box(showcase=icon_svg("database")):
                "Total Gas Emissions"
                @render.text
                def emission():
                    """
                    Calculate emission

                    Args
                    ----
                    None

                    Returns
                    -------
                    
                    """
                    total_emission = filtered_df()['Emissions'].sum().round(1)
                    # Formatting the total_unit_price with commas
                    formatted_emission = f"{total_emission:,}"
                    return formatted_emission

        # Plot on monthly sales over time        
        with ui.layout_columns(fill=False):
             with ui.card():
                "Emissions plot"
                @render.plot
                def plot_emissions():
                    """
                    Plot Gas Emissions

                    Args
                    ----
                    None

                    Returns
                    -------
                    fig (plot): Emissons over time
                    """
                    df_emissions = filtered_df()
                    df_emissions.set_index("Year_dt", inplace=True)

                    # Plot the time series data
                    fig = plt.figure(figsize=(12, 6))
                    plt.plot(df_emissions.index,
                                 df_emissions['Emissions'], marker='o')
                    plt.title('Emissions over time')
                    plt.xlabel('Year')
                    plt.ylabel('Emissions')
                    plt.grid(True)
                    return fig
    

# Sidebar: Filter controls
with ui.sidebar(title="Filter controls", open="desktop"):
    # # Date selector
    # ui.input_date_range(
    #     "date",
    #     "Date range",
    #     start=start,
    #     end=end,
    #     min=start,
    #     max=end,
    #     width="100"
    # )

    # Countries selector
    ui.input_checkbox_group(
        "country",
        "Countries",
        ["Ghana", "Rwanda", "Zimbabwe"],
        selected=["Ghana", "Rwanda", "Zimbabwe"],
    )

    # # Year selector
    # ui.input_checkbox_group(
    #     "year",
    #     "Year",
    #     [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014],
    #     selected=[2021])
    
    # Manufacturer selector
    ui.input_checkbox_group(
        "gas",
        "Gas",
        ['All GHG', 'CH4', 'N2O'],
        selected=['All GHG', 'CH4', 'N2O']
    )
    
    # Buttons
    ui.input_action_button("filter", "Filter") # Filter
    ui.input_action_button("reset", "Reset") # Reset

# CSS stylesheet
ui.include_css(app_dir / "styles.css")

# Reactive data
@reactive.calc
@reactive.event(input.filter, ignore_none=False)
def filtered_df():
    """
    Reactively calculate the dataset output

    Args
    ----
    None

    Returns
    -------
    filt_df (dataframe): Unfiltered or filtered dataframe
    """
    df_country = df["Country"].isin(input.country())
    # df_year = df["Year_object"].isin(input.year())
    df_gas = df["Gas"].isin(input.gas())
    return df[df_country & df_gas]

# @reactive.effect
# @reactive.event(input.reset)
# def _():
#     """
#     Reset filters
#     """
#     ui.update_date_range("date", start=start, end=end)
#     ui.update_checkbox_group("city", selected=["Abidjan", "Bouake"])
#     ui.update_checkbox_group("channel", selected=[
#                              "Groceries", "Open_Market", "Boutique"])
#     ui.update_checkbox_group("manufacturer", 
#                              selected=['CAPRA', 'GOYMEN FOODS', 'DOUBA', 'PAGANINI', 'PANZANI',
#                                         'PASTA DOUBA', 'MR COOK', 'TAT MAKARNACILIK SANAYI VE TICARET AS',
#                                         'REINE', 'MOULIN MODERNE', 'AVOS GROUP', 'OBA MAKARNA'])
#     ui.update_checkbox_group("pack_size", selected=[
#                              '200G', '500G', '4540G', '475G', '250G', '450G'])
#     ui.update_checkbox_group("packaging", selected=['SACHET', 'BAG'])
