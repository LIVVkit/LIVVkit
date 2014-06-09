;*************************************************
; NCL Graphics: figure4.ncl
;************************************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file

;  a = addfile("lnd/hist/b.e10.BG20TRCN.f09_g16.002.clm2.h0.1960-07.nc","r")     ; read in data
; same data from CAM
;  b = addfile("atm/hist/b.e10.BG20TRCN.f09_g16.002.cam2.h0.1960-07.nc","r")     ; read in data
;  PNG = "/lustre/atlas/scratch/ab3/cli062/higher-order/livv/plots/validation/"

  flds = a->FLDS(0,:,:)               ; grab the mean downwelling longwave rad
  flds@lat = a->lat(:)
  flds@lon = a->lon(:)
  flns = a->FIRA(0,:,:)               ; grab the mean net IR longwave rad, absorbed
  flns = -1*flns
  flns@lat = a->lat(:)
  flns@lon = a->lon(:)

;  is_mask = a->gris_mask(0,:,:)               ; grab the ice sheet mask
;  is_mask@lat = a->lat(:)
;  is_mask@lon = a->lon(:)

;  f = addfile("/lustre/atlas/scratch/4ue/cli062/CESM-CISM/Greenland_5km_v1.1_SacksRev_c110629.nc","r")
  e  = f->usrf(0,:,:)				; grab the elevation data
  e@lat2d = f->lat(0,:,:)
  e@lon2d = f->lon(0,:,:)


  printVarSummary(flds)
  printMinMax(flds,True)
  printVarSummary(flns)
  printMinMax(flns,True)
;  printVarSummary(e)
;  printMinMax(e,True)

;************************************************
; create plot of elevation data, then an overlay of percent ice sheet/caps data
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a ncgm file
  gsn_define_colormap(wks,"matlab_jet")         ; select color map
;  gsn_define_colormap(wks,"prcp_2")         ; select color map
  plot = new(2,graphic)

  res1 = True                                    ; plot mods desired
  res1@gsnDraw = False				; do not draw the plot
  res1@gsnFrame = False				; do not advance the frame
  res1@tiMainString  	     = "" 		 ; main title blank
  res1@gsnSpreadColors      = True               ; make cn span entire color map
  res1@mpFillOn             = False              ; turn off gray continents
  res1@cnLineLabelsOn        = False
  res1@mpProjection         =  "Aitoff"    ; map Projection
  res1@mpLimitMode         =  "LatLon"    ; how to zoom in
  res1@mpCenterLatF         =  70.
  res1@mpCenterLonF         =  -44.
  res1@mpMinLonF            = -55                ; set min lon
  res1@mpMaxLonF            = -30                ; set max lon
  res1@mpMinLatF            =  57.               ; set min lat
  res1@mpMaxLatF            =  85.               ; set min lat
  res1@mpOutlineOn          =  False             ; turn map outline off
  res1@cnLinesOn            = False 		; do not draw contour lines
  res1@cnFillOn             = True               ; color fill on
  res1@cnFillMode           = "RasterFill"       ; color fill on
  res1@cnLineLabelsOn       = False
  res1@lbOrientation       = "Vertical"		; make label bar vertical
  res1@pmLabelBarOrthogonalPosF = -0.01 		; move label bar closer
; contour levels for winter
  res1@cnLevelSelectionMode = "ExplicitLevels" ; use explicit levels
  res1@cnLevels = ispan(190,340,10)             ; set the contour levels

  res2 = True                                    ; plot mods desired
  res2@gsnDraw = False				; do not draw the plot
  res2@gsnFrame = False				; do not advance the frame
  res2@tiMainString  	     = "" 		 ; main title blank
  res2@gsnSpreadColors      = True               ; make cn span entire color map
  res2@mpFillOn             = False              ; turn off gray continents
  res2@cnLineLabelsOn        = False
  res2@mpProjection         =  "Aitoff"    ; map Projection
  res2@mpLimitMode         =  "LatLon"    ; how to zoom in
  res2@mpCenterLatF         =  70.
  res2@mpCenterLonF         =  -44.
  res2@mpMinLonF            = -55                ; set min lon
  res2@mpMaxLonF            = -30                ; set max lon
  res2@mpMinLatF            =  57.               ; set min lat
  res2@mpMaxLatF            =  85.               ; set min lat
  res2@mpOutlineOn          =  False             ; turn map outline off
  res2@cnLinesOn            = False 		; do not draw contour lines
  res2@cnFillOn             = True               ; color fill on
  res2@cnFillMode           = "RasterFill"       ; color fill on
  res2@cnLineLabelsOn       = False
  res2@lbOrientation       = "Vertical"		; make label bar vertical
  res2@pmLabelBarOrthogonalPosF = -0.01 		; move label bar closer
; contour levels for summer
  res2@cnLevelSelectionMode = "ExplicitLevels" ; use explicit levels
;  res2@cnLevels = ispan(40,250,4)             ; set the contour levels
  res2@cnLevels = (/-130,-90,-80,-70,-60,-50,-40,-30,-20,-10,30/)            ; set the contour levels

  sres = True                                    ; plot mods desired
  sres@cnFillOn             = False               ; color fill on
  sres@cnLinesOn            = True 		; do not draw contour lines
  sres@cnLineLabelsOn      = False 		; do not draw line labels
  sres@gsnDraw = False				; do not draw the plot
  sres@gsnFrame = False				; do not advance the frame

; contour levels for the elevation data
  sres@cnLevelSelectionMode = "ExplicitLevels"    ; use explicit levels
  sres@cnLevels = (/0,1000,2000,3000/)            ; set the contour levels

;  cres = True                                    ; plot mods desired
;  cres@cnFillOn             = False               ; color fill on
;  cres@cnLinesOn            = False 		; do not draw contour lines
;  cres@cnLineLabelsOn       = False
;  cres@cnLineThicknessF  = 4.                      ; line thickness
;  cres@cnLineDashPattern = 12                      ; dashed lines
;  cres@cnLineColor       = "Blue"                  ; blue contour lines
;  cres@cnLevelSelectionMode = "ExplicitLevels"    ; use explicit levels
;  cres@cnLevels = (/50,100/)            ; set the contour levels

  plotA = gsn_csm_contour_map_overlay(wks,flds,e,res1,sres)   ; create plot
  plotB = gsn_csm_contour_map_overlay(wks,flns,e,res2,sres)   ; create plot
  plot(0) = plotA
  plot(1) = plotB

; for paneling
  resP = True
;  resP@gsnMaximize = True 
  gsn_panel(wks,plot,(/1,2/),resP)

  end

   
  
