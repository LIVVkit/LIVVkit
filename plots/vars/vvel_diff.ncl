; Copyright (c) 2015, UT-BATTELLE, LLC
; All rights reserved.
; 
; Redistribution and use in source and binary forms, with or without
; modification, are permitted provided that the following conditions are met:
; 
; 1. Redistributions of source code must retain the above copyright notice, this
; list of conditions and the following disclaimer.
; 
; 2. Redistributions in binary form must reproduce the above copyright notice,
; this list of conditions and the following disclaimer in the documentation
; and/or other materials provided with the distribution.
; 
; 3. Neither the name of the copyright holder nor the names of its contributors
; may be used to endorse or promote products derived from this software without
; specific prior written permission.
; 
; THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
; ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
; WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
; DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
; FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
; DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
; SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
; CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
; OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
; OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


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
   
    bench_vel = bench->vvel(:,:,:,:)
    bench_scaled = bench_vel@scale_factor * bench_vel
    bench_sum = dim_sum_n(bench_scaled, (/0,1/) )
    bench_scaled@long_name  = "Scaled Benchmark"

    test_vel = test->vvel(:,:,:,:)
    test_scaled = test_vel@scale_factor * test_vel
    test_sum = dim_sum_n(test_scaled, (/0,1/) )
    test_scaled@long_name  = "Scaled Test Run"

    diff_sum = (test_sum - bench_sum) / (dims(0) * dims(1))
    diff_sum@long_name  = "Sum of Difference"


    ;************************************************
    ; create plots
    ;************************************************
    wks = gsn_open_wks("png",plotFile)         ; open a png file
    gsn_define_colormap(wks,"ncview_default")  ; choose a colormap

    plot  = new(3,graphic)

    res                        = True                ; plot mods desired
    res@cnFillOn               = True                ; turn on color
    res@cnFillMode             = "RasterFill"        ; fill array cells individually
    res@gsnSpreadColors        = True                ; use full range of colormap
    res@cnLinesOn              = False               ; turn off contour lines
    res@cnLineLabelsOn         = False               ; turn off contour line labels
    res@gsnDraw                = False               ; don't draw
    res@gsnFrame               = False               ; don't advance frame
    res@cnLevelSelectionMode   = "EqualSpacedLevels" ; Set equal spaced contour levels
    res@cnMaxLevelCount        = 40                  ; limit number of contours to 40
    res@pmLabelBarDisplayMode  = "Always"            ; enable individual label bars
    res@pmLabelBarSide         = "Bottom"            ; place individual bar below each graph
    res@lbOrientation          = "Horizontal"        ; horizonal label bar
    res@lbAutoManage           = False               ; allow to change label bar font height
    res@lbLabelFontHeightF     = 0.02                ; make font height uniform for all label bars
    res@lbBoxLinesOn           = False               ; turn off label bar box lines
    res@cnInfoLabelOn          = False               ; turn off cn info label

    plot(0) = gsn_contour(wks,bench_scaled(dims(0)-1,1,:,:),res)
    plot(1) = gsn_contour(wks,test_scaled(dims(0)-1,1,:,:),res)

    res@cnLineLabelFormat      = "*+.2e"               ; use exponential format for diff plot

    plot(2) = gsn_contour(wks,diff_sum,res)


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
