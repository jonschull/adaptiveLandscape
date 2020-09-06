from landscape4 import makeUnits, initLandscape, sortRect, showLabels
Rows=3
Cols=3
showLabels=False

units = makeUnits(Rows,Cols, showLabels)
initLandscape(  units, Rows, Cols)
sortRect(       units, Rows, Cols)