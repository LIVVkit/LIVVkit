; Copyright (c) 2015,2016, UT-BATTELLE, LLC
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


; Created by Lauren Vargo 06/11/2015
; Reworked by Joseph H Kennedy for LIVVkit on 08/24/15

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl" 

begin
    ;******************************************************
    ; Variables to be defined in call
    ;******************************************************
    ; gl_data        -- Greenland base dataset 
    ; vel_data       -- INSAR velocity dataset 
    ;
    ; model_prefix   -- 
    ; model_suffix   -- 
    ; model_start    -- 
    ; model_end      -- 
    ;
    ; plot_file_base -- the output file for the plot
    ;
    ;******************************************************
    ; Process the data
    ;******************************************************

    nt = 0
    
    gl_lat2d = gl_data->lat(nt,:,:)   
    gl_lon2d = gl_data->lon(nt,:,:)
    
    dimgrd = dimsizes(gl_lat2d)
    nlat = dimgrd(0)        
    mlon = dimgrd(1)  

    smb   = new((/nlat,mlon/),double,"No_FillValue")
    temp  = new((/nlat,mlon/),double,"No_FillValue")
    thk   = new((/nlat,mlon/),double,"No_FillValue")
    topg  = new((/nlat,mlon/),double,"No_FillValue")
    usurf = new((/nlat,mlon/),double,"No_FillValue")
    
    uvel = new((/nlat-1,mlon-1/),double,"No_FillValue")
    vvel = new((/nlat-1,mlon-1/),double,"No_FillValue")
    
    do k = model_start,model_end
        model_name = model_prefix + sprinti("%0.4i",k) + model_suffix
        model = addfile(model_name,"r")
        
        smb(:,:)   = smb(:,:) + model->acab(0,:,:)
        temp(:,:)  = temp(:,:) + model->temp(0,0,:,:)
        thk(:,:)   = thk(:,:) + model->thk(0,:,:)
        topg(:,:)  = topg(:,:) + model->topg(0,:,:)
        usurf(:,:) = usurf(:,:) + model->usurf(0,:,:)
        uvel(:,:)  = uvel(:,:) + model->uvel(0,0,:,:)
        vvel(:,:)  = vvel(:,:) + model->vvel(0,0,:,:)
    end do  

    ; Average the results over the model window
    n_files = model_end - model_start + 1
    smb   = smb   / n_files 
    temp  = temp  / n_files 
    thk   = thk   / n_files 
    topg  = topg  / n_files 
    usurf = usurf / n_files 
    uvel  = uvel  / n_files 
    vvel  = vvel  / n_files 

    ; Apply the scale factors if needed
    if(isatt(model->acab,"scale_factor")) then
        smb := smb * model->acab@scale_factor
    end if 
    if(isatt(model->temp,"scale_factor")) then
        temp := temp * model->temp@scale_factor
    end if 
    if(isatt(model->thk,"scale_factor")) then
        thk := thk * model->thk@scale_factor
    end if 
    if(isatt(model->topg,"scale_factor")) then
        topg := topg * model->topg@scale_factor
    end if 
    if(isatt(model->usurf,"scale_factor")) then
        usurf := usurf * model->usurf@scale_factor
    end if 
    if(isatt(model->uvel,"scale_factor")) then
        uvel := uvel * model->uvel@scale_factor
    end if       
    if(isatt(model->vvel,"scale_factor")) then
        vvel := vvel * model->vvel@scale_factor
    end if       

    ; calculate the velocity
    vel = ((uvel^2) + (vvel^2))^0.5

    
    ;******************************************************
    ; Make plots
    ;******************************************************
    
    res_data                      = True                        ; plot mods desired 
    res_data@gsnDraw              = False                       ; wait to draw the plot until all panels are plotted
    res_data@gsnFrame             = False                       ; wait to draw the plot until all panels are plotted
    res_data@cnFillOn             = True                        ; turn on color
    res_data@cnFillMode           = "RasterFill"                 
    res_data@cnLinesOn            = False                       ; no black lines between contours
    res_data@gsnLeftString        = ""                          ; no subtitle
    res_data@gsnRightString       = ""                          ; no subtitle
    res_data@cnFillPalette        = "WhiteBlueGreenYellowRed"   ; select the colormap
    res_data@lbTitleOn            = True                        ; add a title to the label bar
    res_data@lbTitleFontHeightF   = 0.015                       ; change font for the label bar title 
    res_data@lbTitlePosition      = "bottom"                    ; move title to below label bar
    res_data@lbLabelFontHeightF   = 0.012                       ; font smaller than default
    res_data@pmLabelBarHeightF    = 0.1                         ; wider than default
    res_data@pmLabelBarWidthF     = 0.3                         ; smaller than default
    res_data@trGridType           = "TriangularMesh"
    res_data@mpProjection         = "Stereographic"
    res_data@mpDataBaseVersion    = "mediumres"
    res_data@mpFillOn             = False                       ; turn off default land map fill
    res_data@mpLimitMode          = "Corners"  
    res_data@mpLeftCornerLatF     = gl_lat2d(0,0)
    res_data@mpLeftCornerLonF     = gl_lon2d(0,0)
    res_data@mpRightCornerLatF    = gl_lat2d(nlat-1,mlon-1)
    res_data@mpRightCornerLonF    = gl_lon2d(nlat-1,mlon-1)
    res_data@mpCenterLonF         = model->mapping@straight_vertical_longitude_from_pole
    res_data@mpCenterLatF         = model->mapping@standard_parallel
    res_data@tiMainFontHeightF    = 0.012

    res_diff = res_data
    ;NOTE: "MPL_bwr" is only available in version 6.2 and later
    ;res_diff@cnFillPalette        = "MPL_bwr"
    res_diff@cnFillPalette        = "BlWhRe"

    ; panel resources
    res_panel = True                                            
    res_panel@gsnMaximize          = True
    
    undef("make_a_plot")                                    ; Just to make sure this isn't alread a function
    procedure make_a_plot(bench_data, test_data, range_mod, plot_name, bench_title)
    local wks, max_test, max_bench, max_range, min_test, min_bench, min_range, total_range, rng, diff_data, plot
    begin
        wks = gsn_open_wks("png", plot_name)
        
        max_test = ceil(max(test_data))
        max_bench = ceil(max(bench_data))
        if max_test .ge. max_bench
            max_range = max_test
        else
            max_range = max_bench
        end if
        
        min_test = floor(min(test_data))
        min_bench = floor(min(bench_data))
        if min_test .le. min_bench
            min_range  = min_test
        else
            min_range  = min_bench
        end if
        
        total_range = (max_range - min_range)*range_mod
        rng = (max_range - min_range)/total_range
        
        test_data@lat2d = gl_lat2d 
        test_data@lon2d = gl_lon2d
        
        bench_data@lat2d = gl_lat2d
        bench_data@lon2d = gl_lon2d
        
        diff_data := test_data - bench_data                                        ; subtract model from data
        diff_data@lat2d = gl_lat2d
        diff_data@lon2d = gl_lon2d
        
        plot = new(3,graphic)   ; create the graphic with 3 panels
        
        res_data@cnLevelSelectionMode = "ManualLevels"
        res_data@cnMinLevelValF  := min_range			                ; set the minimum contour level
        res_data@cnMaxLevelValF  := max_range			                ; set the maximum contour level
        res_data@cnLevelSpacingF := rng			                    ; set the interval between contours 
        res_data@tiMainString   := "CISM mean: Year"+ sprintf("%3.0f",model_start) + " -" + sprintf("%3.0f",model_end)
        res_data@lbTitleString  := " ("+bench_data@units+")"             ; label bar laber for first panel
        
        plot(0) = gsn_csm_contour_map(wks,test_data,res_data)             ; create the first panel plot
             
        res_data@tiMainString   := bench_title 
        res_data@lbTitleString  := " ("+bench_data@units+")" 

        plot(1) = gsn_csm_contour_map(wks,bench_data,res_data)
        
        res_diff@tiMainString   := "Difference (CISM - Data)"
        res_diff@lbTitleString  := " ("+bench_data@units+")"
        
        symMinMaxPlt (diff_data,21,False,res_diff)
        plot(2) = gsn_csm_contour_map(wks,diff_data,res_diff)
      
        res_panel@txString   := bench_data@long_name                         ; title for first set of plots
        gsn_panel(wks,plot,(/1,3/),res_panel)                       ; create first set of plots
    
    end

    ; for the plot procedure
    range_mod = 2

    ; surface mass balance
    make_a_plot(gl_data->smb(nt,:,:), smb, range_mod, plot_file_base+"_smb.png", "1958-2007 Climatology")

    ; temperature
    gl_temp = gl_data->surftemp(nt,:,:)
	do r = 0,nlat-1
     	do c = 0,mlon-1
			if ( thk(r,c) .eq. 0 )
				gl_temp(r,c) = 0
			end if
		end do 
	end do 	
    
    make_a_plot(gl_temp, temp, range_mod, plot_file_base+"_temp.png", "Present day "+gl_data->surftemp@long_name)

    ; thickness
    range_mod := 1.0/100
    make_a_plot(gl_data->thk(nt,:,:), thk, range_mod, plot_file_base+"_thk.png", "Present day "+gl_data->thk@long_name)

    ; topography
    range_mod := 1.0/200
    make_a_plot(gl_data->topg(nt,:,:), topg, range_mod, plot_file_base+"_topg.png", "Present day "+gl_data->topg@long_name)

    ; surface elevation
    range_mod := 1.0/100
    make_a_plot(gl_data->usrf(nt,:,:), usurf, range_mod, plot_file_base+"_usurf.png", "Present day "+gl_data->usrf@long_name)
    
    ; absolute velocity (surface)
    vx = vel_data->vx(nt,:,:)   
    vy = vel_data->vy(nt,:,:)
    
    velnorm := ((vx^2) + (vy^2))^0.5
   
    do e = 0,1500
        do f = 0,2800
            if ( velnorm(f,e) .gt. 1e10 )
                velnorm(f,e) = 0.0
            end if
        end do
    end do

    xi = vel_data->x1(:)
    yi = vel_data->y1(:)
    klon = model->x0(:) 
    klat = model->y0(:) 
    velnorm_data = linint2 (xi,yi,velnorm,False,klon,klat,0)
     
    ;NOTE: velocity data is sufficiently different such that we'll have to manually make the plot.
    ;make_a_plot(velnorm_data, vel, range_mod, plot_file_base+"_velnorm.png", "Present day "+gl_data->usrf@long_name)
    bench_data = velnorm_data
    test_data = vel 

    wks = gsn_open_wks("png", plot_file_base+"_velnorm.png")
    
    max_test = ceil(max(test_data))
    max_bench = ceil(max(bench_data))
    if max_test .ge. max_bench
        max_range = max_test
    else
        max_range = max_bench
    end if
    ln_max = log10(max(max_range))
    ;logspace = (10)^(fspan(0,lnmax,21))       ; logrithmically spaced contours
    logspace = ((/1,10,100,1000,10000/))
    
    test_data@lat2d = gl_lat2d 
    test_data@lon2d = gl_lon2d
    
    bench_data@lat2d = gl_lat2d
    bench_data@lon2d = gl_lon2d
    
    diff_data := test_data - bench_data                                        ; subtract model from data
    diff_data@lat2d = gl_lat2d
    diff_data@lon2d = gl_lon2d
    
    plot = new(3,graphic)   ; create the graphic with 3 panels
    
    res_data@cnLevelSelectionMode = "ExplicitLevels"                        ; set explicit contour levels 
    res_data@cnLevels = (logspace)                             ; set levels 
    res_data@tiMainString   := "CISM mean: Year"+ sprintf("%3.0f",model_start) + " -" + sprintf("%3.0f",model_end)
    res_data@lbTitleString  := " ("+gl_data->surfvelmag@units+")"             ; label bar laber for first panel
    
    plot(0) = gsn_csm_contour_map(wks,test_data,res_data)             ; create the first panel plot
         
    res_data@tiMainString   := "Present day "+gl_data->surfvelmag@long_name
    res_data@lbTitleString  := " ("+gl_data->surfvelmag@units+")" 

    plot(1) = gsn_csm_contour_map(wks,bench_data,res_data)
    
    res_diff@cnLevelSelectionMode = "ExplicitLevels"                        ; set explicit contour levels 
    logspace := ((/-10000,-1000,-100-10,-1,0,1,10,100,1000,10000/))
    res_diff@cnLevels = (logspace)                             ; set levels 
    res_diff@tiMainString   := "Difference (CISM - Data)"
    res_diff@lbTitleString  := " ("+gl_data->surfvelmag@units+")"
    
    symMinMaxPlt (diff_data,21,False,res_diff)
    plot(2) = gsn_csm_contour_map(wks,diff_data,res_diff)
  
    res_panel@txString   := gl_data->surfvelmag@long_name                         ; title for first set of plots
    gsn_panel(wks,plot,(/1,3/),res_panel)                       ; create first set of plots

end
 
