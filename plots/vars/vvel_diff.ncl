load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 

begin
    ;************************************************
    ; Variables to be defined in call
    ;************************************************
    ; bench   -- the *.nc benchmark data
    ; test    -- the *.nc test data
    ;
    ;plotFile -- the output file for the plot
    ;
    ;************************************************
    ; Get plot data
    ;************************************************
    dims = dimsizes(bench->vvel(:,:,:,:))
   
    bench_vel = bench->vvel(dims(0)-1,1,:,:)
    bench_scaled = bench_vel@scale_factor * bench_vel
    bench_scaled@long_name  = "Scaled Benchmark"

    test_vel = test->vvel(dims(0)-1,1,:,:)
    test_scaled = test_vel@scale_factor * test_vel
    test_scaled@long_name  = "Scaled Test Run"

    diff_scaled = test_scaled - bench_scaled
    diff_scaled@long_name  = "Scaled Difference"


    ;************************************************
    ; create plots
    ;************************************************
    wks = gsn_open_wks("png",plotFile)         ; open a png file
    gsn_define_colormap(wks,"wgne15")          ; choose a colormap

    plot  = new(3,graphic)

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

    plot(0) = gsn_contour(wks,bench_scaled,res)
    plot(1) = gsn_contour(wks,test_scaled,res)
    plot(2) = gsn_contour(wks,diff_scaled,res)


    ;************************************************
    ; create panel
    ;************************************************
    resPanel = True                       ; panel resources
    resPanel@gsnFrame = False                 
    resPanel@gsnPanelTop = 1.0                 
    resPanel@gsnPanelBottom = 0.10
    resPanel@gsnMaximize = True
    resPanel@txString = "V Velocity"   ; title string (make blank to remove)

    gsn_panel(wks,plot,(/1,3/),resPanel)
    frame(wks)

end
