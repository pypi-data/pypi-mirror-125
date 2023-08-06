# Automated Fibrosis Analysis Toolkit (AFAT)

*This tool was documented in [our paper](http://doi.org/10.1016/j.mex.2019.11.028) on marcophage and fibrosis quantification*

*Hundlab Website: [hundlab.org](http://hundlab.org/)*

*PyPI: [pypi.org/project/hundlab-AFAT](https://pypi.org/project/hundlab-AFAT/)*

*Github: [github.com/hundlab/MAT](https://github.com/hundlab/AFAT)*

## Setup

### Windows

1. Python 3 will need to be installed prior to setting up AFAT, preferably any python
    greater than 3.7. Python 3 can be downloaded from the [python website](http://python.org).
    The x86-64 executable installer is reccommended, as the default install configuration 
    will set python to open .py files by double clicking. If it is installed correctly opening
    cmd or powershell window and typing `py --version` will print the installed python
    version.

2.  Install AFAT by opening a cmd or powershell window and running
    `py -m pip install hundlab-AFAT`, this should install AFAT and all of its dependancies.

3.  Once AFAT has been installed it can be run via cmd, powershell or the start menu. To run
     type `AutomatedFibrosisAnalysisToolkit.py`. To create a desktop shortcut type
     `AutomatedFibrosisAnalysisToolkit.py` into the start menu select `Copy full path`, then on the 
     Desktop `right-click` -> `new` -> `new shortcut` and paste the path when it askes for a
     path.

     If AFAT does not run above as described this means that the python scipts directory has
     not been added to the windows path. To find the install location of python type 
     `py -0p` this will give the location of the python executable. In the same directory
     as python.exe, is a Scripts directory and the `AutomatedFibrosisAnalysisToolkit.py` will
     be in there. Once the AFAT script has been found, a shortcut can be made to it directly
     and placed on the desktop.

After installation, the `ConfigureColorRules.py` tool can be run in the same manner as AFAT.

*Note that it may take a few seconds for AFAT to start.*

### Mac/Linux

1. Python 3 will need to be installed prior to setting up AFAT. Python 3 can be 
    installed via your package manager in linux, or downloaded from python.org for mac.
    If it is installed correctly opening a terminal and typing `python --version` (in some 
    distributions such as Ubuntu the command is `python3`) should start a python prompt. It 
    may also be necessary to install Tkinter. On unbuntu the package is `python3-tk`.

2. Install AFAT using pip: `python -m pip install hundlab-AFAT`

3. To run AFAT use the command `AutomatedFibrosisAnalysisToolkit.py`

After installation, the `ConfigureColorRules.py` tool can be run in the same manner as AFAT.

## Usage

### Version 1.0 

Our paper on AFAT and MAT outline the general usage instructions and processing steps that AFAT uses
to quantify the fibrosis and tissue content in each image. This is still an excellent starting point
for anyone new to using AFAT. Further, see the changes and instructions below for version 2.0.

### Version 2.0

There were two primary aims in updating AFAT:

1. To reduce the memory usage of AFAT. This goal arose from the need to processes more detailed images
   of large sections of tissue as our lab equipment has improved. AFAT now uses around 4Gb of RAM for
   a 500Mb image (8bit color only).

2. To make configuring AFAT more user friendly. To this aim we have added an easier to use interface
   for running simulations that no longer requires editing python files. Further, we have added
   a configuration tool, that allows the color profiles to be retuned to account for differences
   between stainings, or changed entirely to allow for different types of staining altogether.

### Automated Fibrosis Analysis Toolkit

![Image AFAT configure and run](./images/AFAT_configure_run.PNG)

This is the new configuration panel to select all of the inputs needed for AFAT to run the analysis.
First, using `Choose Images` select any images you want to be analyzed in one batch. No special per
batch processing is done, so the results will be equivalent if the images are run separately or in a
batch, however it is likely more convenient to configure the analysis once, and then run it on all the
images of interest. In regards to aim 1 of version 2.0, each image is loaded separately so that
the overall memory usage is minimized. Second, use `Choose Save File` to select an output csv file
to contain all of the results from the analysis (pixel counts from each step and final percentage
stain out of stain and tissue). I typically create a new folder and save the csv file in there, so
that all of the results of the simulation are together in one folder. The next button, 
`Choose Save Directory`, selects the directory where the image files showing the final color
mask for tissue, stain, background and other/unclassified will be saved. In addition to the image
files, new with version 2.0 the settings that were used (including the color profiles) will be saved
in that directory as well.

The color rules file and settings files are the detailed configuration for each analysis. A new tool
for creating your own color rules file will be documented below. Using this file you can change the colors
that AFAT will detect as tissue, stain or background. When an analysis is run, the settings will be saved
(including the color rules) in a `settings.yaml` file. These settings can then be used by a latter analysis
on new images, or to redo the analysis on existing images.

*Note: There is some randomness in the analysis that may result in multiple runs of the same image yeilding
slightly different results.*

The check boxes at the bottom allow for control over what is saved an shown to the user. `Show Images` is not
checked by default, as showing the diagnostic images from each analysis may use a large amount of memory, when
these images can be saved to be viewed latter.

### Configure Color Rules

![Image Configuration menu for color rules](./images/color_rules_configure.PNG)

This is the main configuration menu for customizing the color rules. The configuration uses the HSV colorspace with all values being between 0 and 255. More information on HSV can be found online, but briefly: H refers to
hue, the color; S refers to saturation, the intensity of the color (0 being no color/gray, 255 being intense/rich color); and V is called value, which is also related to color intensity with 0 being black and 255 being intense/rich color. Together S and V define color vs white vs black vs gray. Initially the default rules are loaded
. These rules may be changed and new values may be added by filling in both blanks in for H, S or V. Similarly,
existing rules may be removed by deleting the entries in both blanks. When making changes be sure to deselect
the number entry box for your change to be applied (this will also be reflected in a status update in the
bottom left-hand corner of the window).

![Image Configuration display for color rules](./images/color_rules_view.jpg)

An image may be loaded using the file menu on the main configuration window. The loaded image will show up in
this secondary viewing window with additional information about the color rules. First, the bottom left-hand
status bar displays information on the pixel the mouse is hovering over. Specifically, in the green
highlighted section the HSV values are displayed as well as which category that pixel would be classified
as (using only the color rules and not the full AFAT analysis). This can be helpful for examining the normal
range of colors that different sections of the image take on. It is not necessary that every pixel is
classified by the color rules, but rules should capture the majority of their intended targets without
capturing unintended targets. Sometimes it is not easy to create a rule that excludes all of the undesired
pixels, in which case it may be beneficial to crop or edit out parts of the image prior to analysis. 

In the top right-hand icon bar, highlighted in red, are toggle buttons to show the boundaries of each section
type. These can be useful for finding regions of the image which were not categorized correctly. Note: once
toggled they may use up a relatively large amount of memory.

Once color rules have been defined, they may be saved using the file menu on the main configuration window.

## Advanced Usage

This section details the two settings files used by AFAT: `settings.yaml` and `color_rules.yaml`. While these
two files are show separately, they can be combined into the settings file.

### Settings file

```yaml
###############################################################################
# k neighbors classifier settings
## this is the second pass which attempts to classify pixes missed in the first
## pass into blue, red, or unidentifiable.

#raw settings for KNeighborsClassifier
#see https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html#sklearn.neighbors.KNeighborsClassifier
KNN:
  raw:
    n_neighbors: 5
    n_jobs: -1

# minimum fraction of neighbors with the same label needed to classify a pixel
#default 1 or 100% of neighbors must be the same
  min_consensus: 0.8


# These settins control the maximum number of pixels to be used by KNN
# so if there are more pixels in the image than max_pixels only max_pixel
# number of pixels will be used
  max_pixels: 10_000_000

# The pixels are resampled so that there are fixed fractions of each group
# the fraction of background to be used will be calcuated by 
# 1 - frac_stain - frac_tissue
  frac_stain: 0.375
  frac_tissue: 0.375


###############################################################################
# other settings

# save mask images to a directory
save_images: True

# show image plots
show_images: False

# save settings yaml file with analysis
# will be saved in the same location as the csv data file
save_settings: True
###############################################################################
```

Of primary interest in the settings file is the KNN settings. The `raw` settings
will be passed directly to the KNN constructor and can configure most aspects
of the classifier itself. At the moment, the two options specified are 
`n_neighbors` and `n_jobs`, which control the number of already classified pixels
to be used to classify an unknown/other pixel and the number of threads KNN should
use, respectively. The `min consensus` setting specifies a threshold for the number
of neighbors which must agree in order for the pixel to be classified. (Given that
we are using 5 neighbors the number of agreeing neighbors will be one of 1/5... 5/5).
If consensus is set to 0, then all unknown/other pixels will be classified based
one the plurality of their neighbors.

The `max_pixels` settings controls the maximum number of pixels to be used to train
the KNN. This is set to prevent AFAT from using excessive memory, or computational
time. If the total number of pixels in the image is less than `max_pixels` only that
number of pixels will be used to train the KNN. The `frac_stain` and `frac_tissue`
control the fraction of training pixels which are from each group. White pixels make
up the rest of the training group, frac_white = 1 - frac_stain - frac_tissue. This
means that if there are not enough pixels from a particular group (usually this is
true for the stain group) they will be resampled (duplicated) until enough pixels
are available. Briefly, this is desirable as stain is often underrepresented and
over sampling can help to ensure that unknown pixels have a change of being classified
as stain.

### Color Rules file

```yaml
color_rules:
  background:
    S:
    - - 0
      - 15
    V:
    - - 192
      - 255
  tissue:
    H:
    - - 199
      - 255
    - - 0
      - 50
    S:
    - - 26
      - 255
  stain:
    H:
    - - 148
      - 183
    S:
    - - 40
      - 255
    V:
    - - 0
      - 150

```

Color rules can be specified manually by editing the color rules file. Like when using
the configuration tool, they are specified using ranges in the HSV colorspace.
