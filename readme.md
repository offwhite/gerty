

# How it works

- Gerty detects faces. then runs recognition on them.
- if the face is not recognised
  - save the face to unknown
  - if there is enough examples -> run recognition

- Recognition process
  - determine the next id
  - create a dir for that id
  - move all images into that dir
  - run trainer

- Trainer Process
  - load each image from the training pool
  - associate with an id from the dir name
  - run trainer







# Installation

1. install open CV - platform specific
   https://www.learnopencv.com/install-opencv3-on-macos/
