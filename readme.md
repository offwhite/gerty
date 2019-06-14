

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


### setup virtual environments

# create env
mkvirtualenv gerty-py2 -p python2

# work on env
workon gerty-py2

# stop working on env
source $(which virtualenvwrapper.sh)
deactivate


mkvirtualenv gerty-py3 -p python3
workon gerty-py3

# console
ipython


echo /usr/local/opt/opencv/lib/python2.7/site-packages >> /usr/local/lib/python2.7/site-packages/opencv3.pth

echo /usr/local/opt/opencv/lib/python3.7/site-packages >> /usr/local/lib/python3.7/site-packages/opencv3.pth

find /usr/local/opt/opencv/lib/ -name cv2*.so

# outputs
     /usr/local/opt/opencv/lib//python2.7/site-packages/cv2/python-2.7/cv2.so


cd ~/.virtualenvs/gerty-py2/lib/python2.7/site-packages/
ln -s /usr/local/opt/opencv/lib//python2.7/site-packages/cv2/python-2.7/cv2.so cv2.so

cd ~/.virtualenvs/gerty-py3/lib/python3.7/site-packages/

ln -s /usr/local/opt/opencv/lib/python3.7/site-packages/cv2/python-3.7/cv2.cpython-36m-darwin.so cv2.so
ln -s /usr/local/opt/opencv/lib/python3.7/site-packages/cv2/python-3.7/cv2.cpython-37m-darwin.so cv2.so
