
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing
;  STOCK1     = addfile("/tmp/work/ab3/higher-order/reg_test/bench/dome30/diagnostic/data/dome.1.nc","r")
;  STOCK4     = addfile("/tmp/work/ab3/higher-order/reg_test/bench/dome30/diagnostic/data/dome.4.nc","r")
;  VAR1       = addfile("/tmp/work/ab3/higher-order/reg_test/dome30/diagnostic/data/dome.1.nc","r")
;  VAR4       = addfile("/tmp/work/ab3/higher-order/reg_test/dome30/diagnostic/data/dome.4.nc","r")
;  PNG        = "/tmp/work/ab3/higher-order/livv_new/plots2/dome30dvel"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  velstock1    = STOCK1->velnorm(0,1,:,:)

  velstock4    = STOCK4->velnorm(0,1,:,:)

  velvarbl1    = VAR1->velnorm(0,1,:,:)
  veldiff1     = new((/30,30/),float);
  veldiff1     = velvarbl1(:,:)-velstock1(:,:);

  velvarbl4    = VAR4->velnorm(0,1,:,:)
  veldiff4     = new((/30,30/),float);
  veldiff4     = velvarbl4(:,:)-velstock4(:,:);

  vs1   = velstock1@scale_factor   * velstock1
  vs4   = velstock4@scale_factor   * velstock4
  vv1   = velstock1@scale_factor   * velvarbl1
  vv4   = velstock4@scale_factor   * velvarbl4
  vd1   = velstock1@scale_factor   * veldiff1
  vd4   = velstock4@scale_factor   * veldiff4
  vs1@long_name    = "1 Proc Scaled Benchmark"
  vs4@long_name    = "4 Proc Scaled Benchmark"
  vv1@long_name    = "1 Proc Scaled Current Run"
  vv4@long_name    = "4 Proc Scaled Current Run" 
  vd1@long_name    = "1 Proc Scaled Difference"
  vd4@long_name    = "4 Proc Scaled Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap  

  plotvel  = new(3,graphic)
  plotvel2 = new(3,graphic)

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
; res@gsnMaximize            = True          ; make as large as possible

  plotvel(0) = gsn_contour(wks,vs1,res) 
  plotvel(1) = gsn_contour(wks,vv1,res) 
  plotvel(2) = gsn_contour(wks,vd1,res) 

  plotvel2(0) = gsn_contour(wks,vs4,res) 
  plotvel2(1) = gsn_contour(wks,vv4,res) 
  plotvel2(2) = gsn_contour(wks,vd4,res) 

;************************************************
; create panel
;************************************************
  
  resvel = True                             ; panel resources
  resvel@gsnFrame = False                 
  resvel@gsnPanelTop = 1.0                 
  resvel@gsnPanelBottom = 0.53                 
  resvel@gsnMaximize = True                 ; make as large as possible
  resvel@txString = "Velocity Norm"   ; title string (make blank to remove)
  resvel@gsnPanelFigureStrings = (/"bench)", "current)", "1)"/)   ; add strings to panel
  
  resvel2 = True
  resvel2@gsnFrame = False 
  resvel2@gsnPanelTop = 0.49
  resvel2@gsnPanelBottom = 0.08
  resvel2@txString = ""
  resvel2@gsnPanelFigureStrings = (/"bench)", "current)", "4)"/)   ; add strings to panel
  
  gsn_panel(wks,plotvel,(/1,3/),resvel)                  
  gsn_panel(wks,plotvel2,(/1,3/),resvel2)
  frame(wks)


end

