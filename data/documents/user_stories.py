from app.models.user_story import UserStory

USER_STORIES = [
    UserStory(
        title="YTD Excel File | Generate Excel Document and Add Button",
        story_url="https://dev.azure.com/Vizientinc/CDBSLA/_boards/board/t/Questers/Stories?System.IterationPath=%40currentIteration&workitem=1266130",
        description=(
            "As a user, I want the system to generate an Excel document containing my YTD data in the approved QA Progress (Tabs Summary and Metric Detail) format so that I can review, share, and analyze the information outside the application.\n\n"
            "As a user, I want an Excel download button on the YTD view so that I can initiate the download of the YTD QA Progress workbook."
        ),
        acceptance_criteria=(
            "AC1 – Generate Excel Document\n"
            "GIVEN the user has initiated the YTD Excel download\n"
            "WHEN the system processes the request\n"
            "THEN the system generates an Excel document containing the user’s YTD data.\n\n"

            "AC2 – Match Approved Excel Template\n"
            "GIVEN the system is generating the Excel document\n"
            "WHEN the document is created\n"
            "THEN its worksheets, columns, headings, layout, and formatting match the provided QAProgress_YTD_MedicareID_CohortShortName.xlsx example.\n\n"

            "AC3 – Populate YTD Data\n"
            "GIVEN the Excel document is being generated\n"
            "WHEN YTD data is available for the user\n"
            "THEN the system populates the applicable fields in the document with the user’s YTD data.\n\n"

            "AC4 – Preserve Data Types and Formatting\n"
            "GIVEN the document contains text, dates, percentages, scores, or numeric values\n"
            "WHEN the data is written to the Excel document\n"
            "THEN each value uses the corresponding data type, number format, and presentation shown in the approved example.\n\n"

            "AC6 – Handle Missing Data\n"
            "GIVEN a field included in the approved template has no corresponding YTD data\n"
            "WHEN the document is generated\n"
            "THEN the field shall be displayed exactly as shown in UI\n\n"

            "AC7 – Create Valid Excel File\n"
            "GIVEN the system has completed document generation\n"
            "WHEN the file is prepared for download\n"
            "THEN the document is a valid .xlsx file that can be opened in supported spreadsheet applications without an error or repair warning.\n\n"

            "AC8 – Apply File Naming Convention\n"
            "GIVEN the Excel document has been generated successfully\n"
            "WHEN it is provided for download\n"
            "THEN the filename follows the approved naming convention based on QAProgress_YTD_MedicareID.xlsx, with the applicable Medicare ID or facility identifier included.\n\n"

            "AC9 - Add hover over for the download icon that displays \"Download Excel\""
        ),
        feature="YTD Excel",
        priority="High",
        status="Active",
    ),
]