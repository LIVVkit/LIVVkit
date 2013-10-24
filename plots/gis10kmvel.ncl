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
;  PNG         = "/tmp/work/ab3/higher-order/livv_new/plots2/gis10vel"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  velstockcism    = STOCKcism->velnorm(1,1,:,:)

  velstockcism10   = STOCKcism10->velnorm(1,1,:,:)

  velvarblcism    = VARcism->velnorm(1,1,:,:)
  veldiffcism     = new((/279,149/),float);
  veldiffcism     = velvarblcism(:,:)-velstockcism(:,:);

  velvarblcism10   = VARcism10->velnorm(1,1,:,:)
  veldiffcism10    = new((/279,149/),float);
  veldiffcism10    = velvarblcism10(:,:)-velstockcism10(:,:);

  velstockcism@long_name   = "Initial, year 1"
  velvarblcism@long_name   = "Simulation, year 1"
  veldiffcism@long_name    = "Difference"
  velstockcism10@long_name = "Initial, year 1"
  velvarblcism10@long_name = "Simulation, year 1"
  veldiffcism10@long_name  = "Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotvel = new(3,graphic)
  plotvel2 = new(3,graphic)

  res                        = True          ; plot mods desired
  res@cnFillOn               = True          ; turn on color
  res@gsnSpreadColors        = True          ; velse full range of colormap
  res@cnLinesOn              = False         ; turn off contour lines
  res@gsnDraw                = False         ; don't draw
  res@gsnFrame               = False         ; don't advance frame
  res@cnInfoLabelOn          = False         ; turn off cn info label
  res@cnMaxLevelCount        = 8             ; limit number of contours to 8
  res@pmLabelBarDisplayMode  = "Always"      ; enable individual label bars
  res@pmLabelBarSide         = "Bottom"      ; place individual bar below each graph
  res@lbOrientation          = "Horizontal"  ; horizonal label bar
; res@gsnMaximize            = True          ; make as large as possible
  res@vpWidthF               = 0.25          ; change aspect ratio of plot
  res@vpHeightF              = 0.6

  plotvel(0) = gsn_contour(wks,velstockcism,res)
  plotvel(1) = gsn_contour(wks,velvarblcism,res)
  plotvel(2) = gsn_contour(wks,veldiffcism,res)

  plotvel2(0) = gsn_contour(wks,velstockcism10,res)
  plotvel2(1) = gsn_contour(wks,velvarblcism10,res)
  plotvel2(2) = gsn_contour(wks,veldiffcism10,res)

;************************************************
; create panel
;************************************************

  resvel = True                             ; panel resources
  resvel@gsnFrame = False
  resvel@gsnPanelTop = 1.0
  resvel@gsnPanelBottom = 0.53
  resvel@txString = "Velocity Norm"
  resvel@gsnPanelFigureStrings = (/"bench)","cism)"/)   ; add strings to panel

  resvel2 = True                             ; panel resources
  resvel2@gsnFrame = False
  resvel2@gsnPanelTop = 0.49
  resvel2@gsnPanelBottom = 0.08
  resvel2@txString = ""
  resvel2@gsnPanelFigureStrings = (/"bench)","cism10)"/)   ; add strings to panel

  gsn_panel(wks,plotvel,(/1,3/),resvel)
  gsn_panel(wks,plotvel2,(/1,3/),resvel2)
  frame(wks)


end

