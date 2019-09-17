'''
;***********************************************************;
;                                                           ;
;  This script is a example to plot contours on China map.  ;
;  Written by Huang Yongjie(IAP/CAS), 2016-05-22.           ;
;  Convert to Python by YONGJIE HUANG, 2019-02-07.          ;
;                                                           ;
;***********************************************************;
'''
import numpy as np
import Ngl, Nio

#----------------------------------------------------------------------
# This function attaches outlines from the given shapefile to the plot.
#----------------------------------------------------------------------
def add_shapefile_outlines(wks,plot,filename,color="black",ThicknessF=1.0):
#---Read data off shapefile
    f        = Nio.open_file(filename, "r")
    lon      = np.ravel(f.variables["x"][:])
    lat      = np.ravel(f.variables["y"][:])
    
    plres                  = Ngl.Resources()      # resources for polylines
    plres.gsLineColor      = color                # default is black
    plres.gsLineThicknessF = ThicknessF           # default is 1.0
    plres.gsSegments       = f.variables["segments"][:,0]
    
    return Ngl.add_polyline(wks, plot, lon, lat, plres)


#----------------------------------------------------------------------
# Main code
#----------------------------------------------------------------------
# Read variables

f = Nio.open_file("pres.mon.ltm.nc")
pres = f.variables["pres"][0,:,:]
lat  = f.variables["lat"][:]
lon  = f.variables["lon"][:]
#print(pres)

#----------------------------------------------------------------------
wks = Ngl.open_wks("x11","PyNGL_China_boundary") 

Ngl.define_colormap(wks,"gui_default")
  
res                            = Ngl.Resources()
res.nglMaximize                = True
res.nglDraw                    = False
res.nglFrame                   = False

#---------------------------------------------------------------
# set for the map
res.sfXArray                   = lon
res.sfYArray                   = lat

res.mpLimitMode                = "LatLon"
res.mpMinLatF                  = 17.
res.mpMaxLatF                  = 55.
res.mpMinLonF                  = 72.
res.mpMaxLonF                  = 136.
 
#~/anaconda3/envs/ncl_to_python//lib/python3.6/site-packages/ngl/ncarg/database/ 
#res.mpDataSetName              = "Earth..4"
res.mpDataSetName              = "./database/Earth..4"
res.mpDataBaseVersion          = "MediumRes" # or "Ncarg4_1"

res.mpFillOn                   = True
res.mpFillBoundarySets         = "NoBoundaries"
res.mpFillAreaSpecifiers       = ["land","water"]
res.mpSpecifiedFillColors      = ["white","white"]

res.mpAreaMaskingOn            = True
res.mpMaskAreaSpecifiers       = ["China"]

res.mpOutlineBoundarySets      = "NoBoundaries"
res.mpOutlineSpecifiers        = ["China","China:Provinces"]

#res.mpLandFillColor            = "white"
#res.mpOceanFillColor           = "white"
#res.mpInlandWaterFillColor     = "white"
#res.mpNationalLineColor        = "black"
#res.mpProvincialLineColor      = "black"
#res.mpGeophysicalLineColor     = "black"
res.mpNationalLineThicknessF   = 2
res.mpProvincialLineThicknessF = 1

res.mpGridAndLimbOn            = False

#---------------------------------------------------------------
# set for the plot
res.cnFillPalette              = "gui_default"
res.cnFillOn                   = True
res.cnFillDrawOrder            = "PreDraw"
res.cnLinesOn                  = False             
res.cnLineLabelsOn             = False
res.cnLevelSelectionMode       = "ManualLevels"
res.cnMinLevelValF             = 520.
res.cnMaxLevelValF             = 1080.
res.cnLevelSpacingF            = 20.             
#res.nglSpreadColors            = True   
res.lbLabelAutoStride          = True
res.lbLabelFontHeightF         =  0.009
res.lbOrientation              = "horizontal"

res.pmTickMarkDisplayMode      = "Always"

map = Ngl.contour_map(wks,pres,res) 

#-- write Left and Right strings to the plot
vpx  = Ngl.get_float(map,'vpXF')
vpy  = Ngl.get_float(map,'vpYF')
vpw  = Ngl.get_float(map,'vpWidthF')
fnth = Ngl.get_float(map,'tmXBLabelFontHeightF')

txres                          = Ngl.Resources()
txres.txFontHeightF            = fnth

txres.txJust  = "CenterLeft"
Ngl.text_ndc(wks,"Surface pressure over part China Map with SCS",vpx,vpy+0.02,txres)

txres.txJust  = "CenterRight"
Ngl.text_ndc(wks,"hPa",vpx+vpw,vpy+0.02,txres)

#--- add South China Sea --- 
nhres                          = res
nhres.nglMaximize              = False

nhres.vpHeightF                = 0.18    
nhres.vpWidthF                 = 0.18
  
nhres.mpMinLatF                =   2.0    
nhres.mpMaxLatF                =  23.0
nhres.mpMinLonF                = 105.0
nhres.mpMaxLonF                = 123.0

nhres.lbLabelBarOn             = False
nhres.tmXBOn                   = False 
nhres.tmXTOn                   = False
nhres.tmYLOn                   = False
nhres.tmYROn                   = False

map_nanhai = Ngl.contour_map(wks,pres,nhres)

adres                          = Ngl.Resources()
adres.amParallelPosF           = 0.495 # -0.5 is the left edge of the plot.
adres.amOrthogonalPosF         = 0.49  # -0.5 is the top edge of the plot.
adres.amJust                   = "BottomRight"

plotnh = Ngl.add_annotation(map,map_nanhai,adres)

#--- add Yangtze and Yellow rivers --- 
plotrv = add_shapefile_outlines(wks, map, "./cnmap_NetCDF/rivers.nc", "blue", 3.0)

#--- add City --- 
plotct = add_shapefile_outlines(wks, map, "./cnmap_NetCDF/diquJie_polyline.nc", "grey")

Ngl.draw(map)
Ngl.frame(wks)

Ngl.end()
