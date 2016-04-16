[![chat and bugs](https://img.shields.io/badge/chat_and_bugs-more_links_→-brightgreen.svg)](https://github.com/GlPortal/glPortal)
# GlPortal editor
The GlPortal editor allows Blender to import, edit, create and export GlPortal maps.

## Features
- Easy import and export GlPortal maps
- Support for Blender features
- Preview with textures
- Language: English

## Installation
- Install [Blender](http://www.blender.org/download/)
- [Download GlPortal editor.](https://bintray.com/artifact/download/glportal/generic/1.0.0/glportal-editor.zip) *Don’t unzip*.
- Run Blender:
  - Select `File > User Preferences...`
  - Move to the Addons tab.
  - Click `Install From File...` in the bottom of the window.
  - Find the downloaded zip file and select it.
  - Find and check the `GlPortal XML Format` box. Wait a moment for activation to complete.
  - Find and click on right Arrow to display details and preferences.
  - Go to `Set up GlPortal data directory` and find GlPortal data directory.
  - Click `Save User Settings` and close the window.
If you are upgrading, you may need to restart Blender.

## Development
If you want to use the development version of the map editor you can symlink it to your blender plugin directory with the linkExtension software call the linkExtension script with the h option. Or add this path to your script path in the blender settings.
