
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing
;  STOCKout    = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/ismip-hom-c/80km/data_titan/ishom.c.80km.out.nc","r")
;  STOCKPIC    = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/ismip-hom-c/80km/data_titan/ishom.c.80km.PIC.out.nc","r")
;  STOCKJFNK    = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/ismip-hom-c/80km/data_titan/ishom.c.80km.JFNK.out.nc","r")
;  VARout   = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/ismip-hom-c/80km/data_titan/ishom.c.80km.out.nc","r")
;  VARPIC   = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/ismip-hom-c/80km/data_titan/ishom.c.80km.PIC.out.nc","r")
;  VARJFNK   = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/ismip-hom-c/80km/data_titan/ishom.c.80km.JFNK.out.nc","r")
;  PNG    = "/lustre/atlas/scratch/ab3/cli062/higher-order/livv/plots/ismipcu"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  ustockout    = STOCKout->uvel(0,1,:,:)

  ustockPIC    = STOCKPIC->uvel(0,1,:,:)

  ustockJFNK   = STOCKJFNK->uvel(0,1,:,:)

  uvarblout    = VARout->uvel(0,1,:,:)
  udiffout     = new((/39,39/),float);

  uvarblPIC    = VARPIC->uvel(0,1,:,:)
  udiffPIC     = new((/39,39/),float);
  udiffPIC     = uvarblPIC(:,:)-ustockPIC(:,:);

  uvarblJFNK   = VARJFNK->uvel(0,1,:,:)
  udiffJFNK    = new((/39,39/),float);
  udiffJFNK    = uvarblJFNK(:,:)-ustockJFNK(:,:);

  usout   = ustockout@scale_factor  * ustockout
  usPIC   = ustockPIC@scale_factor  * ustockPIC
  usJFNK  = ustockJFNK@scale_factor * ustockJFNK
  uvout   = uvarblout@scale_factor  * uvarblout
  uvPIC   = uvarblPIC@scale_factor  * uvarblPIC
  uvJFNK  = uvarblJFNK@scale_factor * uvarblJFNK
  udout   = udiffout@scale_factor  * udiffout
  udPIC   = udiffPIC@scale_factor  * udiffPIC
  udJFNK  = udiffJFNK@scale_factor * udiffJFNK
  usout@long_name  = "Serial Scaled Benchmark"
  usPIC@long_name  = "PIC Scaled Benchmark"
  usJFNK@long_name = "JFNK Scaled Benchmark"
  uvout@long_name  = "Serial Scaled Current Run"
  uvPIC@long_name  = "PIC Scaled Current Run"
  uvJFNK@long_name = "JFNK Scaled Current Run"
  udout@long_name  = "Serial Scaled Difference"
  udPIC@long_name  = "PIC Scaled Difference"
  udJFNK@long_name = "JFNK Scaled Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotu = new(3,graphic)
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

  plotu(0) = gsn_contour(wks,usout,res)
  plotu(1) = gsn_contour(wks,uvout,res)
  plotu(2) = gsn_contour(wks,udout,res)

  plotu2(0) = gsn_contour(wks,usPIC,res)
  plotu2(1) = gsn_contour(wks,uvPIC,res)
  plotu2(2) = gsn_contour(wks,udPIC,res)

  plotu3(0) = gsn_contour(wks,usJFNK,res)
  plotu3(1) = gsn_contour(wks,uvJFNK,res)
  plotu3(2) = gsn_contour(wks,udJFNK,res)

;************************************************
; create panel
;************************************************

  resu = True                             ; panel resources
  resu@gsnFrame = False
  resu@gsnPanelTop = 1.0
  resu@gsnPanelBottom = 0.66
  resu@gsnMaximize = True                 ; make as large as possible
  resu@txString    = "U Velocity"    ; title string (make blank to remove)
  resu@gsnPanelFigureStrings = (/"bench)", "current)", "out)"/)   ; add strings to panel

  resu2 = True                             ; panel resources
  resu2@gsnFrame = False
  resu2@gsnPanelTop = 0.64
  resu2@gsnPanelBottom = 0.36
  resu2@txString = ""
  resu2@gsnPanelFigureStrings = (/"bench)", "current)", "PIC)"/)   ; add strings to panel

  resu3 = True                             ; panel resources
  resu3@gsnFrame = False
  resu3@gsnPanelTop = 0.34
  resu3@gsnPanelBottom = 0.00
  resu3@txString = ""
  resu3@gsnPanelFigureStrings = (/"bench)", "current)", "JFNK)"/)   ; add strings to panel

  gsn_panel(wks,plotu,(/1,3/),resu)
  gsn_panel(wks,plotu2,(/1,3/),resu2)
  gsn_panel(wks,plotu3,(/1,3/),resu3)
  frame(wks)

end
