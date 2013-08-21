load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing

;  STOCKout    = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.c.80km.out.nc","r")
;  STOCKPIC    = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.c.80km.PIC.out.nc","r")
;  STOCKJFNK   = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.c.80km.JFNK.out.nc","r")
;  VARout      = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.c.80km.out.nc","r")
;  VARPIC      = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.c.80km.PIC.out.nc","r")
;  VARJFNK     = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.c.80km.JFNK.out.nc","r")
;  PNG         = "/tmp/work/ab3/higher-order/livv_new/plots2/ismipav"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  vstockout    = STOCKout->vvel(0,1,:,:)

  vstockPIC    = STOCKPIC->vvel(0,1,:,:)

  vstockJFNK   = STOCKJFNK->vvel(0,1,:,:)

  vvarblout    = VARout->vvel(0,1,:,:)
  vdiffout     = new((/40,40/),float);
  vdiffout     = vvarblout(:,:)-vstockout(:,:);
  
  vvarblPIC    = VARPIC->vvel(0,1,:,:)
  vdiffPIC     = new((/40,40/),float);
  vdiffPIC     = vvarblPIC(:,:)-vstockPIC(:,:);

  vvarblJFNK   = VARJFNK->vvel(0,1,:,:)
  vdiffJFNK    = new((/40,40/),float);
  vdiffJFNK    = vvarblJFNK(:,:)-vstockJFNK(:,:);

  vsout   = vstockout@scale_factor  * vstockout
  vsPIC   = vstockPIC@scale_factor  * vstockPIC
  vsJFNK  = vstockJFNK@scale_factor * vstockJFNK
  vvout   = vstockout@scale_factor  * vvarblout
  vvPIC   = vstockPIC@scale_factor  * vvarblPIC
  vvJFNK  = vstockJFNK@scale_factor * vvarblJFNK
  vdout   = vstockout@scale_factor  * vdiffout
  vdPIC   = vstockPIC@scale_factor  * vdiffPIC
  vdJFNK  = vstockJFNK@scale_factor * vdiffJFNK
  vsout@long_name  = "Scaled Benchmark"
  vsPIC@long_name  = "Scaled Benchmark"
  vsJFNK@long_name = "Scaled Benchmark"
  vvout@long_name  = "Scaled Current Run"
  vvPIC@long_name  = "Scaled Current Run"
  vvJFNK@long_name = "Scaled Current Run"
  vdout@long_name  = "Diff out plot"
  vdPIC@long_name  = "Diff PIC plot"
  vdJFNK@long_name = "Diff JFNK plot"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotv = new(3,graphic)
  plotv2 = new(3,graphic)
  plotv3 = new(3,graphic)

  res                     = True          ; plot mods desired
  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; use full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label
;  res@gsnMaximize         = True          ; make as large as possible

  plotv(0) = gsn_contour(wks,vsout,res)
  plotv(1) = gsn_contour(wks,vvout,res)
  plotv(2) = gsn_contour(wks,vdout,res)

  plotv2(0) = gsn_contour(wks,vsPIC,res)
  plotv2(1) = gsn_contour(wks,vvPIC,res)
  plotv2(2) = gsn_contour(wks,vdPIC,res)

  plotv3(0) = gsn_contour(wks,vsJFNK,res)
  plotv3(1) = gsn_contour(wks,vvJFNK,res)
  plotv3(2) = gsn_contour(wks,vdJFNK,res)

;************************************************
; create panel
;************************************************

  resv = True                             ; panel resources
  resv@gsnFrame = False
  resv@gsnPanelTop = 1.0
  resv@gsnPanelBottom = 0.66
  resv@gsnMaximize = True                 ; make as large as possible
  resv@txString    = "V Velocity"    ; title string (make blank to remove)
  resv@gsnPanelFigureStrings = (/"bench)", "current)", "out)"/)   ; add strings to panel

  resv2 = True                             ; panel resources
  resv2@gsnFrame = False
  resv2@gsnPanelTop = 0.64
  resv2@gsnPanelBottom = 0.36
  resv2@txString = ""
  resv2@gsnPanelFigureStrings = (/"bench)", "current)", "PIC)"/)   ; add strings to panel

  resv3 = True                             ; panel resources
  resv3@gsnFrame = False
  resv3@gsnPanelTop = 0.34
  resv3@gsnPanelBottom = 0.00
  resv3@txString = ""
  resv3@gsnPanelFigureStrings = (/"bench)", "current)", "JFNK)"/)   ; add strings to panel
  resv3@gsnPanelLabelBar = True            ; make a common contour bar
  resv3@lbLabelAngleF = 45                 ; angle of contour bar labels

  gsn_panel(wks,plotv,(/1,3/),resv)
  gsn_panel(wks,plotv2,(/1,3/),resv2)
  gsn_panel(wks,plotv3,(/1,3/),resv3)
  frame(wks)


end

