load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing

;  STOCK1    = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/ismip-hom-a/80km/data_titan/ishom.a.80km.glissade.1.nc","r")
;  STOCK4   = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/bench/ismip-hom-a/80km/data_titan/ishom.a.80km.glissade.4.nc","r")
;  VAR1      = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/ismip-hom-a/80km/data_titan/ishom.a.80km.glissade.1.nc","r")
;  VAR4     = addfile("/lustre/atlas/scratch/ab3/cli062/higher-order/reg_test/ismip-hom-a/80km/data_titan/ishom.a.80km.glissade.4.nc","r")
;  PNG         = "/lustre/atlas/scratch/ab3/cli062/higher-order/livv/plots/ismipathk"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  thkstock1    = STOCK1->thk(0,:,:)

  thkstock4   = STOCK4->thk(0,:,:)

  thkvarbl1    = VAR1->thk(0,:,:)
  thkdiff1     = new((/40,40/),float);
  thkdiff1     = thkvarbl1(:,:)-thkstock1(:,:);

  thkvarbl4   = VAR4->thk(0,:,:)
  thkdiff4    = new((/40,40/),float);
  thkdiff4    = thkvarbl4(:,:)-thkstock4(:,:);

  ts1   = thkstock1@scale_factor  * thkstock1
  ts4  = thkstock4@scale_factor * thkstock4
  tv1   = thkstock1@scale_factor  * thkvarbl1
  tv4  = thkstock4@scale_factor * thkvarbl4
  td1   = thkstock1@scale_factor  * thkdiff1
  td4  = thkstock4@scale_factor * thkdiff4
  ts1@long_name  = "1 Scaled Benchmark"
  ts4@long_name = "4 Scaled Benchmark"
  tv1@long_name  = "1 Scaled Current Run"
  tv4@long_name = "4 Scaled Current Run"
  td1@long_name  = "1 Scaled Difference"
  td4@long_name = "4 Scaled Difference"

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
  res@lbAutoManage           = False         ; allow to change label bar font height
  res@lbLabelFontHeightF     = 0.02          ; make font height uniform for all label bars
; res@gsnMaximize            = True          ; make as large as possible

  plotthk(0) = gsn_contour(wks,ts1,res)
  plotthk(1) = gsn_contour(wks,tv1,res)
  plotthk(2) = gsn_contour(wks,td1,res)

  plotthk2(0) = gsn_contour(wks,ts4,res)
  plotthk2(1) = gsn_contour(wks,tv4,res)
  plotthk2(2) = gsn_contour(wks,td4,res)

;************************************************
; create panel
;************************************************

  resthk = True                             ; panel resources
  resthk@gsnFrame = False
  resthk@gsnPanelTop = 1.0
  resthk@gsnPanelBottom = 0.53
  resthk@txString = ""
  resthk@txString    = "Thickness"    ; title string (make blank to remove)
  resthk@gsnPanelFigureStrings = (/"bench)", "current)", "1)"/)   ; add strings to panel

  resthk2 = True                             ; panel resources
  resthk2@gsnFrame = False
  resthk2@gsnPanelTop = 0.49
  resthk2@gsnPanelBottom = 0.08
  resthk2@txString = ""
  resthk2@gsnPanelFigureStrings = (/"bench)", "current)", "4)"/)   ; add strings to panel

  gsn_panel(wks,plotthk,(/1,3/),resthk)
  gsn_panel(wks,plotthk2,(/1,3/),resthk2)
  frame(wks)


end

