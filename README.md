# FRC Scouting Generator
The FRC Scouting Generator is a tool developed originally for team 5948 to automate the creation of the spreadsheet used for scouting. Since every year the competition changes, it is not possible to use the same template for each year, though it does stay similar in many aspects. Plus, there is a lot of "busy" work, like filling out the teams and the schedule. With this application you can generate a Google Sheets spreadsheet that lives in your Google Drive that can be easily shared with the rest of the team. Thanks to the [Google Sheets API](https://developers.google.com/sheets/api/reference/rest), you can create a spreadsheet for each event your team attends within seconds. With the help of [The Blue Alliance API](https://www.thebluealliance.com/apidocs/v3) and the [Statbotics API](https://www.statbotics.io/api/rest), you will automatically get advanced statistics on each team present in the competition, with which you can pretty accurately predict performance. However, your are not restricted to these stats. The main customizability comes from the 'Quals' sheet, where you can specify the observations you will be looking for in each team, so that your team can also manually scout with ease. Combining all the information collected through manual scouting and the advanced stats, you should be able to have a great idea of the performance and the potential of each team, being useful when picking alliances but also when trying to outplay your oponents.

## Use
Download the latest release and extract the folder. Before running the executable, you are going to need to set up the Google Sheets API and The Blue Alliance API.

For the Google Sheets API, you need to setup a Google Cloud Project with access to the Google Sheets API. Create a new project [here](https://console.cloud.google.com/projectcreate); enable the Google Sheets API; configure the OAuth consent screen: add the Google Sheets API scope (/auth/spreadsheets) and add the email of whoever is going to use the app as a 'Test user' (there can be multiple); create the credentials for a OAuth client ID for a desktop application; download the JSON with the credentials, rename the file to credentials.json and move it to the root of the '_internal' folder you unzipped.

A more detailed tutorial on how to create the necessary Google Cloud Project can be found [here](https://developers.google.com/sheets/api/quickstart/python)

For The Blue Alliance API, get an API token [here](https://www.thebluealliance.com/account) by adding a new key in the 'Read API Keys' section (the name does not matter). When you run the exectuable, you will need the X-TBA-Auth-Key that it gives you when creating the key.

Run 'Scouting_Generator.exe', read and fill out the prompts according to your needs, and click the button at the bottom that says "Create and Save". It is recommended to start by using one of the templates that are offered. If you wish to save your configuration without creating a spreadsheet you can also just click "Save". Next time you open the app it will prompt you if you want to recover the previous session, along with the predefined templates.

Once a spreadsheet has been created, you can update it anytime. If you erased a sheet, if you never created it in the first place, or if you wish to update the content in it, just include the URL for the spreadsheet inside the configuration and indicate which sheets you wish to update/create. The main use of this would be to update the statistics retrieved from Statbotics and The Blue Alliance. This is done by updating the 'Advanced Stats' sheet.

After a week of the executable being run you may get an error saying something about an expiry or not being able to refresh the token. To fix this you need to erase the file '_internal/token.json'. When you open the application again the Google pop up of the Cloud Project will show up again. This happens because the token file that acts as your credentials for the Google Sheets API expires after 7 days in some cases.

## Sheets
Descriptions for all of the sheets that are available for creation. It is not necessary to create every one, but it is recommended.

- Teams: Only sheet that is absolutely necessary. It stores the names, numbers, and schools of the teams that are attending the event. You can fill out the 'Scout' column ('Responsable' in Spanish) with the names of the people responsable for manually scouting each team. This becomes especially useful in tandem with the 'Scouting' sheet.
- Match Order: Gives you the list of all the qualification matches and the teams that play in them, provided by the data of The Blue Alliance. It also shows the 'expected' time each match will start, though they often get a bit delayed. You can specify the timezone for this schedule, or you can leave it as the default, which will use the timezone provided by FRC (usually the correct timezone for where the event is taking place).
- Scouting: You can choose a specific match from a dropdown menu at the top. It will show you the teams that are playing in the chosen match, the alliances, and the scout responsable for each team, if you filled it in the 'Teams' sheet.
- Quals: The most customizable sheet. It is used exclusively for the manual scouting and should be filled out by the team members as the competition goes on. You can choose the observations you want to scout. This is the sheet that needs to be updated from season to season to reflect the changes in the competition and the things you are scouting. There are 4 different types of observations you can choose from. 'Every Match' is used to count numerical values in each match, normally used with number of game pieces scored, for example; 'Options' is to create a single column, each cell with a dropdown menu with the options you set; 'Yes or No' is the same as 'Options' but the options are just preset as 'Yes' or 'No', as the name suggests; 'Paragraph/Note' is a single empty column, you can use it however you want, though the most common use case would be to add notes or comments.
- Advanced Stats: Sheet where the statistics provided by Statbotics (EPA) and by The Blue Alliance (OPR, DPR, CCWM) live. It is necessary for the next two sheets to work. It is preferrable that nothing is changed here. You can update this sheet through the app as the competition goes on to have up-to-date data. Please don't abuse the 'Update Sheet' mechanic, though. API calls are not free for the people running the servers.
- Ranking: The sheet to use when making decisions on who to pick as an alliance member. All the important advanced and manually scouted statistics are here in one, convenient sheet. You can sort and filter the teams with the filter icon at the top of each column. The statistics are assigned a gradient; green means good and red means bad. To signify that a team is no longer available, erase the corresponding cell (it should say TRUE by default) in the last column 'Available'. This will grey-out the team to very easily see which teams are available and which are not.
- Compare: It shows the same statistics as the 'Ranking' sheet. However, you can add up to 3 teams to compare them. To add or change the teams shown just change the team number at the top (there is a dropdown menu to help). You will have the statistics side to side, and, in the case of the advanced stats, there is a graph to see the differences more visually.

## Example Spreadsheets
Opening the application for the first time you will find a prompt asking if you want to use some templates. If you were to click the corresponding option and create without changing anything else, you would get the following spreadsheets. They are available as examples.

- [English template example](https://docs.google.com/spreadsheets/d/11K-1oVin5HfTjDxt1L_8-VlmY1GssvZ1t-bzX-c4T5Q/edit?usp=sharing)
- [Spanish template example](https://docs.google.com/spreadsheets/d/1fK7XMPbOH0kVruFoO_5L4ssx_yM2mSrTmDVQkCVQC3E/edit?usp=sharing)


## Contributing
To run the code you will need to download all the libraries in the requirements.txt.

```shell
pip install -r requirements.txt
```

It is recommended to use a Virtual Environment. The version of Python used in the project was 3.11.8.

```shell
python -m venv /path/to/new/virtual/environment
```

You will also need to set up the Google Cloud Project. The instructions for that are found [here](#use). Move the credentials.json file to the root of this folder.

To run the GUI_main.py file (which is the one that creates the GUI app), you need to be inside the 'src' folder.

If you wish to contribute, please contact me through GitHub or email.

Thank you for your interest!