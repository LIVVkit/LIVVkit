load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing

;  STOCKcism   = addfile("/tmp/work/ab3/higher-order/reg_test/bench/gis_10km/data/gis_10km.seacism.nc","r")
;  STOCKcism10 = addfile("/tmp/work/ab3/higher-order/reg_test/bench/gis_10km/data/gis_10km.seacism.10.nc","r")
;  STOCKcrop   = addfile("/tmp/work/ab3/higher-order/reg_test/bench/gis_10km/data/gis_10km.051011.crop.nc","r")
;  VARcism     = addfile("/tmp/work/ab3/higher-order/reg_test/gis_10km/data/gis_10km.seacism.nc","r")
;  VARcism10   = addfile("/tmp/work/ab3/higher-order/reg_test/gis_10km/data/gis_10km.seacism.10.nc","r")
;  VARcrop     = addfile("/tmp/work/ab3/higher-order/reg_test/gis_10km/data/gis_10km.051011.crop.nc","r")
;  PNG         = "/tmp/work/ab3/higher-order/livv_new/plots2/gis10kmthk"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  thkstockcism    = STOCKcism->thk(1,:,:)

  thkstockcism10   = STOCKcism10->thk(1,:,:)

  thkstockcrop   = STOCKcrop->thk(1,:,:)
  
  thkvarblcism    = VARcism->thk(1,:,:)
  thkdiffcism     = new((/280,150/),float);
  thkdiffcism     = thkvarblcism(:,:)-thkstockcism(:,:);

  thkvarblcism10   = VARcism10->thk(1,:,:)
  thkdiffcism10    = new((/280,150/),float);
  thkdiffcism10    = thkvarblcism10(:,:)-thkstockcism10(:,:);
  
  thkvarblcrop    = VARcrop->thk(1,:,:)
  thkdiffcrop     = new((/280,150/),float);
  thkdiffcrop     = thkvarblcrop(:,:)-thkstockcrop(:,:);

  thkstockcism@long_name   = "Initial, year 1"
  thkvarblcism@long_name   = "Simulation, year 1"
  thkdiffcism@long_name    = "Difference cism"
  thkstockcism10@long_name = "Initial, year 1"
  thkvarblcism10@long_name = "Simulation, year 1"
  thkdiffcism10@long_name  = "Difference cism10"
  thkstockcrop@long_name   = "Initial, year 1"
  thkvarblcrop@long_name   = "Simulation, year 1"
  thkdiffcrop@long_name    = "Scaled Difference crop"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotthk  = new(3,graphic)
  plotthk2 = new(3,graphic)
  plotthk3 = new(3,graphic)

  res                     = True          ; plot mods desired
  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; tse full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label
;  res@gsnMaximize         = True          ; make as large as possible
  res@vpWidthF            = 0.25           ; change aspect ratio of plot
  res@vpHeightF           = 0.6
  
  plotthk(0) = gsn_contour(wks,thkstockcism,res)
  plotthk(1) = gsn_contour(wks,thkvarblcism,res)
  plotthk(2) = gsn_contour(wks,thkdiffcism,res)

  plotthk2(0) = gsn_contour(wks,thkstockcism10,res)
  plotthk2(1) = gsn_contour(wks,thkvarblcism10,res)
  plotthk2(2) = gsn_contour(wks,thkdiffcism10,res)

  plotthk3(0) = gsn_contour(wks,thkstockcrop,res)
  plotthk3(1) = gsn_contour(wks,thkvarblcrop,res)
  plotthk3(2) = gsn_contour(wks,thkdiffcrop,res)
;************************************************
; create panel
;************************************************

  resthk = True                             ; panel resources
  resthk@gsnFrame = False
  resthk@gsnPanelTop = 1.0
  resthk@gsnPanelBottom = 0.66
  resthk@txString = ""
  resthk@txString    = "Thickness"    ; title string (make blank to remove)
  resthk@gsnPanelFigureStrings = (/"bench)","sim cism)","diff)"/)   ; add strings to panel

  resthk2 = True                             ; panel resources
  resthk2@gsnFrame = False
  resthk2@gsnPanelTop = 0.64
  resthk2@gsnPanelBottom = 0.36
  resthk2@txString = ""
  resthk2@gsnPanelFigureStrings = (/"bench)","sim cism10)","diff)"/)   ; add strings to panel

  resthk3 = True                             ; panel resources
  resthk3@gsnFrame = False
  resthk3@gsnPanelTop = 0.34
  resthk3@gsnPanelBottom = 0.00
  resthk3@txString = ""
  resthk3@gsnPanelFigureStrings = (/"bench)","sim crop)","diff)"/)   ; add strings to panel
  resthk3@gsnPanelLabelBar = True            ; make a common contour bar
  resthk3@lbLabelAngleF = 45                 ; angle of contour bar labels
  

  gsn_panel(wks,plotthk,(/1,3/),resthk)
  gsn_panel(wks,plotthk2,(/1,3/),resthk2)
  gsn_panel(wks,plotthk3,(/1,3/),resthk3)
  frame(wks)


end

