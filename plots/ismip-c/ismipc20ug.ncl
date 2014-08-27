
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing
;  STOCK1    = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/ismip-hom-c/20km/data_titan/ishom.c.20km.glissade.1.nc","r")
;  STOCK4    = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/ismip-hom-c/20km/data_titan/ishom.c.20km.glissade.4.nc","r")
;  VAR1   = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/ismip-hom-c/20km/data_titan/ishom.c.20km.glissade.1.nc","r")
;  VAR4   = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/ismip-hom-c/20km/data_titan/ishom.c.20km.glissade.4.nc","r")
;  PNG    = "/lustre/atlas/scratch/ab3/cli062/higher-order/livv/plots/ismip-c/ismipc2u"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  ustock1   = STOCK1->uvel(0,1,:,:)

  ustock4   = STOCK4->uvel(0,1,:,:)

  uvarbl1   = VAR1->uvel(0,1,:,:)
  udiff1    = new((/39,39/),float);
  udiff1    = uvarbl1(:,:)-ustock1(:,:);

  uvarbl4   = VAR4->uvel(0,1,:,:)
  udiff4    = new((/39,39/),float);
  udiff4    = uvarbl4(:,:)-ustock4(:,:);

  us1  = ustock1@scale_factor * ustock1
  us4  = ustock4@scale_factor * ustock4
  uv1  = uvarbl1@scale_factor * uvarbl1
  uv4  = uvarbl4@scale_factor * uvarbl4
  ud1  = udiff1@scale_factor * udiff1
  ud4  = udiff4@scale_factor * udiff4
  us1@long_name = "1 Scaled Benchmark"
  us4@long_name = "4 Scaled Benchmark"
  uv1@long_name = "1 Scaled Current Run"
  uv4@long_name = "4 Scaled Current Run"
  ud1@long_name = "1 Scaled Difference"
  ud4@long_name = "4 Scaled Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotu2 = new(3,graphic)
  plotu3 = new(3,graphic)
  
  res                        = True          ; plot mods desired
  res@cnFillOn               = True          ; turn on color
  res@gsnSpreadColors        = True          ; use full range of colormap
  res@cnLinesOn              = False         ; turn off contour lines
  res@gsnDraw                = False         ; don't draw
  res@gsnFrame               = False         ; don't advance frame
  res@cnInfoLabelOn          = False         ; turn off cn info label
  res@cnMaxLevelCount        = 8             ; limit number of contours to 8
  res@pmLabelBarDisplayMode  = "Always"      ; enable individual label bars
  res@pmLabelBarSide         = "Bottom"      ; place individual bar below each graph
  res@lbOrientation          = "Horizontal"  ; horizonal label bar
  res@lbAutoManage           = False         ; allow to change label bar font height
  res@lbLabelFontHeightF     = 0.02          ; make font height uniform for all label bars
; res@gsnMaximize            = True          ; make as large as possible

  plotu2(0) = gsn_contour(wks,us1,res)
  plotu2(1) = gsn_contour(wks,uv1,res)
  plotu2(2) = gsn_contour(wks,ud1,res)

  plotu3(0) = gsn_contour(wks,us4,res)
  plotu3(1) = gsn_contour(wks,uv4,res)
  plotu3(2) = gsn_contour(wks,ud4,res)

;************************************************
; create panel
;************************************************

  resu2 = True                             ; panel resources
  resu2@gsnFrame = False
  resu2@gsnPanelTop = 1.00
  resu2@gsnPanelBottom = 0.53
  resu2@txString = "U Velocity"           ; title string (make blank to remove)
  resu2@gsnPanelFigureStrings = (/"bench)", "current)", "1)"/)   ; add strings to panel

  resu3 = True                             ; panel resources
  resu3@gsnFrame = False
  resu3@gsnPanelTop = 0.49
  resu3@gsnPanelBottom = 0.08
  resu3@txString = ""
  resu3@gsnPanelFigureStrings = (/"bench)", "current)", "4)"/)   ; add strings to panel

  gsn_panel(wks,plotu2,(/1,3/),resu2)
  gsn_panel(wks,plotu3,(/1,3/),resu3)
  frame(wks)

end
