;*************************************************
; NCL Graphics: figure3.ncl
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
;  a = addfile("atm/hist/b.e10.BG20TRCN.f09_g16.002.cam2.h0.1960-07.nc","r")     ; read in data
;  PNG = "/lustre/atlas/scratch/ab3/cli062/higher-order/livv/plots/validation/"

  fsds = a->FSDS(0,:,:)               ; grab the mean downwelling solar flux
  fsds@lat = a->lat(:)
  fsds@lon = a->lon(:)
  fsns = a->FSA(0,:,:)               ; grab the mean net solar flux, absorbed
  fsns@lat = a->lat(:)
  fsns@lon = a->lon(:)
  fsr = a->FSR(0,:,:)               ; grab the mean net solar flux, reflected
  fsr@lat = a->lat(:)
  fsr@lon = a->lon(:)

  albedo = fsr
  albedo@long_name = "Albedo, fsr/fsds"
  albedo = fsr/(where(fsds.ne.0, fsds,fsds@_FillValue))

;  is_mask = a->gris_mask(0,:,:)               ; grab the ice sheet mask
;  is_mask@lat = a->lat(:)
;  is_mask@lon = a->lon(:)

;  f = addfile("/lustre/atlas/scratch/4ue/cli062/CESM-CISM/Greenland_5km_v1.1_SacksRev_c110629.nc","r")
  e  = f->usrf(0,:,:)				; grab the elevation data
  e@lat2d = f->lat(0,:,:)
  e@lon2d = f->lon(0,:,:)

;  fsds_masked = mask(fsds,is_mask,1);
;  fsns_masked = mask(fsns,is_mask,1);

  printVarSummary(fsds)
  printMinMax(fsds,True)
  printVarSummary(fsns)
  printMinMax(fsns,True)
  printVarSummary(fsr)
  printMinMax(fsr,True)
;  printVarSummary(e)
;  printMinMax(e,True)

  printVarSummary(albedo)
  printMinMax(albedo,True)

;************************************************
; create plot of elevation data, then an overlay of percent ice sheet/caps data
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a ncgm file
  gsn_define_colormap(wks,"matlab_jet")         ; select color map
;  gsn_define_colormap(wks,"prcp_2")         ; select color map
  plot = new(3,graphic)

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
  res1@cnLevels = ispan(140,320,10)             ; set the contour levels

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
  res2@cnLevels = (/40,50,70,90,110,130,150,200,250/)            ; set the contour levels

  res3 = True                                    ; plot mods desired
  res3@gsnDraw = False				; do not draw the plot
  res3@gsnFrame = False				; do not advance the frame
  res3@tiMainString  	     = "" 		 ; main title blank
  res3@gsnSpreadColors      = True               ; make cn span entire color map
  res3@mpFillOn             = False              ; turn off gray continents
  res3@cnLineLabelsOn        = False
  res3@mpProjection         =  "Aitoff"    ; map Projection
  res3@mpLimitMode         =  "LatLon"    ; how to zoom in
  res3@mpCenterLatF         =  70.
  res3@mpCenterLonF         =  -44.
  res3@mpMinLonF            = -55                ; set min lon
  res3@mpMaxLonF            = -30                ; set max lon
  res3@mpMinLatF            =  57.               ; set min lat
  res3@mpMaxLatF            =  85.               ; set min lat
  res3@mpOutlineOn          =  False             ; turn map outline off
  res3@cnLinesOn            = False 		; do not draw contour lines
  res3@cnFillOn             = True               ; color fill on
  res3@cnFillMode           = "RasterFill"       ; color fill on
  res3@cnLineLabelsOn       = False
  res3@lbOrientation       = "Vertical"		; make label bar vertical
  res3@pmLabelBarOrthogonalPosF = -0.01 		; move label bar closer
; contour levels for summer
  res3@cnLevelSelectionMode = "ExplicitLevels" ; use explicit levels
  res3@cnLevels = (/0.05,0.25,0.5,0.6,0.7,0.8,0.825,0.85,0.9/)            ; set the contour levels

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

  plotA = gsn_csm_contour_map_overlay(wks,fsds,e,res1,sres)   ; create plot
  plotB = gsn_csm_contour_map_overlay(wks,fsns,e,res2,sres)   ; create plot
  plotC = gsn_csm_contour_map_overlay(wks,albedo,e,res3,sres)   ; create plot
  plot(0) = plotA
  plot(1) = plotB
  plot(2) = plotC

; for paneling
  resP = True
;  resP@gsnMaximize = True 
  gsn_panel(wks,plot,(/1,3/),resP)

  end

   
  
