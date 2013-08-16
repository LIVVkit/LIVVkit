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
;  PNG         = "/tmp/work/ab3/higher-order/livv_new/plots2/ismipathk"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  thkstockPIC    = STOCKPIC->thk(0,:,:)

  thkstockJFNK   = STOCKJFNK->thk(0,:,:)

  thkvarblPIC    = VARPIC->thk(0,:,:)
  thkdiffPIC     = new((/41,41/),float);
  thkdiffPIC     = thkvarblPIC(:,:)-thkstockPIC(:,:);

  thkvarblJFNK   = VARJFNK->thk(0,:,:)
  thkdiffJFNK    = new((/41,41/),float);
  thkdiffJFNK    = thkvarblJFNK(:,:)-thkstockJFNK(:,:);

  tsPIC   = thkstockPIC@scale_factor * thkstockPIC
  tdPIC   = thkstockPIC@scale_factor * thkdiffPIC
  tsJFNK  = thkstockJFNK@scale_factor * thkstockJFNK
  tdJFNK  = thkstockJFNK@scale_factor * thkdiffJFNK
  tsPIC@long_name  = "Scaled Benchmark"
  tdPIC@long_name  = "Scaled Difference PIC"
  tsJFNK@long_name = "Scaled Benchmark"
  tdJFNK@long_name = "Scaled Difference JFNK"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotthk = new(2,graphic)
  plotthk2 = new(2,graphic)

  res                     = True          ; plot mods desired
  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; tse full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label
;  res@gsnMaximize         = True          ; make as large as possible

  plotthk(0) = gsn_contour(wks,tsPIC,res)
  plotthk(1) = gsn_contour(wks,tdPIC,res)

  plotthk2(0) = gsn_contour(wks,tsJFNK,res)
  plotthk2(1) = gsn_contour(wks,tdJFNK,res)

;************************************************
; create panel
;************************************************

  resthk = True                             ; panel resources
  resthk@gsnFrame = False
  resthk@gsnPanelTop = 1.0
  resthk@gsnPanelBottom = 0.58
  resthk@txString = ""
  resthk@txString    = "Thickness"    ; title string (make blank to remove)
  resthk@gsnPanelFigureStrings = (/"bench)","PIC)"/)   ; add strings to panel

  resthk2 = True                             ; panel resources
  resthk2@gsnFrame = False
  resthk2@gsnPanelTop = 0.57
  resthk2@gsnPanelBottom = 0.04
  resthk2@txString = ""
  resthk2@gsnPanelFigureStrings = (/"bench)","JFNK)"/)   ; add strings to panel
  resthk2@gsnPanelLabelBar = True            ; make a common contour bar
  resthk2@lbLabelAngleF = 45                 ; angle of contour bar labels

  gsn_panel(wks,plotthk,(/1,2/),resthk)
  gsn_panel(wks,plotthk2,(/1,3/),resthk2)
  frame(wks)


end

