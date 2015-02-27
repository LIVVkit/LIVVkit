load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing

;  STOCK1    = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/ismip-hom-a/20km/data_titan/ishom.a.20km.glissade.1.nc","r")
;  STOCK4   = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/ismip-hom-a/20km/data_titan/ishom.a.20km.glissade.4.nc","r")
;  VAR1      = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/ismip-hom-a/20km/data_titan/ishom.a.20km.glissade.1.nc","r")
;  VAR4     = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/ismip-hom-a/20km/data_titan/ishom.a.20km.glissade.4.nc","r")
;  PNG         = "/lustre/atlas/scratch/ab3/cli062/higher-order/livv/plots/ismipav"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  vstock1    = STOCK1->vvel(0,1,:,:)

  vstock4   = STOCK4->vvel(0,1,:,:)

  vvarbl1    = VAR1->vvel(0,1,:,:)
  vdiff1     = new((/39,39/),float);

  vvarbl4   = VAR4->vvel(0,1,:,:)
  vdiff4    = new((/39,39/),float);

  vs1   = vstock1@scale_factor  * vstock1
  vs4  = vstock4@scale_factor * vstock4
  vv1   = vvarbl1@scale_factor  * vvarbl1
  vv4  = vvarbl4@scale_factor * vvarbl4
  vd1   = vv1 -vs1
  vd4  = vv4 -vs4

  vs1@long_name  = "1 Proc Benchmark"
  vs4@long_name = "4 Proc Benchmark"
  vv1@long_name  = "1 Proc Current Run"
  vv4@long_name = "4 Proc Current Run"
  vd1@long_name  = "1 Proc Difference"
  vd4@long_name = "4 Proc Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotv = new(3,graphic)
  plotv2 = new(3,graphic)
;  plotv3 = new(3,graphic)

  res                        = True          ; plot mods desired
  res@cnFillOn               = True          ; turn on color
  res@gsnSpreadColors        = True          ; use full range of colormap
  res@cnLinesOn              = False         ; turn off contour lines
  res@gsnDraw                = False         ; don't draw
  res@gsnFrame               = False         ; don't advance frame
  res@cnMaxLevelCount        = 8             ; limit number of contours to 8
  res@pmLabelBarDisplayMode  = "Always"      ; enable individual label bars
  res@pmLabelBarSide         = "Bottom"      ; place individual bar below each graph
  res@lbOrientation          = "Horizontal"  ; horizonal label bar
  res@lbAutoManage           = False         ; allow to change label bar font height
  res@lbLabelFontHeightF     = 0.02          ; make font height uniform for all label bars
  res@cnInfoLabelOn          = False         ; turn off cn info label

  plotv(0) = gsn_contour(wks,vs1,res)
  plotv(1) = gsn_contour(wks,vv1,res)
  plotv(2) = gsn_contour(wks,vd1,res)

  plotv2(0) = gsn_contour(wks,vs4,res)
  plotv2(1) = gsn_contour(wks,vv4,res)
  plotv2(2) = gsn_contour(wks,vd4,res)

;************************************************
; create panel
;************************************************

  resv = True                             ; panel resources
  resv@gsnFrame = False
  resv@gsnPanelTop = 1.00
  resv@gsnPanelBottom = 0.53
  resv@gsnMaximize = True                 ; make as large as possible
  resv@txString = "V Velocity"
  resv@gsnPanelFigureStrings = (/"bench)", "current)", "1)"/)   ; add strings to panel

  resv2 = True                             ; panel resources
  resv2@gsnFrame = False
  resv2@gsnPanelTop = 0.49
  resv2@gsnPanelBottom = 0.08
  resv2@txString = ""
  resv2@gsnPanelFigureStrings = (/"bench)", "current)", "4)"/)   ; add strings to panel

  gsn_panel(wks,plotv,(/1,3/),resv)
  gsn_panel(wks,plotv2,(/1,3/),resv2)
  frame(wks)


end

