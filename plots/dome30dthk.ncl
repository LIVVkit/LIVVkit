
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
;  PNG        = "/tmp/work/ab3/higher-order/livv_new/plots2/dome30dthk"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  thkstockout  = STOCKout->thk(0,:,:)

  thkstock1    = STOCK1->thk(0,:,:)

  thkstock4    = STOCK4->thk(0,:,:)

  thkvarblout  = VARout->thk(0,:,:);
  thkdiffout   = new((/31,31/),float);
  thkdiffout   = thkvarblout(:,:)-thkstockout(:,:);

  thkvarbl1    = VAR1->thk(0,:,:)
  thkdiff1     = new((/31,31/),float);
  thkdiff1     = thkvarbl1(:,:)-thkstock1(:,:);

  thkvarbl4    = VAR4->thk(0,:,:)
  thkdiff4     = new((/31,31/),float);
  thkdiff4     = thkvarbl4(:,:)-thkstock4(:,:);

  tsout = thkstockout@scale_factor * thkstockout
  ts1   = thkstock1@scale_factor   * thkstock1
  ts4   = thkstock4@scale_factor   * thkstock4
  tvout = thkstockout@scale_factor * thkvarblout
  tv1   = thkstock1@scale_factor   * thkvarbl1
  tv4   = thkstock4@scale_factor   * thkvarbl4
  tdout = thkstockout@scale_factor * thkdiffout
  td1   = thkstock1@scale_factor   * thkdiff1
  td4   = thkstock4@scale_factor   * thkdiff4
  tsout@long_name  = "Serial Scaled Benchmark"
  ts1@long_name    = "1 Proc Scaled Benchmark"
  ts4@long_name    = "4 Proc Scaled Benchmark"
  tvout@long_name  = "Serial Scaled Current Run"
  tv1@long_name    = "1 Proc Scaled Current Run"
  tv4@long_name    = "4 Proc Scaled Current Run"
  tdout@long_name  = "Serial Scaled Difference"
  td1@long_name    = "1 Proc Scaled Difference"
  td4@long_name    = "4 Proc Scaled Difference"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap  

  plotthk  = new(3,graphic)
  plotthk2 = new(3,graphic)
  plotthk3 = new(3,graphic)

  res                     = True          ; plot mods desired
  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; use full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label
;  res@gsnMaximize         = True          ; make as large as possible

  plotthk(0) = gsn_contour(wks,ts1,res) 
  plotthk(1) = gsn_contour(wks,tv1,res) 
  plotthk(2) = gsn_contour(wks,td1,res)

  plotthk2(0) = gsn_contour(wks,ts4,res) 
  plotthk2(1) = gsn_contour(wks,tv4,res) 
  plotthk2(2) = gsn_contour(wks,td4,res)

  plotthk3(0) = gsn_contour(wks,tsout,res)
  plotthk3(1) = gsn_contour(wks,tvout,res)
  plotthk3(2) = gsn_contour(wks,tdout,res)

;************************************************
; create panel
;************************************************
  
  resthk = True                             ; panel resources
  resthk@gsnFrame = False                 
  resthk@gsnPanelTop = 1.00                 
  resthk@gsnPanelBottom = 0.66                 
  resthk@gsnMaximize = True                 ; make as large as possible
  resthk@txString    = "Thickness"   ; title string (make blank to remove)
  resthk@gsnPanelFigureStrings = (/"bench)", "current)", "1)"/)   ; add strings to panel

  resthk2 = True
  resthk2@gsnFrame = False
  resthk2@gsnPanelTop = 0.64                 
  resthk2@gsnPanelBottom = 0.36                 
  resthk2@txString   = ""
  resthk2@gsnPanelFigureStrings = (/"bench)", "current)", "4)"/)   ; add strings to panel
  
  resthk3 = True
  resthk3@gsnFrame = False
  resthk3@gsnPanelTop = 0.34
  resthk3@gsnPanelBottom = 0.00
  resthk3@txString = ""
  resthk3@gsnPanelFigureStrings = (/"bench)", "current)", "out)"/)
  resthk3@gsnPanelLabelBar = True		; make a common contour bar
  resthk3@lbLabelAngleF = 45			; angle of contour bar labels


  gsn_panel(wks,plotthk,(/1,3/),resthk)                  
  gsn_panel(wks,plotthk2,(/1,3/),resthk2)
  gsn_panel(wks,plotthk3,(/1,3/),resthk3)
  frame(wks)


end

