load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing

;  STOCKout    = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.a.80km.out.nc","r")
;  STOCKPIC    = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc","r")
;  STOCKJFNK   = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc","r")
;  VARout      = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.a.80km.out.nc","r")
;  VARPIC      = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc","r")
;  VARJFNK     = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc","r")
;  PNG         = "/tmp/work/ab3/higher-order/livv_new/plots2/ismipau"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file


  ustockPIC    = STOCKPIC->uvel(0,1,:,:)

  ustockJFNK   = STOCKJFNK->uvel(0,1,:,:)

  uvarblPIC    = VARPIC->uvel(0,1,:,:)
  udiffPIC     = new((/39,39/),float);
  udiffPIC     = uvarblPIC(:,:)-ustockPIC(:,:);

  uvarblJFNK   = VARJFNK->uvel(0,1,:,:)
  udiffJFNK    = new((/39,39/),float);
  udiffJFNK    = uvarblJFNK(:,:)-ustockJFNK(:,:);

  usPIC   = ustockPIC@scale_factor  * ustockPIC
  usJFNK  = ustockJFNK@scale_factor * ustockJFNK
  uvPIC   = ustockPIC@scale_factor  * uvarblPIC
  uvJFNK  = ustockJFNK@scale_factor * uvarblJFNK
  udPIC   = ustockPIC@scale_factor  * udiffPIC
  udJFNK  = ustockJFNK@scale_factor * udiffJFNK
  usPIC@long_name  = "Scaled Benchmark"
  usJFNK@long_name = "Scaled Benchmark"
  uvPIC@long_name  = "Scaled Current Run"
  uvJFNK@long_name = "Scaled Current Run"
  udPIC@long_name  = "Diff PIC plot"
  udJFNK@long_name = "Diff JFNK plot"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotu = new(3,graphic)
  plotu2 = new(3,graphic)

  res                     = True          ; plot mods desired
  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; use full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label

  plotu(0) = gsn_contour(wks,usPIC,res)
  plotu(1) = gsn_contour(wks,uvPIC,res)
  plotu(2) = gsn_contour(wks,udPIC,res)

  plotu2(0) = gsn_contour(wks,usJFNK,res)
  plotu2(1) = gsn_contour(wks,uvJFNK,res)
  plotu2(2) = gsn_contour(wks,udJFNK,res)

;************************************************
; create panel
;************************************************

  resu = True                             ; panel resources
  resu@gsnFrame = False
  resu@gsnPanelTop = 1.00
  resu@gsnPanelBottom = 0.58
  resu@gsnMaximize = True                 ; make as large as possible
  resu@txString    = "U Velocity"    ; title string (make blank to remove)
  resu@gsnPanelFigureStrings = (/"bench)", "current)", "PIC)"/)   ; add strings to panel

  resu2 = True                             ; panel resources
  resu2@gsnFrame = False
  resu2@gsnPanelTop = 0.57
  resu2@gsnPanelBottom = 0.04
  resu2@txString = ""
  resu2@gsnPanelFigureStrings = (/"bench)", "current)", "JFNK)"/)   ; add strings to panel
  resu2@gsnPanelLabelBar = True            ; make a common contour bar
  resu2@lbLabelAngleF = 45                 ; angle of contour bar labels

  gsn_panel(wks,plotu,(/1,3/),resu)
  gsn_panel(wks,plotu2,(/1,3/),resu2)
  frame(wks)


end

