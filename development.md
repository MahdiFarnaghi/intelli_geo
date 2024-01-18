# Development Instruction

1. Clone the project ino the plugins folder of your QGIS
    - To find the path, open QGIS and then go to `Settings > User profiles > Open Active Profile Folder`. The plugin folder is with `python` folder.
2. Create `QGISDIR` environmental variable pointing to the plugins folder.
3. Create a Python environment in your project and activate it in a terminal.
4. Use QT Designer to modify the interface 

    -  Open QT designer installed by QGIS
    - Open the `intelli_geo_dockwidget_base.ui`
    
        - Modify
        - Save
5. Compile the interface using `pb_tools`

    - Using pip install the pb_tools

        `pip install pb-tool`

    - Using pip install pyqt5ac

        `pip install pyqt5ac`
    - Check to see if the pb_tool.exe is in the scripts folder of the python environment
    - On the terminal, go the the intelli_geo module folder and compile using the following command
        `pbt compile`
6. In QGIS, go to plugins > manage and install plugins. Select the Installed tab. Check the checkbox beside IntelliGeo. Close the plugins manager. You should see the IntelliGeo menu bar in the Plugins menu.