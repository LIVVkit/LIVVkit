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
    asciiwrite("log","hello1")    
    gl_lat2d_data = gl_data->lat(nt,:,:)   
    gl_lon2d_data = gl_data->lon(nt,:,:)
    gdims=getfilevardimsizes(gl_data,"lon")
    nlat_data = gdims(1)
    mlon_data = gdims(2)        
    asciiwrite("log","hello2")     
    
    ;Get model netCDF grid dimensions
    model_name = model_prefix + sprinti("%0.4i",model_start) + model_suffix
    model = addfile(model_name,"r")
    gl_lat2d_model = model->lat(nt,:,:)   
    gl_lon2d_model = model->lon(nt,:,:) 
    gdims=getfilevardimsizes(model,"lon")       
    nlat_model = gdims(1)
    mlon_model = gdims(2)
    asciiwrite("log","hello3") 
    smb   = new((/nlat_model,mlon_model/),double,"No_FillValue")
    temp  = new((/nlat_model,mlon_model/),double,"No_FillValue")
    thk   = new((/nlat_model,mlon_model/),double,"No_FillValue")
    topg  = new((/nlat_model,mlon_model/),double,"No_FillValue")
    usurf = new((/nlat_model,mlon_model/),double,"No_FillValue")
    uvel = new((/nlat_model-1,mlon_model-1/),double,"No_FillValue")
    vvel = new((/nlat_model-1,mlon_model-1/),double,"No_FillValue")
    do k = model_start,model_end
        model_name = model_prefix + sprinti("%0.4i",k) + model_suffix
	model = addfile(model_name,"r")
        smb(:,:)   = smb(:,:)   + model->acab(0,:,:)
        temp(:,:)  = temp(:,:)  + model->tempstag(0,0,:,:)
        thk(:,:)   = thk(:,:)   + model->thk(0,:,:)
        topg(:,:)  = topg(:,:)  + model->topg(0,:,:)
        usurf(:,:) = usurf(:,:) + model->usurf(0,:,:)
        uvel(:,:)  = uvel(:,:)  + model->uvel(0,0,:,:)
        vvel(:,:)  = vvel(:,:)  + model->vvel(0,0,:,:)
    end do  
    asciiwrite("log","hello4")    
    ; Average the results over the model window
    n_files = model_end - model_start + 1
    smb   = smb   / n_files 
    temp  = temp  / n_files 
    thk   = thk   / n_files 
    topg  = topg  / n_files 
    usurf = usurf / n_files 
    uvel  = uvel  / n_files 
    vvel  = vvel  / n_files 
    asciiwrite("log","hello6")
    ; Apply the scale factors if needed
    if(isatt(model->acab,"scale_factor")) then
        smb := smb * model->acab@scale_factor
    end if 
    if(isatt(model->tempstag,"scale_factor")) then
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

    usurf = where( usurf .le. 0.0 , 0.0 , usurf) 

    ; calculate the velocity
    vel = ((uvel^2) + (vvel^2))^0.5
    
    ;******************************************************
    ; Make plots
    ;******************************************************
    
    ;;;;GENERATE COMMON PLOT CONFIGS FOR MODEL OUTPUT
    res_model                      = True                        ; plot mods desired 
    res_model@gsnDraw              = False                       ; wait to draw the plot until all panels are plotted
    res_model@gsnFrame             = False                       ; wait to draw the plot until all panels are plotted
    res_model@cnFillOn             = True                        ; turn on color
    res_model@cnFillMode           = "RasterFill"                 
    res_model@cnLinesOn            = False                       ; no black lines between contours
    res_model@gsnLeftString        = ""                          ; no subtitle
    res_model@gsnRightString       = ""                          ; no subtitle
    res_model@cnFillPalette        = "topo_15lev"                ; select the colormap
    res_model@lbTitleOn            = True                        ; add a title to the label bar
    res_model@lbTitleFontHeightF   = 0.015                       ; change font for the label bar title 
    res_model@lbTitlePosition      = "bottom"                    ; move title to below label bar
    res_model@lbLabelFontHeightF   = 0.012                       ; font smaller than default
    res_model@pmLabelBarHeightF    = 0.1                         ; wider than default
    res_model@pmLabelBarWidthF     = 0.3                         ; smaller than default
    res_model@trGridType           = "TriangularMesh"
    res_model@mpProjection         = "Stereographic"
    res_model@mpDataBaseVersion    = "mediumres"
    res_model@mpFillOn             = False                       ; turn off default land map fill
    res_model@mpLimitMode          = "Corners"     
    asciiwrite("log","hello7.1") 
    res_model@mpLeftCornerLatF     = gl_lat2d_model(0,0)
    res_model@mpLeftCornerLonF     = gl_lon2d_model(0,0)
    asciiwrite("log","hello7.2")    
    res_model@mpRightCornerLatF    = gl_lat2d_model(nlat_model-1,mlon_model-1)
    res_model@mpRightCornerLonF    = gl_lon2d_model(nlat_model-1,mlon_model-1)
    res_model@mpCenterLonF         = model->mapping@straight_vertical_longitude_from_pole
    res_model@mpCenterLatF         = model->mapping@standard_parallel
    
    res_model@tiMainFontHeightF    = 0.012
    
    ;;;;COPY ABOVE PLOT CONFIG, THEN MODIFY FOR COMPARISON PLOT   
     
    res_data=res_model
    res_data@mpRightCornerLatF    = gl_lat2d_data(nlat_data-1,mlon_data-1)
    res_data@mpRightCornerLonF    = gl_lon2d_data(nlat_data-1,mlon_data-1) 

    ;;;;COPY ABOVE PLOT CONFIG FOR DIFFERENCE PLOT

    res_diff=res_data
    res_diff@cnFillPalette        = "BlueDarkRed18"

    ; panel resources
    res_panel = True                                            
    res_panel@gsnMaximize          = True
    
    undef("make_a_plot")                                    ; Just to make sure this isn't already a function

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;    
    procedure make_a_plot(bench_data, test_data, color_range, plot_name, bench_title)
    local wks, max_range, min_range, diff_data, plot
    begin
        wks = gsn_open_wks("png", plot_name)
    asciiwrite("log","Hello1.1")      
        test_data@lat2d = gl_lat2d_model 
        test_data@lon2d = gl_lon2d_model
    asciiwrite("log","Hello1.2")         
        bench_data@lat2d = gl_lat2d_data
        bench_data@lon2d = gl_lon2d_data
    asciiwrite("log","Hello1.3")         
        diff_data := test_data - bench_data					   ; subtract model from data
        diff_data@lat2d = gl_lat2d_data
        diff_data@lon2d = gl_lon2d_data	   
    asciiwrite("log","Hello1.4") 	
        plot = new(3,graphic)   ; create the graphic with 3 panels
	
        res_model@cnLevelSelectionMode = "ManualLevels"
        res_model@cnMinLevelValF  := color_range(0)
        res_model@cnMaxLevelValF  := color_range(1)
        res_model@cnLevels := 100		
        res_model@tiMainString   := "CISM mean: Year"+ sprintf("%3.0f",model_start) + " -" + sprintf("%3.0f",model_end)
        res_model@lbTitleString  := " ("+bench_data@units+")"             ; label bar laber for first panel
        plot(0) = gsn_csm_contour_map(wks,test_data,res_model)             ; create the first panel plot
    asciiwrite("log","Hello1.5") 
        res_data@tiMainString   := bench_title 
        res_data@lbTitleString  := " ("+bench_data@units+")"
	res_data@cnLevelSelectionMode = "ManualLevels"
        res_data@cnMinLevelValF  := color_range(0)
        res_data@cnMaxLevelValF  := color_range(1)
        res_data@cnLevels := 100		
        plot(1) = gsn_csm_contour_map(wks,bench_data,res_data)
    asciiwrite("log","Hello1.6") 	
        res_diff@tiMainString	:= "Difference (CISM - Data)"
        res_diff@lbTitleString  := " ("+bench_data@units+")"
	res_diff@cnLevelSelectionMode = "ManualLevels"	
	res_diff@cnMinLevelValF  := min(diff_data); set the minimum contour level
        res_diff@cnMaxLevelValF  := max(diff_data); set the maximum contour level
        res_diff@cnLevels := 100			                    ; set the interval between contours 
        ;symMinMaxPlt (diff_data,21,False,res_diff)	
    asciiwrite("log","Hello1.7")	
        plot(2) = gsn_csm_contour_map(wks,diff_data,res_diff)
    asciiwrite("log","Hello1.8")	
        res_panel@txString   := bench_data@long_name			     ; title for first set of plots	
        gsn_panel(wks,plot,(/1,3/),res_panel)                                ; create first set of plots
    asciiwrite("log","Hello1.9")	
    end
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


    ; for the plot procedure

