# Development Instruction

## Run the project on your local machine

1. Clone the project ino the plugins folder of your QGIS
    - To find the path, open QGIS and then go to `Settings > User profiles > Open Active Profile Folder`. The plugin folder is with `python` folder.
2. Create `QGISDIR` environmental variable pointing to the plugins folder.
3. Create a Python environment in your project and activate it in a terminal.
4. Use QT Designer to modify the interface 

    - Open QT designer installed by QGIS
    - Open the `intelli_geo_dockwidget_base.ui`
    
        - Modify
        - Save
5. Compile the interface using `pb_tools`

    - Using pip install the pb_tools

        `pip install pb-tool`

    - Using pip install pyqt5ac

        `pip install pyqt5ac`
    - On linux, due to a [known issue](https://github.com/qgis/QGIS/issues/48368#issuecomment-1293898268), using pip installing qt will introduce some incompatible packages with QT5, therefore, solution is to install use
        ```
        sudo apt-get install python3-pyqt5
        sudo apt-get install qtcreator pyqt5-dev-tools
        sudo apt-get install qttools5-dev-tools
        ```  
    - Check to see if the pb_tool.exe is in the scripts folder of the python environment
    - On the terminal, go the the intelli_geo module folder and compile using the following command
        `pbt compile`
6. In QGIS, go to plugins > manage and install plugins. Select the Installed tab. Check the checkbox beside IntelliGeo. Close the plugins manager. You should see the IntelliGeo menu bar in the Plugins menu.

## Contribute to the project - if you're not part of our team

If you want to contribute to IntelliGeo project, then you need to fork our repo. Since you do not have access to our repository to create a branch, you need to create a copy of the repository into your GitHub account, using fork functionality.

1. On GitHub.com, navigate to the [IntelliGeo repository](https://github.com/MahdiFarnaghi/intelli_geo).

2. In the top-right corner of the page, click Fork. For more information check the [GitHub information page about Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).

![Fork](img/fork.png "Fork")

3. Clone the forked repo from your GitHub account into my hard drive. Work on the project, add functionalities, fix bugs, etc. Then commit the changes to your forked repository on GitHub. 

4. If you want to send the changes to the main IntelliGeo repository, you need to register a *pull request*. On the forked repo (on your GitHub account), click on New pull request. This pull request is sent to the original IntelliGeo repository.

![New pull request](/img/new_pull_request.png "New pull request")

Notice that you can check whether there is a conflict or not, but you cannot merge it. The IntelliGeo team can review the changes and accept/reject the changes.

## Contribute to the project - if you're part of our team

1. In the project folder, pull the main branch.
    `git checkout main`
    `git pull origin main`

2. Check out a new branch.
    `git checkout -b <new_branch_name>`

3. Modify the code and add new features.

4.  Add the chagnes to staged area.
    `git add .`

5. I commit the changes into the local repo.
    `git commit -m "Provide a detailed message"`

6. Push the branch to GitHub so that for review.
    `git push origin <new_branch_name>`

7. Check the GitHub repo. You will see the new branch added. Use the *Compare & pull request* button to compare the changes on this branch with the *main* branch.

![Compare and Pull Request Button](/img/compare_and_pull_request.png "Compare and Pull Request Button").

8. Then, *Open a pull request* window is shown. Write a message, select reviewers, and press the *Create pull request* button.

 ![Open a pull request window](/img/open_pull_request.png "Open a pull request window").

9. Other team members will receive a message. They can see the committed
ed files, write a comment, request for change. At the end, if the team agrees with the changes, they can merge the new branch into the `main` branch using the *Merge pull request* button.  

![Merge pull request button](/img/merge_pull_request.png "Merge pull request button")

10. It is also possible to delete the old branch.


## Develop Roadmap

Known Issues & to-be-discussed

### User Interface
#### Message panel layout

```diff
- ENTER hitting checkbox for sending message.
+ User deletion right (GDPR)
```

### Backend
```diff
! Langchain backend handling empty inupts.
```