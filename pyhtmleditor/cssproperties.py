"""
   CSSProperties:  A data class containing cascading style sheet properties.
   Created by Edward Charles Eberle<eberdeed@eberdeed.net>
   January 2016, San Diego, California 
"""

import os, sys

class CSSProperties:
    cssprops = {"accelerator":None,  "azimuth":None,  "background":None,  "background-attachment":None,  \
        "background-color":None,  "background-image":None,  "background-position":None,  \
        "background-position-x":None,  "background-position-y":None,  \
        "background-repeat":None,  "behavior":None,  "border":None,  \
        "border-bottom":None,  "border-bottom-color":None,  "border-bottom-style":None,  \
        "border-bottom-width":None,  "border-collapse":None,  "border-color":None,  \
        "border-left":None,  "border-left-color":None,  "border-left-style":None,  \
        "border-left-width":None,  "border-right":None,  "border-right-color":None,  \
        "border-right-style":None,  "border-right-width":None,  "border-spacing":None,  \
        "border-style":None,  "border-top":None,  "border-top-color":None,  \
        "border-top-style":None,  "border-top-width":None,  "border-width":None,  \
        "bottom":None,  "caption-side":None,  "clear":None,  "clip":None,  \
        "color":None,  "content":None,  "counter-increment":None,  "counter-reset":None,  \
        "cue":None,  "cue-after":None,  "cue-before":None,  "cursor":None,  \
        "direction":None,  "display":None,  "elevation":None,  "empty-cells":None,  \
        "filter":None,  "float":None,  "font":None,  "font-family":None,  \
        "font-size":None,  "font-size-adjust":None,  "font-stretch":None,  \
        "font-style":None,  "font-variant":None,  "font-weight":None,  \
        "height":None,  "ime-mode":None,  "include-source":None,  "layer-background-color":None,  \
        "layer-background-image":None,  "layout-flow":None,  "layout-grid":None,  \
        "layout-grid-char":None,  "layout-grid-char-spacing":None,  "layout-grid-line":None,  \
        "layout-grid-mode":None,  "layout-grid-type":None,  "left":None,  \
        "letter-spacing":None,  "line-break":None,  "line-height":None,  \
        "list-style":None,  "list-style-image":None,  "list-style-position":None,  \
        "list-style-type":None,  "margin":None,  "margin-bottom":None,  \
        "margin-left":None,  "margin-right":None,  "margin-top":None,  \
        "marker-offset":None,  "marks":None,  "max-height":None,  "max-width":None,  \
        "min-height":None,  "min-width":None,  "-moz-binding":None,  \
        "-moz-border-radius":None,  "-moz-border-radius-topleft":None,  \
        "-moz-border-radius-topright":None,  "-moz-border-radius-bottomright":None,  \
        "-moz-border-radius-bottomleft":None,  "-moz-border-top-colors":None,  \
        "-moz-border-right-colors":None,  "-moz-border-bottom-colors":None,  \
        "-moz-border-left-colors":None,  "-moz-opacity":None,  "-moz-outline":None,  \
        "-moz-outline-color":None,  "-moz-outline-style":None,  "-moz-outline-width":None,  \
        "-moz-user-focus":None,  "-moz-user-input":None,  "-moz-user-modify":None,  \
        "-moz-user-select":None,  "orphans":None,  "outline":None,  "outline-color":None,  \
        "outline-style":None,  "outline-width":None,  "overflow":None,  \
        "overflow-X":None,  "overflow-Y":None,  "padding":None,  "padding-bottom":None,  \
        "padding-left":None,  "padding-right":None,  "padding-top":None,  \
        "page":None,  "page-break-after":None,  "page-break-before":None,  \
        "page-break-inside":None,  "pause":None,  "pause-after":None,  \
        "pause-before":None,  "pitch":None,  "pitch-range":None,  "play-during":None,  \
        "position":None,  "quotes":None,  "-replace":None,  "richness":None,  \
        "right":None,  "ruby-align":None,  "ruby-overhang":None,  "ruby-position":None,  \
        "-set-link-source":None,  "size":None,  "speak":None,  "speak-header":None,  \
        "speak-numeral":None,  "speak-punctuation":None,  "speech-rate":None,  \
        "stress":None,  "scrollbar-arrow-color":None,  "scrollbar-base-color":None,  \
        "scrollbar-dark-shadow-color":None,  "scrollbar-face-color":None,  \
        "scrollbar-highlight-color":None,  "scrollbar-shadow-color":None,  \
        "scrollbar-3d-light-color":None,  "scrollbar-track-color":None,  \
        "table-layout":None,  "text-align":None,  "text-align-last":None,  \
        "text-decoration":None,  "text-indent":None,  "text-justify":None,  \
        "text-overflow":None,  "text-shadow":None,  "text-transform":None,  \
        "text-autospace":None,  "text-kashida-space":None,  "text-underline-position":None,  \
        "top":None,  "unicode-bidi":None,  "-use-link-source":None,  \
        "vertical-align":None,  "visibility":None,  "voice-family":None,  \
        "volume":None,  "white-space":None,  "widows":None,  "width":None,  \
        "word-break":None,  "word-spacing":None,  "word-wrap":None}