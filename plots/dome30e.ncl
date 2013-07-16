
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************

; stand alone read in for testing
;  STOCK    = addfile("/global/scratch/sd/evanskj/higher-order/reg_test/dome30/evolving/bench/dome.out.nc","r")
;  VAR9    = addfile("/global/scratch/sd/evanskj/higher-order/reg_test/dome30/evolving/data/dome.9.nc","r")
;  VAR15    = addfile("/global/scratch/sd/evanskj/higher-order/reg_test/dome30/evolving/data/dome.15.nc","r")
;  PNG    = "/global/scratch/sd/evanskj/higher-order/livv/plots/dome30e"

;************************************************
; create plots
;************************************************
  wks = gsn_open_wks("png",PNG)                 ; open a png file

  velstock   = STOCK->velnorm(10,1,:,:)
  thkstock   = STOCK->thk(10,:,:)
  tmpstock   = STOCK->tempstag(10,2,:,:)

  velvarbl  = VAR9->velnorm(10,1,:,:)
  veldiff9 = new((/30,30/),float);
  veldiff9 = velvarbl(:,:)-velstock(:,:);

  velvarbl  = VAR15->velnorm(10,1,:,:)
  veldiff15 = new((/30,30/),float);
  veldiff15 = velvarbl(:,:)-velstock(:,:);

  thkvarbl  = VAR9->thk(10,:,:)
  thkdiff9 = new((/31,31/),float);
  thkdiff9 = thkvarbl(:,:)-thkstock(:,:);

  thkvarbl  = VAR15->thk(10,:,:)
  thkdiff15 = new((/31,31/),float);
  thkdiff15 = thkvarbl(:,:)-thkstock(:,:);

  tmpvarbl  = VAR9->tempstag(10,1,:,:)
  tmpdiff9 = new((/31,31/),float);
  tmpdiff9 = tmpvarbl(:,:)-tmpstock(:,:);

  tmpvarbl  = VAR15->tempstag(10,1,:,:)
  tmpdiff15 = new((/31,31/),float);
  tmpdiff15 = tmpvarbl(:,:)-tmpstock(:,:);

;  maxv1=max(velstock(:,:));
;  maxv1=max(velstock(:,:));
;  maxv1=max(velstock(:,:));
;  print(maxv1);
;  printVarSummary(velstock)
;  maxv50=max(velvarbl(:,:));
;  print(maxv50);
;  printVarSummary(velvarbl);

  vs= velstock@scale_factor * velstock
  vd9= velstock@scale_factor * veldiff9
  vd15= velstock@scale_factor * veldiff15
  vs@long_name   = "Benchmark"
  vd9@long_name   = "Diff 9 proc"
  vd15@long_name  = "Diff 15 proc"

  ts= thkstock@scale_factor * thkstock
  td9= thkstock@scale_factor * thkdiff9
  td15= thkstock@scale_factor * thkdiff15
  ts@long_name   = "Scaled Benchmark"
  td9@long_name   = "Scaled Difference 9 proc"
  td15@long_name  = "Scaled Difference 15 proc"

;  tmpstock@long_name   = "Benchmark"
;  tmpdiff9@long_name   = "Difference 9 proc"
;  tmpdiff15@long_name  = "Difference 15 proc"

;************************************************
; create plots
;************************************************

  wks = gsn_open_wks("png",PNG)            ; open a png file
  gsn_define_colormap(wks,"wgne15")        ; choose a colormap
  plotvel = new(3,graphic)
  plotthk = new(3,graphic)
;  plottmp = new(3,graphic)
  
  res                     = True          ; plot mods desired

  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; use full range of colormap
  res@cnLinesOn           = False         ; turn off contour lines
  res@gsnDraw             = False         ; don't draw
  res@gsnFrame            = False         ; don't advance frame
  res@cnLinesOn           = False         ; turn off contour lines
  res@cnInfoLabelOn       = False         ; turn off cn info label
;  res@gsnMaximize         = True          ; make as large as possible

  plotvel(0) = gsn_contour(wks,vs,res) 
  plotvel(1) = gsn_contour(wks,vd9,res) 
  plotvel(2) = gsn_contour(wks,vd15,res) 

  plotthk(0) = gsn_contour(wks,ts,res) 
  plotthk(1) = gsn_contour(wks,td9,res) 
  plotthk(2) = gsn_contour(wks,td15,res) 
;  plottmp(0) = gsn_contour(wks,tmpstock,res) 
;  plottmp(1) = gsn_contour(wks,tmpdiff9,res) 
;  plottmp(2) = gsn_contour(wks,tmpdiff15,res) 

;************************************************
; create panel
;************************************************

  resvel = True                             ; panel resources
  resvel@gsnFrame = False                 
  resvel@gsnPanelTop = 1.0                 
  resvel@gsnPanelBottom = 0.60                 
  resvel@gsnPanelLabelBar = True		; make a common contour bar
;  resvel@gsnMaximize = True                 ; make as large as possible
  resvel@txString    = "Norm of Velocity"   ; title string (make blank to remove)
  resvel@gsnPanelFigureStrings = (/"bench)","1)","4)","9)","15)"/)   ; add strings to panel

  resthk = True                             ; panel resources
  resthk@gsnFrame = False                 
  resthk@gsnPanelTop = 0.55                 
  resthk@gsnPanelBottom = 0.0                 
  resthk@lbLabelAngleF = 45			; angle of contour bar labels
  resthk@gsnPanelLabelBar = True		; make a common contour bar
;  resthk@gsnMaximize = True                 ; make as large as possible
  resthk@txString    = "Thickness"   ; title string (make blank to remove)
  resthk@gsnPanelFigureStrings = (/"bench)","1)","4)","9)","15)"/)   ; add strings to panel

;  restmp = True                             ; panel resources
;  restmp@gsnFrame = False                 
;  restmp@gsnPanelTop = 0.3                 
;  restmp@gsnPanelBottom = 0.0                 
;  restmp@gsnPanelLabelBar = True		; make a common contour bar
;  restmp@txString    = "Temperature"   ; title string (make blank to remove)
;  restmp@gsnPanelFigureStrings = (/"bench)","1)","4)","9)","15)"/)   ; add strings to panel

  gsn_panel(wks,plotvel,(/1,3/),resvel)                  
  gsn_panel(wks,plotthk,(/2,3/),resthk)                  
;  gsn_panel(wks,plottmp,(/3,3/),restmp)                  

  frame(wks)

end

