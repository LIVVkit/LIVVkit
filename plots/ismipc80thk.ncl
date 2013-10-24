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

  tsPIC   = thkstockPIC@scale_factor  * thkstockPIC
  tsJFNK  = thkstockJFNK@scale_factor * thkstockJFNK
  tvPIC   = thkstockPIC@scale_factor  * thkvarblPIC
  tvJFNK  = thkstockJFNK@scale_factor * thkvarblJFNK
  tdPIC   = thkstockPIC@scale_factor  * thkdiffPIC
  tdJFNK  = thkstockJFNK@scale_factor * thkdiffJFNK
  tsPIC@long_name  = "PIC Scaled Benchmark"
  tsJFNK@long_name = "JFNK Scaled Benchmark"
  tvPIC@long_name  = "PIC Scaled Current Run"
  tvJFNK@long_name = "JFNK Scaled Current Run"
  tdPIC@long_name  = "PIC Scaled Difference"
  tdJFNK@long_name = "JFNK Scaled Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotthk = new(3,graphic)
  plotthk2 = new(3,graphic)

  res                        = True          ; plot mods desired
  res@cnFillOn               = True          ; turn on color
  res@gsnSpreadColors        = True          ; tse full range of colormap
  res@cnLinesOn              = False         ; turn off contour lines
  res@gsnDraw                = False         ; don't draw
  res@gsnFrame               = False         ; don't advance frame
  res@cnInfoLabelOn          = False         ; turn off cn info label
  res@cnMaxLevelCount        = 8             ; limit number of contours to 8
  res@pmLabelBarDisplayMode  = "Always"      ; enable individual label bars
  res@pmLabelBarSide         = "Bottom"      ; place individual bar below each graph
  res@lbOrientation          = "Horizontal"  ; horizonal label bar
; res@gsnMaximize            = True          ; make as large as possible

  plotthk(0) = gsn_contour(wks,tsPIC,res)
  plotthk(1) = gsn_contour(wks,tvPIC,res)
  plotthk(2) = gsn_contour(wks,tdPIC,res)

  plotthk2(0) = gsn_contour(wks,tsJFNK,res)
  plotthk2(1) = gsn_contour(wks,tvJFNK,res)
  plotthk2(2) = gsn_contour(wks,tdJFNK,res)

;************************************************
; create panel
;************************************************

  resthk = True                             ; panel resources
  resthk@gsnFrame = False
  resthk@gsnPanelTop = 1.0
  resthk@gsnPanelBottom = 0.53
  resthk@txString = ""
  resthk@txString    = "Thickness"    ; title string (make blank to remove)
  resthk@gsnPanelFigureStrings = (/"bench)", "current)", "PIC)"/)   ; add strings to panel

  resthk2 = True                             ; panel resources
  resthk2@gsnFrame = False
  resthk2@gsnPanelTop = 0.49
  resthk2@gsnPanelBottom = 0.08
  resthk2@txString = ""
  resthk2@gsnPanelFigureStrings = (/"bench)", "current)", "JFNK)"/)   ; add strings to panel

  gsn_panel(wks,plotthk,(/1,3/),resthk)
  gsn_panel(wks,plotthk2,(/1,3/),resthk2)
  frame(wks)


end

