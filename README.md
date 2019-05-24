# Calico
Mass replay uploader for the [Ballchasing](Ballchasing.com) replay repository

## Requirements

- Python 3.6+
- ProgressBar Library
- Windows or Mac

## Dependencies and Prerequisites

Calico uses the progressbar library for python to visualize the progress of the replay uploads

To install progressbar:

    pip install progressbar

An authentication key is required to upload replays to [Ballchasing](Ballchasing.com). To obtain an authentication key, visit ballchasing.com/upload while signed in via steam. Once you have an authentication key, create a file (no extension) named auth in the Resources folder and paste the key inside of it.

The folder structure should look like this:

    Calico/Resources/auth

## Interface

| Argument | Value |                        Description                        |                               Default                              | Optional? |
|:--------:|:-----:|:---------------------------------------------------------:|:------------------------------------------------------------------:|:---------:|
|    -p    |  PATH |    The folder path of the set of replays to be uploaded   | C:/Users/%USERNAME%/Documents/My Games/Rocket League/TAGame/Demos/ |    YES    |
|    -v    |  String |             The visibility option of the the replays to be uploaded            |                            "public"                            |    YES    |


## Uploading

This uploader will by default publically upload the entire replay folder located in `C:/Users/%USERNAME%/Documents/My Games/Rocket League/TAGame/Demos/`

To run the script:

    python Ballchasing.py

If you do not want to upload from the default path, you can pass the argument -p followed by the folder path to upload from there instead:

    python Ballchasing.py -p "C:/Users/%USERNAME%/Documents/FolderToUpload"

To change the visibility settings of the replays to be uploaded, pass the argument -v followed by "public", "private", or "unlisted":

    python Ballchasing.py -v "private"

To use a non-default path and non-default visibility:

    python Ballchasing.py -p "C:/Users/%USERNAME%/Documents/FolderToUpload" -v "private"

## Documentation

### Component Descriptions

|        Component        |                                   Description                                   |
|:-----------------------:|:-------------------------------------------------------------------------------:|
|           Main          |                              Initiates the uploader                             |
|         Uploader        |                       Uploads the replays to Ballchasing.com                      |
