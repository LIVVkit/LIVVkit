load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing

;  STOCKPIC    = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.c.80km.PIC.out.nc","r")
;  STOCKJFNK   = addfile("/tmp/work/ab3/higher-order/reg_test/bench/ismip-hom-a/80km/data/ishom.c.80km.JFNK.out.nc","r")
;  VARPIC      = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.c.80km.PIC.out.nc","r")
;  VARJFNK     = addfile("/tmp/work/ab3/higher-order/reg_test/ismip-hom-a/80km/data/ishom.c.80km.JFNK.out.nc","r")
;  PNG         = "/tmp/work/ab3/higher-order/livv_new/plots2/ismipcvel"

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

  velsPIC   = velstockPIC@scale_factor  * velstockPIC
  velsJFNK  = velstockJFNK@scale_factor * velstockJFNK
  velvPIC   = velvarblPIC@scale_factor  * velvarblPIC
  velvJFNK  = velvarblJFNK@scale_factor * velvarblJFNK
  veldPIC   = veldiffPIC@scale_factor  * veldiffPIC
  veldJFNK  = veldiffJFNK@scale_factor * veldiffJFNK
  velsPIC@long_name  = "PIC Scaled Benchmark"
  velsJFNK@long_name = "JFNK Scaled Benchmark"
  velvPIC@long_name  = "PIC Scaled Current Run"
  velvJFNK@long_name = "JFNK Scaled Current Run"
  veldPIC@long_name  = "PIC Scaled Difference"
  veldJFNK@long_name = "JFNK Scaled Difference"

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
  res@lbAutoManage           = False         ; allow to change label bar font height
  res@lbLabelFontHeightF     = 0.02          ; make font height uniform for all label bars
; res@gsnMaximize            = True          ; make as large as possible

  plotvel(0) = gsn_contour(wks,velsPIC,res)
  plotvel(1) = gsn_contour(wks,velvPIC,res)
  plotvel(2) = gsn_contour(wks,veldPIC,res)

  plotvel2(0) = gsn_contour(wks,velsJFNK,res)
  plotvel2(1) = gsn_contour(wks,velvJFNK,res)
  plotvel2(2) = gsn_contour(wks,veldJFNK,res)

;************************************************
; create panel
;************************************************

  resvel = True                             ; panel resources
  resvel@gsnFrame = False
  resvel@gsnPanelTop = 1.0
  resvel@gsnPanelBottom = 0.53
  resvel@txString = "Velocity Norm"
  resvel@gsnPanelFigureStrings = (/"bench)", "current)", "PIC)"/)   ; add strings to panel

  resvel2 = True                             ; panel resources
  resvel2@gsnFrame = False
  resvel2@gsnPanelTop = 0.49
  resvel2@gsnPanelBottom = 0.08
  resvel2@txString = ""
  resvel2@gsnPanelFigureStrings = (/"bench)", "current)", "JFNK)"/)   ; add strings to panel

  gsn_panel(wks,plotvel,(/1,3/),resvel)
  gsn_panel(wks,plotvel2,(/1,3/),resvel2)
  frame(wks)


end

