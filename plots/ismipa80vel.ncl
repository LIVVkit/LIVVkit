load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing

;  STOCKPIC    = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc","r")
;  STOCKJFNK   = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc","r")
;  VARPIC      = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc","r")
;  VARJFNK     = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc","r")
;  PNG         = "/tmp/work/ab3/higher-order/livv_new/plots2/ismipavel"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  velstockPIC    = STOCKPIC->velnorm(0,1,:,:)

  velstockJFNK   = STOCKJFNK->velnorm(0,1,:,:)

  velvarblPIC    = VARPIC->velnorm(0,1,:,:)
  veldiffPIC     = new((/40,40/),float);
  veldiffPIC     = velvarblPIC(:,:)-velstockPIC(:,:);

  velvarblJFNK   = VARJFNK->velnorm(0,1,:,:)
  veldiffJFNK    = new((/40,40/),float);
  veldiffJFNK    = velvarblJFNK(:,:)-velstockJFNK(:,:);

  velsPIC   = velstockPIC@scale_factor * velstockPIC
  veldPIC   = velstockPIC@scale_factor * veldiffPIC
  velsJFNK  = velstockJFNK@scale_factor * velstockJFNK
  veldJFNK  = velstockJFNK@scale_factor * veldiffJFNK
  velsPIC@long_name  = "Benchmark"
  veldPIC@long_name  = "Diff PIC plot"
  velsJFNK@long_name = "Benchmark"
  veldJFNK@long_name = "Diff JFNK plot"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotvel = new(2,graphic)
  plotvel2 = new(2,graphic)

  res                     = True          ; plot mods desired
  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; velse full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label
;  res@gsnMaximize         = True          ; make as large as possible

  plotvel(0) = gsn_contour(wks,velsPIC,res)
  plotvel(1) = gsn_contour(wks,veldPIC,res)

  plotvel2(0) = gsn_contour(wks,velsJFNK,res)
  plotvel2(1) = gsn_contour(wks,veldJFNK,res)

;************************************************
; create panel
;************************************************

  resvel = True                             ; panel resources
  resvel@gsnFrame = False
  resvel@gsnPanelTop = 1.0
  resvel@gsnPanelBottom = 0.58
  resvel@txString = "Velocity Norm"
  resvel@gsnPanelFigureStrings = (/"bench)","PIC)"/)   ; add strings to panel

  resvel2 = True                             ; panel resources
  resvel2@gsnFrame = False
  resvel2@gsnPanelTop = 0.57
  resvel2@gsnPanelBottom = 0.04
  resvel2@txString = ""
  resvel2@gsnPanelFigureStrings = (/"bench)","JFNK)"/)   ; add strings to panel
  resvel2@gsnPanelLabelBar = True            ; make a common contour bar
  resvel2@lbLabelAngleF = 45                 ; angle of contour bar labels

  gsn_panel(wks,plotvel,(/1,2/),resvel)
  gsn_panel(wks,plotvel2,(/1,3/),resvel2)
  frame(wks)


end

