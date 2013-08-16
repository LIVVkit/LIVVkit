
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
;  PNG      = "/tmp/work/ab3/higher-order/livv_new/plots2/dome30ethk"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  thkstockout  = STOCKout->thk(10,:,:)

  thkstock9    = STOCK9->thk(10,:,:)

  thkstock15   = STOCK15->thk(10,:,:)

  thkvarblout  = VARout->thk(10,:,:);
  thkdiffout   = new((/31,31/),float);
  thkdiffout   = thkvarblout(:,:)-thkstockout(:,:);

  thkvarbl9    = VAR9->thk(10,:,:)
  thkdiff9     = new((/31,31/),float);
  thkdiff9     = thkvarbl9(:,:)-thkstock9(:,:);

  thkvarbl15   = VAR15->thk(10,:,:)
  thkdiff15    = new((/31,31/),float);
  thkdiff15    = thkvarbl15(:,:)-thkstock15(:,:);

  tsout = thkstockout@scale_factor * thkstockout
  ts9   = thkstock9@scale_factor * thkstock9
  ts15  = thkstock15@scale_factor * thkstock15
  tdout = thkstockout@scale_factor * thkdiffout
  td9   = thkstock9@scale_factor * thkdiff9
  td15= thkstock15@scale_factor * thkdiff15
  tsout@long_name  = "Scaled Benchmark"
  ts9@long_name    = "Scaled Benchmark"
  ts15@long_name   = "Scaled Benchmark"
  tdout@long_name  = "Scaled Difference out"
  td9@long_name    = "Scaled Difference 9 proc"
  td15@long_name   = "Scaled Difference 15 proc"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap  

  plotthk  = new(2,graphic)
  plotthk2 = new(2,graphic)
  plotthk3 = new(2,graphic)

  res                     = True          ; plot mods desired
  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; use full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label
;  res@gsnMaximize         = True          ; make as large as possible

  plotthk(0) = gsn_contour(wks,ts9,res) 
  plotthk(1) = gsn_contour(wks,td9,res) 

  plotthk2(0) = gsn_contour(wks,ts15,res) 
  plotthk2(1) = gsn_contour(wks,td15,res) 

  plotthk3(0) = gsn_contour(wks,tsout,res)
  plotthk3(1) = gsn_contour(wks,tdout,res)

;************************************************
; create panel
;************************************************
  
  resthk = True                             ; panel resources
  resthk@gsnFrame = False                 
  resthk@gsnPanelTop = 1.00                 
  resthk@gsnPanelBottom = 0.66                 
  resthk@gsnMaximize = True                 ; make as large as possible
  resthk@txString    = "Thickness"   ; title string (make blank to remove)
  resthk@gsnPanelFigureStrings = (/"bench)","9)"/)   ; add strings to panel

  resthk2 = True
  resthk2@gsnFrame = False
  resthk2@gsnPanelTop = 0.64                 
  resthk2@gsnPanelBottom = 0.36                 
  resthk2@txString   = ""
  resthk2@gsnPanelFigureStrings = (/"bench)","15)"/)   ; add strings to panel
  
  resthk3 = True
  resthk3@gsnFrame = False
  resthk3@gsnPanelTop = 0.34
  resthk3@gsnPanelBottom = 0.00
  resthk3@txString = ""
  resthk3@gsnPanelFigureStrings = (/"bench)","out)"/)
  resthk3@gsnPanelLabelBar = True		; make a common contour bar
  resthk3@lbLabelAngleF = 45			; angle of contour bar labels


  gsn_panel(wks,plotthk,(/1,2/),resthk)                  
  gsn_panel(wks,plotthk2,(/1,2/),resthk2)
  gsn_panel(wks,plotthk3,(/1,3/),resthk3)
  frame(wks)


end

