See how many messages you sent with somebody per day over the existence of your Instagram account. Works on chats that are NOT using end-to-end encryption.

# How to use
1. First, clone this repo on your machine.
2. Get your instagram data .zip file following the instructions in _How to get your data from Instagram_.
3. Extract the zip file to this repo such that there is a directory called `your_instagram_activity` in the root of the repo.
4. Fix the file encoding using `fix_file_formatting.py` by running the file using your python interpreter in your terminal.
5. Prepare chat statistics using `build_statistics.py`
6. Plot all your chats to a graph using `analyze_msgs_per_day.py`
    - You can edit the smoothing amount or which chats are shown using args passed to the `analyze` function.
    - `smoothing` has to be an odd integer. A moving average filter is applied to the data to make the graph more readable.
    - `chat_whitelist` is a list of strings. each string is the name of a chat (same as the name of the directory inside the `statistics` directory)
    - If no whitelist is provided, all chats are included.

## Using the statistics your way

After building the statistics (step 5 in _How to use_), you can analyze the data with your own scripts. Simple functions for loading the chats in Python are in `_load_stats.py`.

# How to get your data from Instagram
1. Open Instagram.
2. Go to "Settings" > "Accounts Center"
3. In Accounts Center go to "Your information and permissions" > "Export your information"
4. Click "Create export" and then "Export to device"
5. Set Format to JSON
6. Set Date range to All time (optional, but recommended)
7. Optionaly select "Customize information" and clear everything except Messages. This could speed up the exporting time.
8. Hit "Start export" and wait to receive an email that your export is ready. This took about an hour in my case, but can vary a lot.
9. Download the .zip file and extract as described in _How to use_ step 3.