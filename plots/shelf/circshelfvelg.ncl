
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing
;  STOCKGLS     = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/circular-shelf/data/circular-shelf.gnu.glissade.nc","r")
;  VARGLS       = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/circular-shelf/data/circular-shelf.gnu.glissade.nc","r")
;  PNG          = "/lustre/atlas/scratch/ab3/cli062/higher-order/livv/plots/circshelfvel"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  velstockGLS   = STOCKGLS->velnorm(0,1,:,:)

  velvarblGLS   = VARGLS->velnorm(0,1,:,:)
  veldiffGLS    = new((/40,40/),float);
  veldiffGLS    = velvarblGLS(:,:)-velstockGLS(:,:);

  vsGLS  = velstockGLS@scale_factor  * velstockGLS
  vvGLS  = velstockGLS@scale_factor  * velvarblGLS
  vdGLS  = velstockGLS@scale_factor  * veldiffGLS
  vsGLS@long_name    = "Glissade Scaled Benchmark"
  vvGLS@long_name    = "Glissade Scaled Current Run"
  vdGLS@long_name    = "Glissade Scaled Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap
  
  plotvel  = new(3,graphic)
  
  res                        = True          ; plot mods desired
  res@cnFillOn               = True          ; turn on color
  res@gsnSpreadColors        = True          ; use full range of colormap
  res@cnLinesOn              = False         ; turn off contour lines
  res@gsnDraw                = False         ; don't draw
  res@gsnFrame               = False         ; don't advance frame
  res@cnMaxLevelCount        = 8             ; limit number of contours to 8
  res@pmLabelBarDisplayMode  = "Always"      ; enable individual label bars
  res@pmLabelBarSide         = "Bottom"      ; place individual bar below each graph
  res@lbOrientation          = "Horizontal"  ; horizonal label bar
  res@lbAutoManage           = False         ; allow to change label bar font height
  res@lbLabelFontHeightF     = 0.02          ; make font height uniform for all label bars
  res@cnInfoLabelOn          = False         ; turn off cn info label

  plotvel(0) = gsn_contour(wks,vsGLS,res) 
  plotvel(1) = gsn_contour(wks,vvGLS,res)
  plotvel(2) = gsn_contour(wks,vdGLS,res)

;************************************************
; create panel
;************************************************

  resvel = True                             ; panel resources
  resvel@gsnFrame = False                 
  resvel@gsnPanelTop = 1.0
  resvel@gsnPanelBottom = 0.10                 
  resvel@gsnMaximize = True
  resvel@txString    = "Velocity Norm"   ; title string (make blank to remove)
  resvel@gsnPanelFigureStrings = (/"bench)", "current)", "GLS)"/)   ; add strings to panel


  gsn_panel(wks,plotvel,(/1,3/),resvel)
  frame(wks)


end

