
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing
;  STOCKGLS   = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/confined-shelf/data_titan/confined-shelf.gnu.glissade.nc","r")
;  VARGLS     = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/confined-shelf/data_titan/confined-shelf.gnu.glissade.nc","r")
;  PNG        = "/lustre/atlas/scratch/ab3/cli062/higher-order/livv/plots/confshelfthk"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  thkstockGLS   = STOCKGLS->thk(0,:,:)

  thkvarblGLS   = VARGLS->thk(0,:,:);
  thkdiffGLS    = new((/44,43/),float);
  thkdiffGLS    = thkvarblGLS(:,:)-thkstockGLS(:,:);

  tsGLS  = thkstockGLS@scale_factor  * thkstockGLS
  tvGLS  = thkvarblGLS@scale_factor  * thkvarblGLS
  tdGLS  = thkvarblGLS@scale_factor  * thkdiffGLS
  tsGLS@long_name   = "Glissade Scaled Benchmark"
  tvGLS@long_name   = "Glissade Scaled Current Run"
  tdGLS@long_name   = "Glissade Scaled Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap

  plotthk  = new(3,graphic)
  
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

  plotthk(0)  = gsn_contour(wks,tsGLS,res) 
  plotthk(1)  = gsn_contour(wks,tvGLS,res)
  plotthk(2)  = gsn_contour(wks,tdGLS,res)

;************************************************
; create panel
;************************************************

  resthk = True                             ; panel resources
  resthk@gsnFrame = False                 
  resthk@gsnPanelTop = 1.00
  resthk@gsnPanelBottom = 0.53                 
  resthk@gsnMaximize = True
  resthk@txString    = "Thickness"   ; title string (make blank to remove)
  resthk@gsnPanelFigureStrings = (/"bench)", "current)", "GLS)"/)   ; add strings to panel

  gsn_panel(wks,plotthk,(/1,3/),resthk)
  frame(wks)


end
