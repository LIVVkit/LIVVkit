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
;  PNG         = "/tmp/work/ab3/higher-order/livv_new/plots2/ismipav"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  vstockPIC    = STOCKPIC->vvel(0,1,:,:)

  vstockJFNK   = STOCKJFNK->vvel(0,1,:,:)

  vvarblPIC    = VARPIC->vvel(0,1,:,:)
  vdiffPIC     = new((/39,39/),float);
  vdiffPIC     = vvarblPIC(:,:)-vstockPIC(:,:);

  vvarblJFNK   = VARJFNK->vvel(0,1,:,:)
  vdiffJFNK    = new((/39,39/),float);
  vdiffJFNK    = vvarblJFNK(:,:)-vstockJFNK(:,:);

  vsPIC   = vstockPIC@scale_factor  * vstockPIC
  vsJFNK  = vstockJFNK@scale_factor * vstockJFNK
  vvPIC   = vstockPIC@scale_factor  * vvarblPIC
  vvJFNK  = vstockJFNK@scale_factor * vvarblJFNK
  vdPIC   = vstockPIC@scale_factor  * vdiffPIC
  vdJFNK  = vstockJFNK@scale_factor * vdiffJFNK
  vsPIC@long_name  = "Scaled Benchmark"
  vsJFNK@long_name = "Scaled Benchmark"
  vvPIC@long_name  = "Scaled Current Run"
  vvJFNK@long_name = "Scaled Current Run"
  vdPIC@long_name  = "Diff PIC plot"
  vdJFNK@long_name = "Diff JFNK plot"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotv = new(3,graphic)
  plotv2 = new(3,graphic)
;  plotv3 = new(3,graphic)

  res                     = True          ; plot mods desired
  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; use full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label

  plotv(0) = gsn_contour(wks,vsPIC,res)
  plotv(1) = gsn_contour(wks,vvPIC,res)
  plotv(2) = gsn_contour(wks,vdPIC,res)

  plotv2(0) = gsn_contour(wks,vsJFNK,res)
  plotv2(1) = gsn_contour(wks,vvJFNK,res)
  plotv2(2) = gsn_contour(wks,vdJFNK,res)

;************************************************
; create panel
;************************************************

  resv = True                             ; panel resources
  resv@gsnFrame = False
  resv@gsnPanelTop = 1.00
  resv@gsnPanelBottom = 0.58
  resv@gsnMaximize = True                 ; make as large as possible
  resv@txString = "V Velocity"
  resv@gsnPanelFigureStrings = (/"bench)", "current)", "PIC)"/)   ; add strings to panel

  resv2 = True                             ; panel resources
  resv2@gsnFrame = False
  resv2@gsnPanelTop = 0.57
  resv2@gsnPanelBottom = 0.04
  resv2@txString = ""
  resv2@gsnPanelFigureStrings = (/"bench)", "current)", "JFNK)"/)   ; add strings to panel
  resv2@gsnPanelLabelBar = True            ; make a common contour bar
  resv2@lbLabelAngleF = 45                 ; angle of contour bar labels

  gsn_panel(wks,plotv,(/1,3/),resv)
  gsn_panel(wks,plotv2,(/1,3/),resv2)
  frame(wks)


end

