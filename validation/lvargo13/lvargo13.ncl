;*************************************************
; NCL Graphics: lsm_1.ncl
;************************************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file


  e  = model->usrf(0,:,:)
  e@lat2d = model->lat(0,:,:)
  e@lon2d = model->lon(0,:,:)

  caps  = bench->PCT_GLC_GIC(:,:)
  caps@lat2d = bench->LATIXY(:,:)
  caps@lon2d = bench->LONGXY(:,:)
  is  = bench->PCT_GLC_ICESHEET(:,:)
  is@lat2d = bench->LATIXY(:,:)
  is@lon2d = bench->LONGXY(:,:)

  both = caps + is ; sum of both (not including PCT_GLACIER)
  both@lat2d = bench->LATIXY(:,:)
  both@lon2d = bench->LONGXY(:,:)

;  printVarSummary(e)
;  printMinMax(e,True)
;  printVarSummary(caps)
;  printMinMax(caps,True)
;  printVarSummary(is)
;  printMinMax(is,True)

;************************************************
; create plot of elevation data, then an overlay of percent ice sheet/caps data
;************************************************
  wks = gsn_open_wks("png",plotFile)                 ; open a ncgm file
; colors = (/"white","black","white","purple","blue","green","yellow","orange",\
;             "red","white"/)
;  gsn_define_colormap(wks,colors)         ; select color map
  gsn_define_colormap(wks,"prcp_2")         ; select color map
  plot = new(3,graphic)

  res = True                                    ; plot mods desired
  res@gsnDraw = False				; do not draw the plot
  res@gsnFrame = False				; do not advance the frame
  res@tiMainString  	     = "" 		 ; main title blank
  res@gsnSpreadColors      = True               ; make cn span entire color map
  res@mpFillOn             = False              ; turn off gray continents
  res@cnLineLabelsOn        = False
  res@mpProjection         =  "Aitoff"    ; map Projection
  res@mpLimitMode         =  "LatLon"    ; how to zoom in
  res@mpCenterLatF         =  70.
  res@mpCenterLonF         =  -44.
  res@mpMinLonF            = -55                ; set min lon
  res@mpMaxLonF            = -30                ; set max lon
  res@mpMinLatF            =  57.               ; set min lat
  res@mpMaxLatF            =  85.               ; set min lat
  res@mpOutlineOn          =  False             ; turn map outline off
  res@cnLinesOn            = False 		; do not draw contour lines
  res@cnFillOn             = True               ; color fill on
  res@cnFillMode           = "RasterFill"       ; color fill on
  res@cnLineLabelsOn       = False
  res@lbOrientation       = "Vertical"		; make label bar vertical
  res@pmLabelBarOrthogonalPosF = -0.01 		; move label bar closer

; contour levels for the percent
  res@cnLevelSelectionMode = "ExplicitLevels" ; use explicit levels
  res@cnLevels = (/1,5,10,20,30,40,50,60,70,80,90,100 /)            ; set the contour levels
;  res@cnLevels = ispan(10,100,15)             ; set the contour levels

  sres = True                                    ; plot mods desired
  sres@cnFillOn             = False               ; color fill on
  sres@cnLinesOn            = True 		; do not draw contour lines
  sres@cnLineLabelsOn      = False 		; do not draw line labels

; only set if not doing overlay
;  sres@gsnSpreadColors      = True               ; make cn span entire color map
;  sres@mpFillOn             = False              ; turn off gray continents
;  sres@cnFillMode           = "RasterFill"     ; raster plot
;  sres@mpOutlineOn          =  False             ; turn map outline off
;  sres@mpMinLonF            = -70               ; set min lon
;  sres@mpMaxLonF            = -15               ; set max lon
;  sres@mpMinLatF            =  55.               ; set min lat

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

  plotA = gsn_csm_contour_map_overlay(wks,is,e,res,sres)   ; create plot
  plotB = gsn_csm_contour_map_overlay(wks,caps,e,res,sres)   ; create plot
  plotC = gsn_csm_contour_map_overlay(wks,both,e,res,sres)   ; create plot
;  plot2 = gsn_csm_contour(wks, both, cres)   ; create plot
;  plot = gsn_csm_contour_map_ce(wks, e, res)   ; create plot
;  overlay(plot,plot2)
  plot(0) = plotA
  plot(1) = plotB
  plot(2) = plotC

; for paneling
  resP = True
;  resP@gsnMaximize = True 
  gsn_panel(wks,plot,(/1,3/),resP)

  end

   
  
