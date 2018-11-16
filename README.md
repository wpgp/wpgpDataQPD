# wpDatasets

About
-----
##### A plugin for QGIS 3 that helps users download raster products from the WorldPop Global Project

The WorldPop Global High Resolution Population Denominators Project, 
funded by the Bill and Melinda Gates Foundation (OPP1134076), has 
produced an open-access archive of 3-arc seconds (approximately 100m 
at the equator) gridded population datasets, also structured by gender 
and age groups, for 249 countries, dependencies, and territories for 
21-years (2000-2020), using the methods described by [Stevens et al., 
2015](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0107042), 
[Gaughan et al., 2016](https://www.nature.com/articles/sdata20165), and [Pezzulo et al., 
2017](https://www.nature.com/articles/sdata201789). In addition, the project has also 
made available the covariate datasets used as inputs to produce the gridded population 
datasets (Lloyd et al., under review). These datasets are available for download from 
the WorldPop website and FTP server using a range of methods and tools.

Installation Instructions
-----

1. Download the repository, using the top right green button.
2. Place the  wpdatasets folder at your QGIS3 addon folder:
    * _Windows_ C:/Users/__username__/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins  
     _<Ubuntu>_ ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins
    * If the subfolder _plugins_ does not exist, you can create it manually.

 
 Usage
 -----
 
 1. After you put the folder into the appropriate directory you should enable it from 
 __Plugins ->Manage and install Plugins ...__
 
 ![enable plugin image](/images/enable_plugin.JPG)
 
 2. A new entry should appear at the plugins menu:
 
 ![](/images/tool_bar_location.JPG)
 
 Clicking the button will open the plugin's main window:
 
 ![](/images/plugin_main_window.JPG)
 
 From this point the plugin is very straight forward: 
 
 ![](/images/selected_product.JPG)
 
  - Each country, is a parent which contains a number of datasets. 
  
  - After you locate the desired dataset from the list you can then click `download` and the addon will 
  fetch that raster from the WorldPop FTP and store it your desired folder.
    - If the `Add downloaded file into Layer List` is checked, the downloaded file will be added automatically 
    at the running QGIS layer list
  
  
ISSUES
-----


For any issues that may arise please open a ticket in our [GitHub repo](https://github.com/wpgp/wpgpDataQPD/issues)
