===================================================================
   HOW TO WIPE GITHUB AND DEPLOY NEW FILES FROM THIS FOLDER
===================================================================

Follow these steps every time you want to completely replace the 
current files on GitHub with the files currently in this folder.

STEP 1: PREPARE THE FOLDER
-------------------------------------------------------------------
1. Make sure your latest build/files are sitting inside this folder.
2. Ensure you DO NOT delete the hidden ".git" folder if it exists.

STEP 2: OPEN MAC TERMINAL TO THIS FOLDER
-------------------------------------------------------------------
1. Open Mac Terminal.
2. Type "cd " (with a space after it).
3. Drag and drop this folder from Finder directly into the Terminal 
   window, then press Enter.

STEP 3: FIRST-TIME SETUP ONLY (Skip if already done)
-------------------------------------------------------------------
If this folder has never been linked to GitHub before, run these 
commands in order (replace the URL with your actual repo URL):

    git init
    git remote add origin https://github.com/CecileeMcMichen/selfcontrolpatrol.git
    git branch -M main

STEP 4: RUN DEPLOY COMMANDS
-------------------------------------------------------------------
Run these three commands one by one to erase the old repository 
contents on GitHub and push your new files:

1. Stage all changes (tells Git to track deletions and new files):
   git add -A

2. Save your snapshot:
   git commit -m "Wiped old build and uploaded fresh files"

3. Force-push to overwrite GitHub completely:
   git push -f origin main

===================================================================
Done! Refresh your GitHub repository page to see your updated files.
===================================================================
