# wpQGIS-Datasets-Plugin

##### A plugin for QGIS 3 that helps users download files from the WorldPop Project

### Installation Instructions

1. Download the repository
2. Place the  wpdatasets folder at your QGIS3 addon folder:
    * C:/Users/__username__/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins
    * If the subfolder _plugins_ does not exist, you can create it manually.

##### Things to be done
 - [ ] Put logger statements.
 - [ ] Add Start/Stop/Pause functionality in the download logic.
 - [ ] Make it work with Linux pyQt. 
 - [ ] More documentation/Comments
 
 

_mostly notes to myself:_

 - Developing Plugin Notes
 https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins.html

My Plugin directory:
- C:/Users/nv1g17/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins

to compile/deploy use [pb_tool][0]

> pb_tool deploy

[0]: https://github.com/g-sherman/plugin_build_tool/tree/qgis3_version

