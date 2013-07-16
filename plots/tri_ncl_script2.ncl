
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
;************************************************
begin
;************************************************
; read in netCDF file
;************************************************
  stock    = addfile("/tmp/work/4ue/SEACISM/cism_tests/gis_5km/data/gis_5km.ice2sea.init.nc","r")
  thckstock  = stock->thk(0,:,:)
  varbl    = addfile("/tmp/work/4ue/SEACISM/cism_tests/gis_5km/data/gis_5km.ice2sea.51-100.nc","r")
  thckvarbl  = varbl->thk(0,:,:)

;************************************************
; create plots
;************************************************
;  PNG = "/tmp/work/4ue/SEACISM/cism_tests/livv/ncl_python/thk"
  wks = gsn_open_wks("png",PNG)                 ; open a png file
;  wks = gsn_open_wks("png","gis_thck_tri_plot")                 ; open a png file
  gsn_define_colormap(wks,"gui_default")
  plot = new(2,graphic)                          ; create a plot array
  
  res                     = True          ; plot mods desired

  res@cnFillOn            = True          ; turn on color
  res@gsnSpreadColors     = True          ; use full range of colormap
  res@cnLinesOn        = False               ; turn off contour lines
  res@gsnDraw             = False           ; don't draw
  res@gsnFrame            = False           ; don't advance frame
  res@cnInfoLabelOn       = False           ; turn off cn info label
  res@vpWidthF            = 0.3           ; change aspect ratio of plot
;  res@vpHeightF           = 0.6

;  thck@_FillValue           = 9.96921e+36 ; set missing values for ncl v5.0

;  res@cnLevelSelectionMode = "ExplicitLevels" ; set explicit contour levels
;  res@cnLevels = (/ 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 500, 1000, 5000, 10000, 25000/) ; set levels

;   plot = gsn_contour(wks,thck,res)       ; contour the variable

  resP = True                          ; panel resources
  resP@gsnMaximize = True              ; make as large as possible
  resP@txString    = "Initial Ice Thickness"   ; (optional) common title
;  gsn_panel(wks,plot,(/1,2/),resP)

  plot(0) = gsn_contour(wks,thckstock,res) 
  plot(1) = gsn_contour(wks,thckvarbl,res)
;  plot(2) = gsn_contour(wks,thckdiff,res) 
;************************************************
; create panel
;************************************************
  resP@gsnPanelLabelBar = True                    ; add common colorbar
  resP@gsnPanelFigureStrings = (/"a)","b)"/)      ; add strings to panel
  gsn_panel(wks,plot,(/1,3/),resP)                ; now draw as one plot

end
