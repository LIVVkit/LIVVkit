
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing
;  STOCKout = addfile("/tmp/work/ab3/higher-order/reg_test/bench/dome30/evolving/data/dome.out.nc","r")
;  STOCK9   = addfile("/tmp/work/ab3/higher-order/reg_test/bench/dome30/evolving/data/dome.9.nc","r")
;  STOCK15  = addfile("/tmp/work/ab3/higher-order/reg_test/bench/dome30/evolving/data/dome.15.nc","r")
;  VARout   = addfile("/tmp/work/ab3/higher-order/reg_test/dome30/evolving/data/dome.out.nc","r")
;  VAR9     = addfile("/tmp/work/ab3/higher-order/reg_test/dome30/evolving/data/dome.9.nc","r")
;  VAR15    = addfile("/tmp/work/ab3/higher-order/reg_test/dome30/evolving/data/dome.15.nc","r")
;  PNG      = "/tmp/work/ab3/higher-order/livv_new/plots2/dome30evel"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  velstock9    = STOCK9->velnorm(10,1,:,:)

  velstock15   = STOCK15->velnorm(10,1,:,:)

  velvarbl9    = VAR9->velnorm(10,1,:,:)
  veldiff9     = new((/30,30/),float);
  veldiff9     = velvarbl9(:,:)-velstock9(:,:);

  velvarbl15   = VAR15->velnorm(10,1,:,:)
  veldiff15    = new((/30,30/),float);
  veldiff15    = velvarbl15(:,:)-velstock15(:,:);

  vs9   = velstock9@scale_factor  * velstock9
  vs15  = velstock15@scale_factor * velstock15
  vv9   = velvarbl9@scale_factor  * velvarbl9
  vv15  = velvarbl15@scale_factor * velvarbl15
  vd9   = veldiff9@scale_factor  * veldiff9
  vd15  = veldiff15@scale_factor * veldiff15
  vs9@long_name    = "9 Proc Scaled Benchmark"
  vs15@long_name   = "15 Proc Scaled Benchmark"
  vv9@long_name    = "9 Proc Scaled Current Run"
  vv15@long_name   = "15 Proc Scaled Current Run"
  vd9@long_name    = "9 Proc Scaled Difference"
  vd15@long_name   = "15 Proc Scaled Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap  

  plotvel  = new(3,graphic)
  plotvel2 = new(3,graphic)
;  plotvel3 = new(2,graphic)

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

  plotvel(0) = gsn_contour(wks,vs9,res) 
  plotvel(1) = gsn_contour(wks,vv9,res) 
  plotvel(2) = gsn_contour(wks,vd9,res) 

  plotvel2(0) = gsn_contour(wks,vs15,res) 
  plotvel2(1) = gsn_contour(wks,vv15,res) 
  plotvel2(2) = gsn_contour(wks,vd15,res) 

;  plotvel3(0) = gsn_contour(wks,vsout,res)
;  plotvel3(1) = gsn_contour(wks,vdout,res)

;************************************************
; create panel
;************************************************
  
  resvel = True                             ; panel resources
  resvel@gsnFrame = False                 
  resvel@gsnPanelTop = 1.0                 
  resvel@gsnPanelBottom = 0.53                 
  resvel@gsnMaximize = True                 ; make as large as possible
  resvel@txString = "Velocity Norm"   ; title string (make blank to remove)
  resvel@gsnPanelFigureStrings = (/"bench)", "current)", "9)"/)   ; add strings to panel
  
  resvel2 = True
  resvel2@gsnFrame = False 
  resvel2@gsnPanelTop = 0.49
  resvel2@gsnPanelBottom = 0.08
  resvel2@txString = ""
  resvel2@gsnPanelFigureStrings = (/"bench)", "current)", "15)"/)   ; add strings to panel
  
;  resvel3 = True
;  resvel3@gsnFrame = False
;  resvel3@gsnPanelTop = 0.34
;  resvel3@PanelBottom = 0.00
;  resvel3@txString = ""
;  resvel3@gsnPanelFigureStrings = (/"bench)","out)"/)
;  resvel3@gsnPanelLabelBar = True		; make a common contour bar
;  resvel3@lbLabelAngleF = 45			; angle of contour bar labels
  resvel@cnLevelSelectionMode = "ManualLevels"     ; set manual contour levels
  resvel@cnLevelSpacingF      = 0.5                  ; contour spacing
  resvel@cnMinLevelValF       = 0.                 ; min level
  resvel@cnMaxLevelValF       =  4.                 ; max level
  

  gsn_panel(wks,plotvel,(/1,3/),resvel)                  
  gsn_panel(wks,plotvel2,(/1,3/),resvel2)
;  gsn_panel(wks,plotvel3,(/1,3/),resvel3)
  frame(wks)

end