asciiwrite("log","hello12")

    ; surface mass balance
    color_range=(/-2.0,1.0/)
    make_a_plot(gl_data->acab(nt,:,:), smb, color_range, plot_file_base+"_smb.png", "1958-2007 Climatology")
asciiwrite("log","hello12")
    ; temperature
    color_range=(/-30.0,0.0/)    
    make_a_plot(gl_data->tempstag(nt,0,:,:), temp, color_range, plot_file_base+"_temp.png", "Present day "+gl_data->surftemp@long_name)

    ; thickness
asciiwrite("log","hello13")    
    asciiwrite("log",max(thk))
    data_thk := gl_data->thk(nt,:,:)
    if(isatt(gl_data->thk,"scale_factor")) then
        data_thk := data_thk * gl_data->thk@scale_factor
    end if     
    data_thk@long_name=gl_data->thk@long_name
    color_range=(/0.0,3000.0/)    
    make_a_plot(data_thk, thk, color_range, plot_file_base+"_thk.png", "Present day "+gl_data->thk@long_name)
asciiwrite("log","hello12")   
    ; topography
    color_range=(/0.0,3000.0/)
    topg_data=  gl_data->topg(nt,:,:)
    where( topg_data < 0 , 0.0 , topg_data)
    make_a_plot(topg_data, topg, color_range, plot_file_base+"_topg.png", "Present day "+gl_data->topg@long_name)
