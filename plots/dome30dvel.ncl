
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing
;  STOCKout   = addfile("/tmp/work/ab3/higher-order/reg_test/bench/dome30/diagnostic/data/dome.out.nc","r")
;  STOCK1     = addfile("/tmp/work/ab3/higher-order/reg_test/bench/dome30/diagnostic/data/dome.1.nc","r")
;  STOCK4     = addfile("/tmp/work/ab3/higher-order/reg_test/bench/dome30/diagnostic/data/dome.4.nc","r")
;  VARout     = addfile("/tmp/work/ab3/higher-order/reg_test/dome30/diagnostic/data/dome.out.nc","r")
;  VAR1       = addfile("/tmp/work/ab3/higher-order/reg_test/dome30/diagnostic/data/dome.1.nc","r")
;  VAR4       = addfile("/tmp/work/ab3/higher-order/reg_test/dome30/diagnostic/data/dome.4.nc","r")
;  PNG        = "/tmp/work/ab3/higher-order/livv_new/plots2/dome30dvel"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  velstockout  = STOCKout->velnorm(0,1,:,:)

  velstock1    = STOCK1->velnorm(0,1,:,:)

  velstock4    = STOCK4->velnorm(0,1,:,:)

  velvarblout  = VARout->velnorm(0,1,:,:)
  veldiffout   = new((/30,30/),float);
  veldiffout   = velvarblout(:,:)-velstockout(:,:);

  velvarbl1    = VAR1->velnorm(0,1,:,:)
  veldiff1     = new((/30,30/),float);
  veldiff1     = velvarbl1(:,:)-velstock1(:,:);

  velvarbl4    = VAR4->velnorm(0,1,:,:)
  veldiff4     = new((/30,30/),float);
  veldiff4     = velvarbl4(:,:)-velstock4(:,:);

  vsout = velstockout@scale_factor * velstockout
  vs1   = velstock1@scale_factor   * velstock1
  vs4   = velstock4@scale_factor   * velstock4
  vvout = velstockout@scale_factor * velvarblout 
  vv1   = velstockout@scale_factor * velvarbl1
  vv4   = velstockout@scale_factor * velvarbl4
  vdout = velstockout@scale_factor * veldiffout
  vd1   = velstock1@scale_factor   * veldiff1
  vd4   = velstock4@scale_factor   * veldiff4
  vsout@long_name  = "Scaled Benchmark"
  vs1@long_name    = "Scaled Benchmark"
  vs4@long_name    = "Scaled Benchmark"
  vvout@long_name  = "Scaled Current Run"
  vv1@long_name    = "Scaled Current Run"
  vv4@long_name    = "Scaled Current Run" 
  vdout@long_name  = "Diff out plot"
  vd1@long_name    = "Diff 1 proc"
  vd4@long_name    = "Diff 4 proc"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap  

  plotvel  = new(3,graphic)
  plotvel2 = new(3,graphic)
  plotvel3 = new(3,graphic)

  res                     = True          ; plot mods desired
  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; use full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label
;  res@gsnMaximize         = True          ; make as large as possible

  plotvel(0) = gsn_contour(wks,vs1,res) 
  plotvel(1) = gsn_contour(wks,vv1,res) 
  plotvel(2) = gsn_contour(wks,vd1,res) 

  plotvel2(0) = gsn_contour(wks,vs4,res) 
  plotvel2(1) = gsn_contour(wks,vv4,res) 
  plotvel2(2) = gsn_contour(wks,vd4,res) 

  plotvel3(0) = gsn_contour(wks,vsout,res)
  plotvel3(1) = gsn_contour(wks,vvout,res)
  plotvel3(2) = gsn_contour(wks,vdout,res) 

;************************************************
; create panel
;************************************************
  
  resvel = True                             ; panel resources
  resvel@gsnFrame = False                 
  resvel@gsnPanelTop = 1.0                 
  resvel@gsnPanelBottom = 0.66                 
  resvel@gsnMaximize = True                 ; make as large as possible
  resvel@txString = "Velocity Norm"   ; title string (make blank to remove)
  resvel@gsnPanelFigureStrings = (/"bench)", "current)", "1)"/)   ; add strings to panel
  
  resvel2 = True
  resvel2@gsnFrame = False 
  resvel2@gsnPanelTop = 0.64
  resvel2@gsnPanelBottom = 0.36
  resvel2@txString = ""
  resvel2@gsnPanelFigureStrings = (/"bench)", "current)", "4)"/)   ; add strings to panel
  
  resvel3 = True
  resvel3@gsnFrame = False
  resvel3@gsnPanelTop = 0.34
  resvel3@PanelBottom = 0.00
  resvel3@txString = ""
  resvel3@gsnPanelFigureStrings = (/"bench)", "current)", "out)"/)
  resvel3@gsnPanelLabelBar = True		; make a common contour bar
  resvel3@lbLabelAngleF = 45			; angle of contour bar labels
  

  gsn_panel(wks,plotvel,(/1,3/),resvel)                  
  gsn_panel(wks,plotvel2,(/1,3/),resvel2)
  gsn_panel(wks,plotvel3,(/1,3/),resvel3)
  frame(wks)


end

