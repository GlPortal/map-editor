[![Download](https://img.shields.io/badge/download-latest_release-brightgreen.svg)](https://github.com/GlPortal/map-editor/releases/)
[![Build Status](https://travis-ci.org/GlPortal/map-editor.svg?branch=master)](https://travis-ci.org/GlPortal/map-editor)
[![Join the chat at https://gitter.im/GlPortal/glPortal](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/GlPortal/glPortal?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Join Chat](https://img.shields.io/badge/irc-join_chat-brightgreen.svg)](http://webchat.freenode.net/?channels=%23%23glportal&uio=d4)

# Radix Map Editor Blender Plugin
The Radix Map Editor Plugin allows Blender to import, edit, create and export Radix maps.

## Features
- Import and export Radix maps
- Radix specific tool panels
- Preview with textures

## Installation
- Install [Blender](http://www.blender.org/download/)
- [Download the latest version](https://github.com/GlPortal/map-editor/releases/) of the Radix editor. *Don’t extract the file* !
- Run Blender:
  - Select `File > User Preferences...`
  - Move to the Addons tab.
  - Click `Install From File...` in the bottom of the window.
  - Select the downloaded zip file.
  - Check the `GlPortal XML Format` box. Wait a moment for activation to complete.
  - Click on the arrow to display details and preferences.
  - Go to `Set up GlPortal data directory` and find GlPortal data directory.
  - Click `Save User Settings` and close the window.
If you are upgrading, you may need to restart Blender.

## Development
-   Install Blender
-   Clone or download this repository
-   To install the plugin either
    -   Copy the directory `RadixMapEditor` into your Blender configuration folder `/home/user/.config/blender/VERSION/scripts/addons`
    -   Use the `linkExtension` script to create a link of the plugin to the Blender extension folder
-   Run Blender:
    -  Open the Blender settings
    -  Check the `GlPortal XML Format` box. Wait a moment for activation to complete.
    -  Click on right arrow to display details and preferences.
    -  Go to `Set up GlPortal data directory` and select your GlPortal data directory.
    -  Go to `Set up GlPortal executable` and find GlPortal executable.
    -  Click `Save User Settings` and close the window. If you are upgrading, you may need to restart Blender.


## Usage of linkExtension

Open terminal in the main repository directory and type:

```
./linkExtension -b blender_version
```

Where the `blender_version` is replaced with your installed Blender version.

### Example
```
./linkExtension -b 2.79
```

## Create a Release
On Linux you can create a release very easily:
```
./draftRelease
```

You can then upload the release to github.
