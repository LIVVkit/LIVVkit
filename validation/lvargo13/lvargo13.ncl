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
    ; gl_data       -- Greenland base dataset 
    ;
    ; model_prefix  -- 
    ; model_suffix  -- 
    ; model_start   -- 
    ; model_end     -- 
    ;
    ; plot_file     -- the output file for the plot
    ;
    ;******************************************************
    ; Process the data
    ;******************************************************

    nt = 0
    
    lat2d = gl_data->lat(nt,:,:)   
    lon2d = gl_data->lon(nt,:,:)
    
    dimgrd = dimsizes(lat2d)
    nlat = dimgrd(0)        
    mlon = dimgrd(1)  

    smbacc   = new((/nlat,mlon/),double,"No_FillValue")
    tempacc  = new((/nlat,mlon/),double,"No_FillValue")
    thkacc   = new((/nlat,mlon/),double,"No_FillValue")
    topgacc  = new((/nlat,mlon/),double,"No_FillValue")
    usurfacc = new((/nlat,mlon/),double,"No_FillValue")
    
    uvelacc = new((/nlat-1,mlon-1/),double,"No_FillValue")
    vvelacc = new((/nlat-1,mlon-1/),double,"No_FillValue")
    
    do k = model_start,model_end
        model_name = model_prefix + sprinti("%0.4i",k) + model_suffix
        model = addfile(model_name,"r")
        
        smbacc(:,:) = smbacc(:,:) + model->acab(0,:,:)
        sfacab = model->acab
        
        tempacc(:,:) = tempacc(:,:) + model->temp(0,0,:,:)
        sftemp = model->temp
        
        thkacc(:,:) = thkacc(:,:) + model->thk(0,:,:)
        sfthk = model->thk
        
        topgacc(:,:) = topgacc(:,:) + model->topg(0,:,:)
        sftopg = model->topg
        
        usurfacc(:,:) = usurfacc(:,:) + model->usurf(0,:,:)
        sfusurf = model->usurf
        
        uvelacc(:,:) = uvelacc(:,:) + model->uvel(0,0,:,:)
        sfuvel = model->uvel
        
        vvelacc(:,:) = vvelacc(:,:) + model->vvel(0,0,:,:)
        sfvvel = model->vvel
    end do  

    ; Average the results over the model window
    n_files = model_end - model_start + 1
    smb   = smbacc   / n_files 
    temp  = tempacc  / n_files 
    thk   = thkacc   / n_files 
    topg  = topgacc  / n_files 
    usurf = usurfacc / n_files 
    uvel  = uvelacc  / n_files 
    vvel  = vvelacc  / n_files 

    ; Apply the scale factors if needed
    if(isatt(sfacab,"scale_factor")) then
        smb := smb * sfacab@scale_factor
    end if 
    if(isatt(sftemp,"scale_factor")) then
        temp := temp * sftemp@scale_factor
    end if 
    if(isatt(sfthk,"scale_factor")) then
        thk := thk * sfthk@scale_factor
    end if 
    if(isatt(sftopg,"scale_factor")) then
        topg := topg * sftopg@scale_factor
    end if 
    if(isatt(sfusurf,"scale_factor")) then
        usurf := usurf * sfusurf@scale_factor
    end if 
    if(isatt(sfuvel,"scale_factor")) then
        uvel := uvel * sfuvel@scale_factor
    end if       
    if(isatt(sfvvel,"scale_factor")) then
        vvel := vvel * sfvvel@scale_factor
    end if       

    ; calculate the velocity
    Vel = ((uvel^2) + (vvel^2))^0.5

    
    ;******************************************************
    ; Make plots
    ;******************************************************
    

    wks = gsn_open_wks("png",plot_file)
    
    res1                      = True                        ; plot mods desired 
    res1@gsnDraw              = False                       ; wait to draw the plot until all panels are plotted
    res1@gsnFrame             = False                       ; wait to draw the plot until all panels are plotted
    res1@cnFillOn             = True                        ; turn on color
    res1@cnFillMode           = "RasterFill"                 
    res1@cnLinesOn            = False                       ; no black lines between contours
    res1@gsnLeftString        = ""                          ; no subtitle
    res1@gsnRightString       = ""                          ; no subtitle
    res1@cnFillPalette        = "WhiteBlueGreenYellowRed"   ; select the colormap
    res1@lbTitleOn            = True                        ; add a title to the label bar
    res1@lbTitleFontHeightF   = 0.015                       ; change font for the label bar title 
    res1@lbTitlePosition      = "bottom"                    ; move title to below label bar
    res1@lbLabelFontHeightF   = 0.012                       ; font smaller than default
    res1@pmLabelBarHeightF    = 0.1                         ; wider than default
    res1@pmLabelBarWidthF     = 0.3                         ; smaller than default
    res1@trGridType           = "TriangularMesh"
    res1@mpProjection         = "Stereographic"
    res1@mpDataBaseVersion    = "mediumres"
    res1@mpFillOn             = False                       ; turn off default land map fill
    res1@mpLimitMode          = "Corners"  
    res1@mpLeftCornerLatF     = lat2d(0,0)
    res1@mpLeftCornerLonF     = lon2d(0,0)
    res1@mpRightCornerLatF    = lat2d(nlat-1,mlon-1)
    res1@mpRightCornerLonF    = lon2d(nlat-1,mlon-1)
    res1@mpCenterLonF         = model->mapping@straight_vertical_longitude_from_pole
    res1@mpCenterLatF         = model->mapping@standard_parallel
    res1@tiMainFontHeightF    = 0.012

    resD = res1
    ;FIXME: Get a """Unable to convert string "MPL_bwr" to ColorMap""" error
    ;resD@cnFillPalette        = "MPL_bwr"

    ; panel resources
    resP = True                                            
    resP@gsnMaximize          = True


    ; Surface mass balance
    plot1 = new(3,graphic)   ; create the graphic with 3 panels
    
    xGL := gl_data->smb(nt,:,:)    ; read in actual data
    xn := smb
    
    maxmod = ceil(max(xn))
    maxmeas = ceil(max(xGL))
    if maxmod .ge. maxmeas
    	maxrange  = maxmod
    else
    	maxrange  = maxmeas
    end if
    
    minmod = floor(min(xn))
    minmeas = floor(min(xGL))
    if minmod .le. minmeas
    	minrange  = minmod
    else
    	minrange  = minmeas
    end if
    
    totalrange = (maxrange - minrange)*2
    rng = (maxrange - minrange)/totalrange
    res1@cnLevelSelectionMode = "ManualLevels"
    res1@cnMinLevelValF  = minrange			                ; set the minimum contour level
    res1@cnMaxLevelValF  = maxrange			                ; set the maximum contour level
    res1@cnLevelSpacingF = rng			                    ; set the interval between contours 
	
    xn@lat2d = lat2d 
    xn@lon2d = lon2d
    res1@tiMainString   = "CISM mean: Year"+ sprintf("%3.0f",model_start) + " -" + sprintf("%3.0f",model_end)
    res1@lbTitleString  = " ("+sfacab@units+")"             ; label bar laber for first panel
    
    plot1(0) = gsn_csm_contour_map(wks,xn,res1)             ; create the first panel plot
         
    xGL@lat2d = lat2d
    xGL@lon2d = lon2d
    res1@tiMainString   = "1958-2007 Climatology"
    res1@lbTitleString  = " ("+xGL@units+")" 

    plot1(1) = gsn_csm_contour_map(wks,xGL,res1)
    
    xdif := xn - xGL                                        ; subtract model from data
    xdif@lat2d = lat2d
    xdif@lon2d = lon2d
    resD@tiMainString   = "Difference (CISM - Data)"
    resD@lbTitleString  = " ("+xGL@units+")"
    
    symMinMaxPlt (xdif,21,False,resD)
    plot1(2) = gsn_csm_contour_map(wks,xdif,resD)
  
    resP@txString   = xGL@long_name                         ; title for first set of plots
    gsn_panel(wks,plot1,(/1,3/),resP)                       ; create first set of plots

end

   
  