asciiwrite("log","hello14")
    ; surface elevation
    color_range=(/0.0,3000.0/)
    data_usrf=gl_data->usrf(nt,:,:)
    if(isatt(gl_data->usrf,"scale_factor")) then
       data_usrf  := data_usrf * gl_data->usrf@scale_factor
    end if     
asciiwrite("log","hello15")    
    data_usrf = where( data_usrf .lt. 0.0 , 0.0 , data_usrf)        

    make_a_plot(data_usrf, usurf, color_range, plot_file_base+"_usurf.png", "Present day "+gl_data->usrf@long_name)
    
    color_range=(/0.0,1000.0/)    
    
    data_velnorm=gl_data->velnorm(nt,0,:,:)
    asciiwrite("log","hello123") 
    if(isatt(gl_data->velnorm,"scale_factor")) then
       data_velnorm  := data_velnorm * gl_data->velnorm@scale_factor
    end if
asciiwrite("log","hello16")    
    data_velnorm@long_name=gl_data->velnorm@long_name
    
    data_velnorm = where( data_velnorm .gt. 500.0 , 500.0 , data_velnorm )
    vel = where( vel .gt. 500.0 , 500.0 , vel )
    
    make_a_plot(data_velnorm, vel, color_range, plot_file_base+"_velnorm.png", "Present day "+gl_data->velnorm@long_name)    
    plot = new(3,graphic)   ; create the graphic with 3 panels
asciiwrite("log","hello17")     
    res_data@cnLevelSelectionMode = "ExplicitLevels"                        ; set explicit contour levels 
    res_data@cnLevels = (logspace)                             ; set levels 
    res_data@tiMainString   := "CISM mean: Year"+ sprintf("%3.0f",model_start) + " -" + sprintf("%3.0f",model_end)
    res_data@lbTitleString  := " ("+gl_data->surfvelmag@units+")"             ; label bar laber for first panel
asciiwrite("log","hello18")     
    plot(0) = gsn_csm_contour_map(wks,test_data,res_data)             ; create the first panel plot
         
    res_data@tiMainString   := "Present day "+gl_data->surfvelmag@long_name
    res_data@lbTitleString  := " ("+gl_data->surfvelmag@units+")" 

    plot(1) = gsn_csm_contour_map(wks,bench_data,res_data)
asciiwrite("log","hello17")     
    res_diff@cnLevelSelectionMode = "ExplicitLevels"                        ; set explicit contour levels 
    ;logspace := ((/-10000,-1000,-100-10,-1,0,1,10,100,1000,10000/))
    ;res_diff@cnLevels = (logspace)                             ; set levels 
    res_diff@tiMainString   := "Difference (CISM - Data)"
    res_diff@lbTitleString  := " ("+gl_data->surfvelmag@units+")"
    
    symMinMaxPlt (diff_data,21,False,res_diff)
    plot(2) = gsn_csm_contour_map(wks,diff_data,res_diff)
  
    res_panel@txString   := gl_data->surfvelmag@long_name       ; title for first set of plots
    gsn_panel(wks,plot,(/1,3/),res_panel)                       ; create first set of plots

end
 
